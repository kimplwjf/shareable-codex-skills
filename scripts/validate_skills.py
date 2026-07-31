#!/usr/bin/env python3
"""Validate the public skill package without third-party Python dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")


def yaml_value(content: str, key: str) -> str | None:
    match = re.search(rf"^  {re.escape(key)}: \"([^\"]+)\"$", content, re.MULTILINE)
    return match.group(1) if match else None


def validate_skill(skill_dir: Path, versions: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    version_file = skill_dir / "VERSION"
    metadata_file = skill_dir / "agents" / "openai.yaml"
    if not skill_file.is_file() or not version_file.is_file() or not metadata_file.is_file():
        return [f"{skill_dir.name}: 缺少 SKILL.md、VERSION 或 agents/openai.yaml"]

    content = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: [^\n]+\n---\n", content)
    if not match or match.group(1) != skill_dir.name:
        errors.append(f"{skill_dir.name}: SKILL.md frontmatter 名称不匹配")
    for reference in re.findall(r"references/[A-Za-z0-9_./-]+", content):
        if not (skill_dir / reference).is_file():
            errors.append(f"{skill_dir.name}: 缺少引用资源 {reference}")

    version = version_file.read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version) or versions.get(skill_dir.name, {}).get("version") != version:
        errors.append(f"{skill_dir.name}: VERSION 与 skill-versions.json 不一致或不是语义化版本")

    metadata = metadata_file.read_text(encoding="utf-8")
    short_description = yaml_value(metadata, "short_description")
    if not yaml_value(metadata, "display_name") or not yaml_value(metadata, "default_prompt"):
        errors.append(f"{skill_dir.name}: agents/openai.yaml 缺少界面字段")
    elif short_description is None or not 25 <= len(short_description) <= 64:
        errors.append(f"{skill_dir.name}: short_description 必须为 25–64 个字符")
    return errors


def main() -> int:
    manifest = json.loads((ROOT / "skill-versions.json").read_text(encoding="utf-8"))
    versions = manifest.get("skills", {})
    errors = [error for directory in sorted((ROOT / "skills").iterdir()) if directory.is_dir()
              for error in validate_skill(directory, versions)]
    if errors:
        print("\n".join(errors))
        return 1
    print("所有公开 skill 的结构、版本和界面元数据均有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
