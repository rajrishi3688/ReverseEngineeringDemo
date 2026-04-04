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
        {"timestamp": _timestamp(), "agent": "technical_spec", "message": message}
    )


def _cacheable_requirements_payload(requirements: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(requirements, dict):
        return {}
    cacheable = dict(requirements)
    cacheable.pop("approval", None)
    return cacheable


def _default_technical_spec_draft() -> dict[str, Any]:
    return {
        "document_type": "technical_spec_draft",
        "screen_name": "",
        "target_stack": {
            "frontend": "Angular",
            "backend": "Node.js",
            "database": "PostgreSQL",
        },
        "ui_design": [],
        "api_design": [],
        "service_design": [],
        "data_design": [],
        "rule_configuration_design": [],
        "validation_design": [],
        "security_and_compliance_design": [],
        "integration_design": [],
        "assumptions": [],
        "open_questions_for_architect": [],
        "review_notes": ["This is a draft pending architect validation."],
        "approval": {
            "status": "PENDING_ARCHITECT_APPROVAL",
            "required_reviewer_role": "Architect",
            "approved_by": "",
            "approved_on": "",
            "review_comments": "",
        },
    }


def _normalize_technical_spec_draft(payload: dict[str, Any]) -> dict[str, Any]:
    default = _default_technical_spec_draft()
    approval = payload.get("approval", {})
    target_stack = payload.get("target_stack", {})
    default.update(
        {
            "document_type": payload.get("document_type", default["document_type"]),
            "screen_name": payload.get("screen_name", ""),
            "target_stack": {
                "frontend": target_stack.get("frontend", "Angular"),
                "backend": target_stack.get("backend", "Node.js"),
                "database": target_stack.get("database", "PostgreSQL"),
            },
            "ui_design": ensure_list(payload.get("ui_design")),
            "api_design": ensure_list(payload.get("api_design")),
            "service_design": ensure_list(payload.get("service_design")),
            "data_design": ensure_list(payload.get("data_design")),
            "rule_configuration_design": ensure_list(payload.get("rule_configuration_design")),
            "validation_design": ensure_list(payload.get("validation_design")),
            "security_and_compliance_design": ensure_list(payload.get("security_and_compliance_design")),
            "integration_design": ensure_list(payload.get("integration_design")),
            "assumptions": ensure_list(payload.get("assumptions")),
            "open_questions_for_architect": ensure_list(payload.get("open_questions_for_architect")),
            "review_notes": ensure_list(payload.get("review_notes")) or default["review_notes"],
            "approval": {
                "status": approval.get("status", "PENDING_ARCHITECT_APPROVAL"),
                "required_reviewer_role": approval.get("required_reviewer_role", "Architect"),
                "approved_by": approval.get("approved_by", ""),
                "approved_on": approval.get("approved_on", ""),
                "review_comments": approval.get("review_comments", ""),
            },
        }
    )
    return default


def run(state: dict[str, Any]) -> dict[str, Any]:
    requirements = state.get("approved_requirements", state.get("requirements_draft", state.get("requirements", {})))
    payload = {"requirements": requirements}
    cache_payload = {"requirements": _cacheable_requirements_payload(requirements)}
    cache = AgentCache(settings.cache_dir)

    if settings.cache_enabled:
        cached = cache.load("technical_spec_draft", cache_payload)
        if cached:
            _append_log(state, "Cache hit for technical specification draft generation.")
            return {"technical_spec_draft": cached, "logs": state["logs"]}

    _append_log(state, "Generating draft technical specification for architect review.")
    prompt = load_prompt(settings.prompts_dir / "technical_spec_prompt.txt")
    raw = call_llm_json("technical_spec", prompt, payload, require_live_call=not settings.cache_enabled)
    parsed = safe_json_loads(raw.get("raw_text", ""), fallback=raw)
    normalized = _normalize_technical_spec_draft(parsed)

    if settings.cache_enabled:
        cache.save("technical_spec_draft", cache_payload, normalized)

    _append_log(state, "Technical specification draft generation complete.")
    return {"technical_spec_draft": normalized, "logs": state["logs"]}
