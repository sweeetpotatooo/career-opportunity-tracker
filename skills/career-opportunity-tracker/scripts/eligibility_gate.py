#!/usr/bin/env python3
"""Route source-backed eligibility checks; no scraping, scoring, or record writes."""
import argparse
import datetime
import json
import sys

DIMENSIONS = {"education", "experience", "availability", "location", "language",
              "required_skills", "application_restrictions", "personal_constraints"}
RESULTS = {"met", "unmet", "unknown", "not_stated"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def assess(data):
    if not isinstance(data, dict):
        raise ValueError("input must be an object")
    try:
        datetime.date.fromisoformat(data["checked_at"])
    except (KeyError, TypeError, ValueError):
        raise ValueError("checked_at must be an ISO date")
    posting = data.get("posting", {})
    if not isinstance(posting, dict) or posting.get("state") not in {"open", "closed", "unknown"}:
        raise ValueError("posting.state must be open, closed, or unknown")
    if not nonempty(posting.get("source")):
        raise ValueError("posting.source is required")
    checks = data.get("checks")
    if not isinstance(checks, list):
        raise ValueError("checks must be a list")
    seen, blockers, unknowns, exceptions = set(), [], [], []
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("each check must be an object")
        dimension = check.get("dimension")
        result = check.get("result")
        if dimension not in DIMENSIONS or result not in RESULTS:
            raise ValueError("invalid dimension or result")
        if type(check.get("required")) is not bool:
            raise ValueError("required must be a boolean")
        for field in ("requirement", "source"):
            if not nonempty(check.get(field)):
                raise ValueError(field + " is required for each check")
        if result in {"met", "unmet"}:
            for field in ("candidate_fact", "candidate_source"):
                if not nonempty(check.get(field)):
                    raise ValueError(field + " is required for met/unmet")
        exception = check.get("exception")
        if exception is not None:
            if (exception != "supplemental" or dimension != "experience"
                    or result != "unmet" or not check["required"]
                    or not nonempty(check.get("policy_source"))):
                raise ValueError("only an explicit experience exception can be supplemental")
        seen.add(dimension)
        issue = {"dimension": dimension, "requirement": check["requirement"],
                 "source": check["source"]}
        if check["required"]:
            if result == "unmet":
                (exceptions if exception else blockers).append(issue)
            elif result == "unknown":
                unknowns.append(issue)
    missing = sorted(DIMENSIONS - seen)
    if posting["state"] == "closed":
        route, label = "closed", "모집 마감"
    elif blockers:
        route, label = "excluded", "지원 불가"
    elif posting["state"] == "unknown" or missing or unknowns:
        route, label = "needs_confirmation", "조건 확인 필요"
    elif exceptions:
        route, label = "supplemental", "조건 차이"
    else:
        route, label = "primary_eligible", "확인된 조건 충족"
    return {"route": route, "label": label, "eligible_for_primary": route == "primary_eligible",
            "blockers": blockers, "unknowns": unknowns, "missing_dimensions": missing,
            "experience_exceptions": exceptions,
            "record_action": "preserve_existing_application_history"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="JSON file; omit to read stdin")
    args = parser.parse_args()
    try:
        if args.input:
            with open(args.input, encoding="utf-8") as handle:
                data = json.load(handle)
        else:
            data = json.load(sys.stdin)
        print(json.dumps(assess(data), ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
