import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("lint_sms.py")
SPEC = importlib.util.spec_from_file_location("lint_sms", SCRIPT)
LINT_SMS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT_SMS)


def run_lint(text: str, use_stdin: bool = False) -> dict:
    command = [sys.executable, str(SCRIPT), "--stdin"] if use_stdin else [
        sys.executable,
        str(SCRIPT),
        "--text",
        text,
    ]
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        input=text if use_stdin else None,
    )
    return {"code": result.returncode, "payload": json.loads(result.stdout)}


class SmsLintTests(unittest.TestCase):
    def test_clean_message_has_no_blocker(self):
        result = run_lint("【示例赛事】亲爱的选手，比赛将于4月19日7:30开跑，请提前抵达。")
        self.assertEqual(result["code"], 0)
        self.assertFalse(result["payload"]["has_blocker"])

    def test_placeholders_and_backslash_block_sending(self):
        result = run_lint("【示例赛事】亲爱的XXX，气温xx℃\\请及时补水。")
        rules = {item["rule"] for item in result["payload"]["issues"]}
        self.assertEqual(result["code"], 1)
        self.assertIn("unresolved-placeholder", rules)
        self.assertIn("stray-backslash", rules)

    def test_placeholder_link_is_blocked_but_real_url_is_not(self):
        blocked = run_lint("点击链接（参赛号查询推文链接）")
        clean = run_lint("点击链接https://example.com/race/123")
        self.assertEqual(blocked["code"], 1)
        self.assertEqual(clean["code"], 0)

    def test_empty_and_structured_placeholders_are_blocked(self):
        for text in (
            "   ",
            "您好，{{name}}",
            "您好，${name}",
            "您好，{姓名}",
            "您好，您的参赛号是{参赛号}",
            "比赛时间（时间待确认）",
        ):
            with self.subTest(text=text):
                self.assertEqual(run_lint(text)["code"], 1)

    def test_broken_missing_and_bare_urls_are_blocked(self):
        for text in (
            "详情请点击https://查看详情。",
            "详情请点击https://[。",
            "详情请点击https://example.com:abc/race。",
            "详情请点击www.example.com查看。",
            "请访问example.com/race查看。",
            "详情请点击链接。",
        ):
            with self.subTest(text=text):
                self.assertEqual(run_lint(text)["code"], 1)

    def test_delimiter_order_is_checked(self):
        result = run_lint("【示例赛事】请于7:30到场）（。")
        rules = {item["rule"] for item in result["payload"]["issues"]}
        self.assertEqual(result["code"], 1)
        self.assertIn("unbalanced-delimiter", rules)

    def test_natural_language_pending_confirmation_is_not_placeholder(self):
        result = run_lint("【示例赛事】比赛是否延期待确认，请勿前往赛场。")
        rules = {item["rule"] for item in result["payload"]["issues"]}
        self.assertNotIn("unresolved-placeholder", rules)

    def test_stdin_redacts_sensitive_placeholder_contents(self):
        sensitive_sample = "【示例赛事】您好，{张三手机号13800138000}，请确认。"
        result = run_lint(sensitive_sample, use_stdin=True)
        rendered = json.dumps(result["payload"], ensure_ascii=False)
        self.assertEqual(result["code"], 1)
        self.assertNotIn("text", result["payload"])
        self.assertNotIn("张三", rendered)
        self.assertNotIn("13800138000", rendered)
        self.assertIn("未替换变量", rendered)

    def test_internal_lint_matrix_covers_advisories(self):
        insecure = LINT_SMS.lint("请访问http://example.com/race")
        rules = {item["rule"] for item in insecure["issues"]}
        self.assertIn("insecure-url", rules)
        self.assertIn("missing-sender-signature", rules)
        self.assertIn("missing-ending-punctuation", rules)
        self.assertTrue(LINT_SMS.valid_hostname("8.8.8.8"))
        self.assertFalse(LINT_SMS.valid_hostname("127.0.0.1"))
        self.assertFalse(LINT_SMS.valid_hostname("10.0.0.8"))
        self.assertFalse(LINT_SMS.valid_hostname("-bad.example.com"))
        self.assertTrue(LINT_SMS.valid_hostname("例子.测试"))
        self.assertEqual(LINT_SMS.redact_url("not a url"), "url://无有效域名/…")


if __name__ == "__main__":
    unittest.main()
