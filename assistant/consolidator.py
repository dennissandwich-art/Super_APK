# assistant/consolidator.py
# BRANCH: main
# ROLE: AI Assistant data consolidation engine

"""
CONSOLIDATOR:
- Merge multiple data sources
- Resolve conflicts
- Create unified view
- Track provenance
"""

from typing import Dict, List, Any, Optional
import time


class DataConsolidator:
    """
    Data consolidation engine for AI Assistant.
    Merges and validates data from multiple sources.
    """

    def __init__(self):
        self._merge_strategies: Dict[str, callable] = {
            "newest": self._merge_newest,
            "oldest": self._merge_oldest,
            "all": self._merge_all,
            "priority": self._merge_priority
        }

    def consolidate(self, sources: List[Dict], strategy: str = "newest") -> Dict:
        """
        Consolidate multiple data sources.
        """
        if not sources:
            return {"status": "ok", "data": {}, "source_count": 0}

        # Validate sources
        valid_sources = [s for s in sources if self._validate_source(s)]

        if not valid_sources:
            return {"status": "error", "reason": "No valid sources"}

        # Apply merge strategy
        merge_fn = self._merge_strategies.get(strategy, self._merge_newest)
        merged = merge_fn(valid_sources)

        return {
            "status": "ok",
            "data": merged,
            "source_count": len(valid_sources),
            "strategy": strategy,
            "timestamp": int(time.time())
        }

    def consolidate_with_conflicts(self, sources: List[Dict]) -> Dict:
        """
        Consolidate and report conflicts.
        """
        conflicts = []
        merged = {}

        for source in sources:
            if not self._validate_source(source):
                continue

            data = source.get("data", {})
            for key, value in data.items():
                if key in merged and merged[key] != value:
                    conflicts.append({
                        "key": key,
                        "existing": merged[key],
                        "new": value,
                        "source": source.get("name", "unknown")
                    })
                merged[key] = value

        return {
            "status": "ok",
            "data": merged,
            "conflicts": conflicts,
            "conflict_count": len(conflicts)
        }

    def diff(self, source_a: Dict, source_b: Dict) -> Dict:
        """
        Compute difference between two sources.
        """
        data_a = source_a.get("data", {})
        data_b = source_b.get("data", {})

        added = {k: v for k, v in data_b.items() if k not in data_a}
        removed = {k: v for k, v in data_a.items() if k not in data_b}
        changed = {
            k: {"from": data_a[k], "to": data_b[k]}
            for k in data_a
            if k in data_b and data_a[k] != data_b[k]
        }

        return {
            "added": added,
            "removed": removed,
            "changed": changed
        }

    def _validate_source(self, source: Dict) -> bool:
        """Validate source has required fields."""
        if not isinstance(source, dict):
            return False
        return "data" in source or "content" in source

    def _merge_newest(self, sources: List[Dict]) -> Dict:
        """Merge keeping newest values."""
        # Sort by timestamp if available
        sorted_sources = sorted(
            sources,
            key=lambda s: s.get("timestamp", 0)
        )

        merged = {}
        for source in sorted_sources:
            data = source.get("data", source.get("content", {}))
            if isinstance(data, dict):
                merged.update(data)

        return merged

    def _merge_oldest(self, sources: List[Dict]) -> Dict:
        """Merge keeping oldest values."""
        sorted_sources = sorted(
            sources,
            key=lambda s: s.get("timestamp", 0),
            reverse=True
        )

        merged = {}
        for source in sorted_sources:
            data = source.get("data", source.get("content", {}))
            if isinstance(data, dict):
                merged.update(data)

        return merged

    def _merge_all(self, sources: List[Dict]) -> Dict:
        """Merge keeping all values as lists."""
        merged = {}
        for source in sources:
            data = source.get("data", source.get("content", {}))
            if isinstance(data, dict):
                for key, value in data.items():
                    if key not in merged:
                        merged[key] = []
                    merged[key].append(value)

        return merged

    def _merge_priority(self, sources: List[Dict]) -> Dict:
        """Merge by source priority."""
        sorted_sources = sorted(
            sources,
            key=lambda s: s.get("priority", 0),
            reverse=True
        )

        merged = {}
        for source in sorted_sources:
            data = source.get("data", source.get("content", {}))
            if isinstance(data, dict):
                for key, value in data.items():
                    if key not in merged:
                        merged[key] = value

        return merged
