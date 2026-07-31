#!/usr/bin/env python3
"""Run deterministic preflight checks on one SMS draft."""

from __future__ import annotations

import argparse
import ipaddress
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


PLACEHOLDER_PATTERNS = (
    re.compile(r"(?<![A-Za-z])x{2,}(?![A-Za-z])", re.IGNORECASE),
    re.compile(r"x月x日|x{1,2}[-—–~至]x{1,2}(?:℃|度)?", re.IGNORECASE),
    re.compile(r"\b(?:TBD|TODO)\b|待补|待填"),
    re.compile(r"\{\{[^{}\r\n]{1,64}\}\}"),
    re.compile(r"\$\{[^{}\r\n]{1,64}\}"),
    re.compile(r"(?<![\{\$])\{[^{}\r\n]{1,64}\}(?!\})"),
    re.compile(r"[\[【（(]\s*待确认(?:[:：][^\]】）)\r\n]*)?[\]】）)]"),
    re.compile(r"[（(][^）)\r\n]{0,32}待确认[）)]"),
    re.compile(r"[（(][^）)]*(?:推文链接|查询链接|报名链接|URL)[^）)]*[）)]", re.IGNORECASE),
)
URL_PATTERN = re.compile(r"https?://[^\s）)】》]+", re.IGNORECASE)
BARE_DOMAIN_PATTERN = re.compile(
    r"(?<![@:/A-Za-z0-9_.-])"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}(?::\d{1,5})?(?:/[^\s，。；！？]*)?",
    re.IGNORECASE,
)
LINK_INTENT_PATTERN = re.compile(
    r"(?:点击|打开|访问)(?:此)?(?:链接|网址)|详情(?:请)?点击",
)
DELIMITER_PAIRS = (("（", "）"), ("(", ")"), ("【", "】"), ("“", "”"), ("‘", "’"), ("《", "》"))


def make_issue(rule: str, severity: str, excerpt: str, message: str) -> dict[str, str]:
    return {
        "rule": rule,
        "severity": severity,
        "excerpt": excerpt,
        "message": message,
    }


def placeholder_issues(text: str) -> tuple[dict[str, str], ...]:
    matches = tuple(
        match.group(0)
        for pattern in PLACEHOLDER_PATTERNS
        for match in pattern.finditer(text)
    )
    unique_matches = tuple(dict.fromkeys(matches))
    return tuple(
        make_issue(
            "unresolved-placeholder",
            "block",
            "未替换变量",
            "存在未替换的变量或临时链接，正式发送前必须替换并复核。",
        )
        for value in unique_matches
    )


def delimiter_issues(text: str) -> tuple[dict[str, str], ...]:
    open_to_close = dict(DELIMITER_PAIRS)
    close_to_open = {right: left for left, right in DELIMITER_PAIRS}
    stack: tuple[str, ...] = ()
    for character in text:
        if character in open_to_close:
            stack = stack + (character,)
        elif character in close_to_open:
            if not stack or stack[-1] != close_to_open[character]:
                return (
                    make_issue(
                        "unbalanced-delimiter",
                        "block",
                        character,
                        "成对符号的闭合顺序错误或缺少左侧符号。",
                    ),
                )
            stack = stack[:-1]
    return (
        make_issue(
            "unbalanced-delimiter",
            "block",
            stack[-1],
            "成对符号缺少右侧闭合符号。",
        ),
    ) if stack else ()


def redact_url(url: str) -> str:
    try:
        parsed = urlsplit(url)
        return f"{parsed.scheme or 'url'}://{parsed.hostname or '无有效域名'}/…"
    except ValueError:
        return "无效链接"


def safe_urlsplit(url: str):
    try:
        return urlsplit(url)
    except ValueError:
        return None


def valid_hostname(hostname: str | None) -> bool:
    if not hostname:
        return False
    try:
        return ipaddress.ip_address(hostname).is_global
    except ValueError:
        pass
    try:
        normalized_hostname = hostname.rstrip(".").encode("idna").decode("ascii")
    except UnicodeError:
        return False
    if len(normalized_hostname) > 253 or "." not in normalized_hostname:
        return False
    labels = normalized_hostname.split(".")
    return all(
        label
        and len(label) <= 63
        and re.fullmatch(r"[A-Za-z0-9-]+", label)
        and not label.startswith("-")
        and not label.endswith("-")
        for label in labels
    )


def valid_port(parsed) -> bool:
    try:
        port = parsed.port
    except ValueError:
        return False
    return port is None or 1 <= port <= 65535


