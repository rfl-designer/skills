#!/usr/bin/env python3
"""Validate package metadata and portable local Markdown references."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicated metadata rather than silently taking the last value."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise ValueError(f"invalid or duplicated metadata key: {key!r}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def prose_only(text):
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, suffix = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not suffix.strip():
                fence = None
            continue
        if fence is None:
            lines.append(line)
    if fence:
        raise ValueError("unclosed Markdown code fence")
    return re.sub(r"`[^`\n]+`", "", "\n".join(lines))


def validate_package(root):
    root = Path(root).resolve()
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("no skills found")
    allowed = {"name", "description", "disable-model-invocation", "argument-hint",
               "metadata", "license", "allowed-tools"}
    for skill in skills:
        label = skill.relative_to(root)
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", skill.read_text(), re.S)
        if not match:
            errors.append(f"{label}: missing YAML frontmatter")
            continue
        try:
            meta = yaml.load(match[1], Loader=UniqueKeyLoader)
            if not isinstance(meta, dict):
                raise ValueError("frontmatter must be a mapping")
            if set(meta) - allowed:
                raise ValueError(f"unknown fields: {sorted(set(meta) - allowed)}")
            name = meta.get("name")
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                raise ValueError("invalid skill name")
            if name != skill.parent.name or len(name) > 64:
                raise ValueError("name must match directory and be at most 64 characters")
            description = meta.get("description")
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError("description must contain 1–1024 characters")
            if "disable-model-invocation" in meta and type(meta["disable-model-invocation"]) is not bool:
                raise ValueError("disable-model-invocation must be a boolean")
            if not skill.read_text()[match.end():].strip():
                raise ValueError("missing skill instructions")
        except (yaml.YAMLError, ValueError) as error:
            errors.append(f"{label}: {error}")

    documents = sorted(root.glob("*.md"))
    for directory in ("skills", "docs", "evals"):
        documents.extend(sorted((root / directory).rglob("*.md")))
    for document in documents:
        label = document.relative_to(root)
        try:
            prose = prose_only(document.read_text())
        except ValueError as error:
            errors.append(f"{label}: {error}")
            continue
        if re.search(r"\[TODO:[^\n]*\]", prose):
            errors.append(f"{label}: unfinished scaffold")
        # Inline Markdown links; code examples are deliberately excluded.
        for target in re.findall(r"\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)", prose):
            target = target.strip("<>")
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            linked = (document.parent / unquote(url.path)).resolve()
            if not linked.is_relative_to(root):
                errors.append(f"{label}: reference escapes package: {target}")
                continue
            if not linked.exists():
                errors.append(f"{label}: missing reference: {target}")
                continue
            # A single-skill install only carries the skill's own directory.
            if document.is_relative_to(root / "skills"):
                skill_root = root / "skills" / document.relative_to(root / "skills").parts[0]
                if not linked.is_relative_to(skill_root):
                    errors.append(f"{label}: non-portable skill reference: {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_package(args.root)
    for error in errors:
        print(error)
    if not errors:
        print("PASS: metadata, Markdown fences and local reference paths")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
