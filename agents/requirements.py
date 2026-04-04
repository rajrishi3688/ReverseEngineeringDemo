from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from config import settings
from utils.cache import AgentCache
from utils.llm import call_llm_json, load_prompt
from utils.parser import ensure_list, safe_json_loads


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_log(state: dict[str, Any], message: str) -> None:
    state.setdefault("logs", []).append(
        {"timestamp": _timestamp(), "agent": "requirements", "message": message}
    )


def _default_requirements_draft() -> dict[str, Any]:
    return {
        "document_type": "requirements_draft",
        "screen_name": "",
        "business_context": "",
        "functional_requirements": [],
        "non_functional_requirements": [],
        "compliance_requirements": [],
        "data_requirements": [],
        "ui_requirements": [],
        "api_requirements": [],
        "migration_requirements": [],
        "assumptions": [],
        "open_questions_for_sme": [],
        "review_notes": ["This is a draft pending SME validation."],
        "approval": {
            "status": "PENDING_SME_APPROVAL",
            "required_reviewer_role": "SME",
            "approved_by": "",
            "approved_on": "",
            "review_comments": "",
        },
    }


def _normalize_requirements_draft(payload: dict[str, Any]) -> dict[str, Any]:
    default = _default_requirements_draft()
    approval = payload.get("approval", {})
    default.update(
        {
            "document_type": payload.get("document_type", default["document_type"]),
            "screen_name": payload.get("screen_name", ""),
            "business_context": payload.get("business_context", ""),
            "functional_requirements": ensure_list(payload.get("functional_requirements")),
            "non_functional_requirements": ensure_list(payload.get("non_functional_requirements")),
            "compliance_requirements": ensure_list(payload.get("compliance_requirements")),
            "data_requirements": ensure_list(payload.get("data_requirements")),
            "ui_requirements": ensure_list(payload.get("ui_requirements")),
            "api_requirements": ensure_list(payload.get("api_requirements")),
            "migration_requirements": ensure_list(payload.get("migration_requirements")),
            "assumptions": ensure_list(payload.get("assumptions")),
            "open_questions_for_sme": ensure_list(payload.get("open_questions_for_sme")),
            "review_notes": ensure_list(payload.get("review_notes")) or default["review_notes"],
            "approval": {
                "status": approval.get("status", "PENDING_SME_APPROVAL"),
                "required_reviewer_role": approval.get("required_reviewer_role", "SME"),
                "approved_by": approval.get("approved_by", ""),
                "approved_on": approval.get("approved_on", ""),
                "review_comments": approval.get("review_comments", ""),
            },
        }
    )
    return default


def run(state: dict[str, Any]) -> dict[str, Any]:
    legacy_spec = state.get("legacy_spec", {})
    target_spec = state.get("target_spec", {})
    gap = state.get("gap", state.get("gap_analysis", {}))
    payload = {"legacy": legacy_spec, "target": target_spec, "gap": gap}
    cache = AgentCache(settings.cache_dir)

    if settings.cache_enabled:
        cached = cache.load("requirements_draft", payload)
        if cached:
            _append_log(state, "Cache hit for requirements draft generation.")
            return {"requirements_draft": cached, "logs": state["logs"]}

    _append_log(state, "Generating draft requirements document for SME review.")
    prompt = load_prompt(settings.prompts_dir / "requirements_prompt.txt")
    raw = call_llm_json("requirements", prompt, payload, require_live_call=not settings.cache_enabled)
    parsed = safe_json_loads(raw.get("raw_text", ""), fallback=raw)
    normalized = _normalize_requirements_draft(parsed)

    if settings.cache_enabled:
        cache.save("requirements_draft", payload, normalized)

    _append_log(state, "Requirements draft generation complete.")
    return {"requirements_draft": normalized, "logs": state["logs"]}