def url_issues(text: str) -> tuple[dict[str, str], ...]:
    urls = tuple(match.group(0).rstrip("。；;，,！!") for match in URL_PATTERN.finditer(text))
    parsed_urls = tuple((url, safe_urlsplit(url)) for url in urls)
    malformed = tuple(
        url
        for url, parsed in parsed_urls
        if parsed is None
        or parsed.scheme not in {"http", "https"}
        or not valid_hostname(parsed.hostname)
        or not valid_port(parsed)
    )
    valid_urls = tuple(url for url, parsed in parsed_urls if url not in malformed)
    insecure = tuple(url for url in valid_urls if urlsplit(url).scheme == "http")
    bare_domains = tuple(match.group(0) for match in BARE_DOMAIN_PATTERN.finditer(text))
    missing_url = bool(LINK_INTENT_PATTERN.search(text)) and not valid_urls
    missing_url_issues = (
        make_issue(
            "missing-url",
            "block",
            "链接指令",
            "正文要求用户点击链接，但未检测到格式有效的完整 URL。",
        ),
    ) if missing_url else ()
    return (
        tuple(
            make_issue("malformed-url", "block", redact_url(url), "链接格式不完整或域名不可解析。")
            for url in malformed
        )
        + tuple(
            make_issue(
                "bare-domain-url",
                "block",
                redact_url(f"https://{domain}"),
                "检测到未带 http/https 协议的裸域名，发送前需替换为完整并已核验的链接。",
            )
            for domain in bare_domains
        )
        + missing_url_issues
        + tuple(
            make_issue("insecure-url", "warn", redact_url(url), "链接使用 http；确认发送平台和落地页是否允许。")
            for url in insecure
        )
    )


def formatting_issues(text: str) -> tuple[dict[str, str], ...]:
    checks = (
        (
            r"\\",
            "stray-backslash",
            "block",
            "发现反斜杠，通常是误输入或错误分隔符。",
        ),
        (
            r"(?<=[\u4e00-\u9fff])[,;](?=[\u4e00-\u9fff])",
            "ascii-punctuation",
            "warn",
            "中文句子中混入半角标点，建议改为全角标点。",
        ),
        (
            r"[，。！？；：、]{2,}",
            "repeated-punctuation",
            "warn",
            "发现连续中文标点，请确认是否误输。",
        ),
        (
            r"[ \t]{2,}|[ \t]+[，。！？；：]",
            "abnormal-spacing",
            "warn",
            "发现多余空格或标点前空格。",
        ),
    )
    return tuple(
        make_issue(rule, severity, match.group(0), message)
        for pattern, rule, severity, message in checks
        for match in re.finditer(pattern, text)
    )


def advisory_issues(text: str) -> tuple[dict[str, str], ...]:
    missing_signature = (
        make_issue(
            "missing-sender-signature",
            "warn",
            "短信开头",
            "未检测到开头的【发送方】签名；若通道会自动添加或本场景不要求，可忽略。",
        ),
    ) if not re.match(r"^【[^】\r\n]{2,20}】", text.strip()) else ()
    missing_ending = (
        make_issue(
            "missing-ending-punctuation",
            "warn",
            "短信结尾",
            "正文末尾缺少结束标点，请确认是否为完整文案。",
        ),
    ) if text and text.rstrip()[-1] not in "。！？!?.）)】》" else ()
    return missing_signature + missing_ending


def lint(text: str) -> dict[str, object]:
    normalized = text.replace("\r\n", "\n").strip()
    empty_issues = (
        make_issue("empty-message", "block", "空正文", "短信正文为空，不能发送。"),
    ) if not normalized else ()
    issues = (
        empty_issues
        +
        placeholder_issues(normalized)
        + delimiter_issues(normalized)
        + url_issues(normalized)
        + formatting_issues(normalized)
        + advisory_issues(normalized)
    )
    utf16_units = len(normalized.encode("utf-16-le")) // 2
    estimated_segments = 0 if not normalized else (1 if utf16_units <= 70 else math.ceil(utf16_units / 67))
    return {
        "character_count": len(normalized),
        "utf16_units": utf16_units,
        "estimated_ucs2_segments": estimated_segments,
        "segment_note": "仅作中文短信保守估算；实际拆分、签名和计费以发送平台规则为准。",
        "has_blocker": any(issue["severity"] == "block" for issue in issues),
        "issues": issues,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint one Chinese SMS draft.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="SMS text to check.")
    source.add_argument("--file", type=Path, help="UTF-8 text file containing the SMS.")
    source.add_argument("--stdin", action="store_true", help="Read SMS text from standard input.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.text is not None:
        text = args.text
    elif args.file is not None:
        text = args.file.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    result = lint(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["has_blocker"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
