from __future__ import annotations

from config import settings
from utils.cache import AgentCache
from utils.llm import call_llm_json, load_prompt
from utils.parser import normalize_system_output, safe_json_loads


def run(system_name: str, code_reverse_spec: dict, sql_reverse_spec: dict, logger) -> dict:
    payload = {
        "system_name": system_name,
        "code_reverse_spec": code_reverse_spec,
        "sql_reverse_spec": sql_reverse_spec,
    }
    cache = AgentCache(settings.cache_dir)
    cache_key = f"collate_{system_name.lower().replace(' ', '_')}"

    if settings.cache_enabled:
        cached = cache.load(cache_key, payload)
        if cached:
            logger("collate", f"Cache hit for {system_name} collation.")
            return cached

    logger("collate", f"Collating reverse-engineered findings for {system_name}.")
    prompt = load_prompt(settings.prompts_dir / "collate_prompt.txt")
    raw = call_llm_json("collate", prompt, payload, require_live_call=not settings.cache_enabled)
    parsed = safe_json_loads(raw.get("raw_text", ""), fallback=raw)
    normalized = normalize_system_output(parsed, system_name=system_name)
    if settings.cache_enabled:
        cache.save(cache_key, payload, normalized)
    logger("collate", f"{system_name} collation complete.")
    return normalized
