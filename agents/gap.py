from __future__ import annotations

from config import settings
from utils.cache import AgentCache
from utils.llm import call_llm_json, load_prompt
from utils.parser import normalize_gap_output, safe_json_loads


def run(legacy_spec: dict, target_spec: dict, logger) -> dict:
    payload = {"legacy_spec": legacy_spec, "target_spec": target_spec}
    cache = AgentCache(settings.cache_dir)

    if settings.cache_enabled:
        cached = cache.load("gap", payload)
        if cached:
            logger("gap", "Cache hit for gap analysis.")
            return cached

    logger("gap", "Performing gap analysis.")
    prompt = load_prompt(settings.prompts_dir / "gap_prompt.txt")
    raw = call_llm_json("gap", prompt, payload)
    parsed = safe_json_loads(raw.get("raw_text", ""), fallback=raw)
    normalized = normalize_gap_output(parsed)
    if settings.cache_enabled:
        cache.save("gap", payload, normalized)
    logger("gap", "Gap analysis complete.")
    return normalized
