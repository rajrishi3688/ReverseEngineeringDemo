from __future__ import annotations

from config import settings
from utils.cache import AgentCache
from utils.llm import call_llm_json, load_prompt
from utils.parser import normalize_forward_engineering_output, safe_json_loads


def _cacheable_document_payload(document: dict) -> dict:
    if not isinstance(document, dict):
        return {}
    cacheable = dict(document)
    cacheable.pop("approval", None)
    return cacheable


def run(requirements: dict, technical_spec: dict, logger) -> dict:
    payload = {"requirements": requirements, "technical_spec": technical_spec}
    cache_payload = {
        "requirements": _cacheable_document_payload(requirements),
        "technical_spec": _cacheable_document_payload(technical_spec),
    }
    cache = AgentCache(settings.cache_dir)

    if settings.cache_enabled:
        cached = cache.load("forward_engineering", cache_payload)
        if cached:
            logger("forward_engineering", "Cache hit for forward engineering output.")
            return cached

    logger("forward_engineering", "Generating forward engineering artifacts from approved inputs.")
    prompt = load_prompt(settings.prompts_dir / "forward_engineering_prompt.txt")
    raw = call_llm_json("forward_engineering", prompt, payload, require_live_call=not settings.cache_enabled)
    parsed = safe_json_loads(raw.get("raw_text", ""), fallback=raw)
    normalized = normalize_forward_engineering_output(parsed)
    if settings.cache_enabled:
        cache.save("forward_engineering", cache_payload, normalized)
    logger("forward_engineering", "Forward engineering artifact generation complete.")
    return normalized
