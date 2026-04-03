from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class AgentCache:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, agent_name: str, payload: dict[str, Any]) -> Path:
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        return self.cache_dir / f"{agent_name}_{digest}.json"

    def load(self, agent_name: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        path = self._cache_path(agent_name, payload)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    def save(self, agent_name: str, payload: dict[str, Any], value: dict[str, Any]) -> dict[str, Any]:
        path = self._cache_path(agent_name, payload)
        path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
        return value
