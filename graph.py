from __future__ import annotations

from datetime import datetime, timezone
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agents import collate, gap, reverse_legacy, reverse_target


class AppState(TypedDict, total=False):
    legacy_folder: str
    target_folder: str
    legacy_reverse_spec: dict
    target_reverse_spec: dict
    legacy_spec: dict
    target_spec: dict
    collated_spec: dict
    gap_analysis: dict
    logs: list[dict]
    error: str


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_log(state: AppState, agent: str, message: str) -> None:
    state.setdefault("logs", []).append({"timestamp": _timestamp(), "agent": agent, "message": message})


def legacy_node(state: AppState) -> AppState:
    result = reverse_legacy.run(state["legacy_folder"], lambda a, m: append_log(state, a, m))
    return {"legacy_reverse_spec": result, "logs": state["logs"]}


def legacy_collate_node(state: AppState) -> AppState:
    result = collate.run("Legacy Insurance System", state["legacy_reverse_spec"], lambda _a, m: append_log(state, "collate_legacy", m))
    return {"legacy_spec": result, "logs": state["logs"]}


def target_node(state: AppState) -> AppState:
    result = reverse_target.run(state["target_folder"], lambda a, m: append_log(state, a, m))
    return {"target_reverse_spec": result, "logs": state["logs"]}


def target_collate_node(state: AppState) -> AppState:
    result = collate.run("Target Insurance System", state["target_reverse_spec"], lambda _a, m: append_log(state, "collate_target", m))
    return {
        "target_spec": result,
        "collated_spec": build_comparison_overview(state.get("legacy_spec", {}), result),
        "logs": state["logs"],
    }


def gap_node(state: AppState) -> AppState:
    result = gap.run(state["legacy_spec"], state["target_spec"], lambda a, m: append_log(state, a, m))
    return {"gap_analysis": result, "logs": state["logs"]}


def build_comparison_overview(legacy_spec: dict, target_spec: dict) -> dict:
    shared_domains: list[str] = []
    if legacy_spec.get("fields") and target_spec.get("fields"):
        shared_domains.append("quote data capture")
    if legacy_spec.get("validations") and target_spec.get("validations"):
        shared_domains.append("eligibility and validation")
    if legacy_spec.get("calculations") and target_spec.get("calculations"):
        shared_domains.append("pricing and risk processing")

    key_differences = []
    if legacy_spec.get("country_specific_rules") and not target_spec.get("country_specific_rules"):
        key_differences.append(
            {
                "category": "country_logic",
                "legacy_position": "Legacy specification contains country-specific rules.",
                "target_position": "Target specification does not contain equivalent country-specific logic.",
                "impact": "Regional and compliance parity is incomplete.",
            }
        )
    if len(legacy_spec.get("business_rules", [])) != len(target_spec.get("business_rules", [])):
        key_differences.append(
            {
                "category": "business_rules",
                "legacy_position": f"{len(legacy_spec.get('business_rules', []))} consolidated rules extracted.",
                "target_position": f"{len(target_spec.get('business_rules', []))} consolidated rules extracted.",
                "impact": "Rule coverage differs across systems.",
            }
        )

    modernization_focus_areas = [
        {"focus_area": "pricing parity", "rationale": "Validate calculation and sequencing consistency.", "priority": "high"},
        {"focus_area": "compliance parity", "rationale": "Reconcile consent, tax, and audit controls.", "priority": "high"},
    ]

    return {
        "shared_domains": shared_domains,
        "key_differences": key_differences,
        "modernization_focus_areas": modernization_focus_areas,
        "confidence": {"overview_confidence": 0.72},
    }


def build_graph():
    workflow = StateGraph(AppState)
    workflow.add_node("reverse_legacy", legacy_node)
    workflow.add_node("collate_legacy", legacy_collate_node)
    workflow.add_node("reverse_target", target_node)
    workflow.add_node("collate_target", target_collate_node)
    workflow.add_node("gap", gap_node)
    workflow.add_edge(START, "reverse_legacy")
    workflow.add_edge("reverse_legacy", "collate_legacy")
    workflow.add_edge("collate_legacy", "reverse_target")
    workflow.add_edge("reverse_target", "collate_target")
    workflow.add_edge("collate_target", "gap")
    workflow.add_edge("gap", END)
    return workflow.compile()


def run_workflow(legacy_folder: str, target_folder: str) -> AppState:
    graph = build_graph()
    initial_state: AppState = {
        "legacy_folder": legacy_folder,
        "target_folder": target_folder,
        "logs": [],
    }
    return graph.invoke(initial_state)
