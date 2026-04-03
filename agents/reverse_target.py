from __future__ import annotations

from config import settings
from utils.cache import AgentCache
from utils.file_reader import read_folder
from utils.llm import call_llm_json, load_prompt
from utils.parser import normalize_reverse_output, safe_json_loads


def run(target_folder: str, logger) -> dict:
    logger("reverse_target", f"Reading target inputs from {target_folder}")
    folder_data = read_folder(
        target_folder,
        max_files=settings.max_files_per_folder,
        max_chars=settings.max_chars_per_file,
    )
    payload = {"system_name": "Target Insurance System", **folder_data}
    cache = AgentCache(settings.cache_dir)

    if settings.cache_enabled:
        cached = cache.load("reverse_target", payload)
        if cached:
            logger("reverse_target", "Cache hit for target reverse engineering.")
            return cached

    logger("reverse_target", "Calling LLM for target reverse engineering.")
    prompt = load_prompt(settings.prompts_dir / "reverse_prompt.txt")
    raw = call_llm_json("reverse_target", prompt, payload)
    parsed = safe_json_loads(raw.get("raw_text", ""), fallback=raw)
    normalized = normalize_reverse_output(parsed, system_name="Target Insurance System")
    normalized["read_errors"] = folder_data["errors"]
    if settings.cache_enabled:
        cache.save("reverse_target", payload, normalized)
    logger("reverse_target", "Target reverse engineering complete.")
    return normalized
