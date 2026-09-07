"""Validate the public, fully synthetic demonstration. It never reads .jobhunt/."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT / "synthetic-workspace"
REPOSITORY = ROOT.parent
SKILL = REPOSITORY / "japan-job-hunting"
sys.path.insert(0, str(SKILL / "scripts"))

from workspace import errors, read  # noqa: E402
from char_count import count  # noqa: E402


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(relative: str) -> dict:
    return read(WORKSPACE / relative)


def main() -> None:
    checks = 0
    facts = load("candidate/facts.json")
    profile = load("candidate/profile.json")
    preferences = load("candidate/preferences.json")
    application = load("applications/aonagi-backend-2027.json")
    company = load("companies/aonagi-software/company.json")

    for record in [facts, profile, preferences, application, company]:
        check(not errors(record), f"Invalid record: {record['id']}")
    checks += 5

    statuses = {fact["status"] for fact in facts["data"]["facts"]}
    check(statuses == {"USER_CONFIRMED"}, "Demo facts must be user-confirmed only")
    checks += 1
    check(application["data"]["status"] == "RESEARCHING", "Demo must not imply an application was submitted")
    checks += 1
    verify = {fact["verification_status"] for fact in company["data"]["facts"]}
    check(verify == {"NEEDS_VERIFICATION"}, "Unknown recruitment facts must not be presented as verified")
    checks += 1
    check(count("志望動機", "codepoints") == 4, "Japanese character counter regression")
    checks += 1

    scanned = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*") if path.is_file() and path.suffix in {".md", ".json", ".html", ".py"})
    forbidden = [r"C:\\\\Users\\", r"E:\\\\box\\", r"sk-[A-Za-z0-9_-]{12,}"]
    check(not any(re.search(pattern, scanned) for pattern in forbidden), "Synthetic demo contains a local path or token pattern")
    print(f"PASS: {checks} checks — synthetic demo only; no user workspace read")


if __name__ == "__main__":
    main()
