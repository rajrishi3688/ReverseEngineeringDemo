from __future__ import annotations

import json
import re
from typing import Any


def extract_json_candidate(text: str) -> str:
    fenced_match = re.search(r"```json\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def safe_json_loads(text: str, fallback: dict[str, Any]) -> dict[str, Any]:
    candidate = extract_json_candidate(text)
    try:
        parsed = json.loads(candidate)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    return fallback


def ensure_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def normalize_reverse_output(payload: dict[str, Any], system_name: str) -> dict[str, Any]:
    return {
        "system_name": payload.get("system_name") or system_name,
        "summary": payload.get("summary", ""),
        "fields": ensure_list(payload.get("fields")),
        "business_rules": ensure_list(payload.get("business_rules")),
        "country_specific_rules": ensure_list(payload.get("country_specific_rules")),
        "validations": ensure_list(payload.get("validations")),
        "calculations": ensure_list(payload.get("calculations")),
        "confidence": payload.get("confidence", {}),
        "source_files": ensure_list(payload.get("source_files")),
        "notes": ensure_list(payload.get("notes")),
    }


def normalize_system_output(payload: dict[str, Any], system_name: str) -> dict[str, Any]:
    normalized = normalize_reverse_output(payload, system_name=system_name)
    normalized["transaction_flow"] = ensure_list(payload.get("transaction_flow"))
    normalized["entities"] = ensure_list(payload.get("entities"))
    normalized["integrations"] = ensure_list(payload.get("integrations"))
    normalized["persistence_model"] = ensure_list(payload.get("persistence_model"))
    normalized["audit_controls"] = ensure_list(payload.get("audit_controls"))
    normalized["exception_paths"] = ensure_list(payload.get("exception_paths"))
    return normalized


def normalize_gap_output(payload: dict[str, Any]) -> dict[str, Any]:
    confidence = payload.get("confidence", {})
    return {
        "missing_features": ensure_list(payload.get("missing_features")),
        "incorrect_implementations": ensure_list(payload.get("incorrect_implementations")),
        "compliance_gaps": ensure_list(payload.get("compliance_gaps")),
        "risks": ensure_list(payload.get("risks")),
        "rule_comparison": ensure_list(payload.get("rule_comparison")),
        "confidence": {
            "gap_confidence": confidence.get("gap_confidence", 0.0),
            "coverage_of_analysis": confidence.get("coverage_of_analysis", {}),
            "notes": ensure_list(confidence.get("notes")),
        },
    }
