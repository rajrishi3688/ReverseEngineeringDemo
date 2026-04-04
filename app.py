from __future__ import annotations

from datetime import datetime
import json
from typing import Any

import pandas as pd
import streamlit as st

from config import settings
from graph import run_workflow


st.set_page_config(
    page_title="AI Modernization Platform",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_OPTIONS = [
    "gpt-5.4-mini",
    "gpt-5.4",
    "gpt-5-mini",
    "gpt-5",
    "gpt-4o-mini",
    "claude-sonnet-4-20250514",
    "claude-opus-4-1-20250805",
]


def apply_enterprise_theme() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(11, 78, 140, 0.14), transparent 28%),
                linear-gradient(180deg, #f4f7fb 0%, #edf2f7 100%);
        }
        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #16263d 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        [data-testid="stSidebar"] * {
            color: #e5eef8;
        }
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] label {
            color: #e5eef8;
        }
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] textarea,
        [data-testid="stSidebar"] [data-baseweb="input"] input {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            background-color: #ffffff !important;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-baseweb="select"] span,
        [data-testid="stSidebar"] [data-baseweb="popover"] *,
        [data-testid="stSidebar"] [data-baseweb="base-input"],
        [data-testid="stSidebar"] [role="combobox"],
        [data-testid="stSidebar"] [role="listbox"],
        [data-testid="stSidebar"] [role="option"] {
            background-color: #ffffff !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] .stText,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stToggle label {
            color: #e5eef8 !important;
        }
        .hero-card, .panel-card, .metric-card, .gap-card {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 18px;
            box-shadow: 0 18px 38px rgba(15, 23, 42, 0.08);
        }
        .hero-card {
            padding: 1.5rem 1.75rem;
            min-height: 180px;
        }
        .panel-card {
            padding: 1.1rem 1.2rem;
        }
        .phase-card {
            height: 206px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .phase-title {
            min-height: 82px;
            display: flex;
            align-items: flex-start;
        }
        .metric-card {
            padding: 1rem 1.1rem;
        }
        .gap-card {
            padding: 1rem 1.15rem;
            height: 100%;
        }
        .eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.72rem;
            color: #0b4e8c;
            font-weight: 700;
        }
        .hero-title {
            font-size: 2.15rem;
            line-height: 1.05;
            margin: 0.35rem 0 0.55rem 0;
            color: #10233b;
            font-weight: 800;
        }
        .hero-copy, .muted-copy {
            color: #4b5d73;
            font-size: 0.98rem;
        }
        .section-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #10233b;
            margin-bottom: 0.65rem;
        }
        .status-chip {
            display: inline-block;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            background: transparent;
            color: #0b4e8c;
            font-size: 0.8rem;
            font-weight: 700;
            margin-right: 0.4rem;
            margin-bottom: 0.4rem;
        }
        .risk-high {
            border-left: 5px solid #c62828;
        }
        .risk-medium {
            border-left: 5px solid #ef6c00;
        }
        .risk-low {
            border-left: 5px solid #2e7d32;
        }
        .small-label {
            font-size: 0.78rem;
            color: #6b7c93;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.3rem;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #10233b;
            margin: 0;
        }
        .metric-subtle {
            color: #61758b;
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, subtle: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="small-label">{label}</div>
            <p class="metric-value">{value}</p>
            <div class="metric-subtle">{subtle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_bullets(items: list, empty_message: str) -> None:
    if items:
        for item in items:
            st.write(f"- {item}")
    else:
        st.write(empty_message)


def normalize_for_table(items: Any) -> pd.DataFrame:
    if isinstance(items, list):
        if not items:
            return pd.DataFrame()
        if all(isinstance(item, dict) for item in items):
            return pd.json_normalize(items, sep=".")
        return pd.DataFrame({"value": [str(item) for item in items]})
    if isinstance(items, dict):
        return pd.json_normalize(items, sep=".")
    if items in (None, ""):
        return pd.DataFrame()
    return pd.DataFrame({"value": [str(items)]})


def sanitize_dataframe_for_display(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe.empty:
        return dataframe

    def normalize_cell(value: Any) -> Any:
        if isinstance(value, list):
            return ", ".join(str(item) for item in value)
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        return value

    return dataframe.map(normalize_cell)


def build_nested_rows(items: list[dict], nested_key: str, parent_keys: list[str], child_prefix: str = "") -> list[dict]:
    rows: list[dict] = []
    for item in items:
        nested_items = item.get(nested_key, [])
        if not isinstance(nested_items, list):
            continue
        for nested_item in nested_items:
            row = {key: item.get(key) for key in parent_keys}
            if isinstance(nested_item, dict):
                for key, value in nested_item.items():
                    row[f"{child_prefix}{key}" if child_prefix else key] = value
            else:
                row[f"{child_prefix}value" if child_prefix else "value"] = nested_item
            rows.append(row)
    return rows


def render_table(items: Any, empty_message: str = "No data available.") -> None:
    dataframe = normalize_for_table(items)
    if dataframe.empty:
        st.info(empty_message)
        return
    dataframe = sanitize_dataframe_for_display(dataframe)
    st.dataframe(dataframe, use_container_width=True, hide_index=True)


def render_notes(items: list[Any]) -> None:
    if not items:
        st.info("No notes available.")
        return
    for item in items:
        st.markdown(
            f"""
            <div class="panel-card" style="margin-bottom: 0.7rem;">
                <div>{item}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_phase_progress(logs: list[dict]) -> None:
    phase_map = {
        "reverse_legacy": "Legacy code and SQL reverse engineering",
        "collate_legacy": "Legacy collation",
        "reverse_target": "Target code and SQL reverse engineering",
        "collate_target": "Target collation",
        "gap": "Gap analysis",
    }
    seen = {entry.get("agent") for entry in logs}
    completed = sum(1 for key in phase_map if key in seen)
    progress = completed / len(phase_map)
    st.progress(progress, text=f"Workflow completion: {int(progress * 100)}%")

    cols = st.columns(len(phase_map))
    for index, (agent, label) in enumerate(phase_map.items()):
        state = "Complete" if agent in seen else "Pending"
        cols[index].markdown(
            f"""
            <div class="panel-card phase-card">
                <div class="small-label">Phase {index + 1}</div>
                <div class="phase-title">
                    <div class="section-title">{label}</div>
                </div>
                <span class="status-chip">{state}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_spec(spec: dict, title: str) -> None:
    st.subheader(title)
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.write(spec.get("summary", "No summary available."))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fields", len(spec.get("fields", [])))
    col2.metric("Business Rules", len(spec.get("business_rules", [])))
    col3.metric("Validations", len(spec.get("validations", [])))
    col4.metric("Calculations", len(spec.get("calculations", [])))
    st.markdown("</div>", unsafe_allow_html=True)

    (
        summary_tab,
        fields_tab,
        rules_tab,
        country_tab,
        validations_tab,
        calculations_tab,
        structure_tab,
        notes_tab,
    ) = st.tabs(
        ["Summary", "Fields", "Business Rules", "Country Rules", "Validations", "Calculations", "Structure", "Notes"]
    )

    with summary_tab:
        st.markdown("**System Summary**")
        st.write(spec.get("summary", "No summary available."))
        st.markdown("**Confidence**")
        render_table(spec.get("confidence", {}), "No confidence metadata available.")
        st.markdown("**Source Files**")
        render_table(spec.get("source_files", []), "No source files recorded.")

    with fields_tab:
        render_table(spec.get("fields", []), "No fields extracted.")

    with rules_tab:
        render_table(spec.get("business_rules", []), "No business rules extracted.")

    with country_tab:
        render_table(spec.get("country_specific_rules", []), "No country-specific rules extracted.")

    with validations_tab:
        render_table(spec.get("validations", []), "No validations extracted.")

    with calculations_tab:
        render_table(spec.get("calculations", []), "No calculations extracted.")

    with structure_tab:
        st.markdown("**UI Components**")
        render_table(spec.get("ui_components", []), "No UI components extracted.")
        ui_control_rows = build_nested_rows(
            spec.get("ui_components", []),
            "controls",
            ["component_name", "component_type", "screen_or_route"],
            child_prefix="control_",
        )
        st.markdown("**UI Controls**")
        render_table(ui_control_rows, "No UI controls extracted.")
        st.markdown("**Classes**")
        render_table(spec.get("classes", []), "No classes extracted.")
        st.markdown("**Methods**")
        render_table(spec.get("methods", []), "No methods extracted.")
        method_parameter_rows = build_nested_rows(spec.get("methods", []), "parameters", ["owner", "method_name"], child_prefix="param_")
        st.markdown("**Method Parameters**")
        render_table(method_parameter_rows, "No method parameters extracted.")
        st.markdown("**Procedures**")
        render_table(spec.get("procedures", []), "No procedures extracted.")
        procedure_parameter_rows = build_nested_rows(
            spec.get("procedures", []),
            "parameters",
            ["procedure_name", "procedure_type"],
            child_prefix="param_",
        )
        st.markdown("**Procedure Parameters**")
        render_table(procedure_parameter_rows, "No procedure parameters extracted.")
        st.markdown("**Procedure Dependencies**")
        render_table(spec.get("procedure_dependencies", []), "No procedure dependencies extracted.")
        st.markdown("**Table Dependencies**")
        render_table(spec.get("table_dependencies", []), "No table dependencies extracted.")
        st.markdown("**API Endpoints**")
        render_table(spec.get("api_endpoints", []), "No API endpoints extracted.")
        if spec.get("source_breakdown"):
            st.markdown("**Source Breakdown**")
            render_table(spec.get("source_breakdown", {}), "No source breakdown available.")

    with notes_tab:
        render_notes(spec.get("notes", []))
        errors = spec.get("read_errors", [])
        if errors:
            st.warning("File read warnings")
            render_bullets(errors, "No file warnings.")


def render_gap(gap_analysis: dict) -> None:
    confidence = gap_analysis.get("confidence", {}).get("gap_confidence", 0.0)
    missing_features = gap_analysis.get("missing_features", [])
    incorrect_implementations = gap_analysis.get("incorrect_implementations", [])
    compliance_gaps = gap_analysis.get("compliance_gaps", [])
    risks = gap_analysis.get("risks", [])

    top1, top2, top3, top4 = st.columns(4)
    with top1:
        render_metric_card("Gap Confidence", f"{confidence:.0%}", "Model-estimated certainty")
    with top2:
        render_metric_card("Missing Features", str(len(missing_features)), "Expected legacy behavior absent")
    with top3:
        render_metric_card("Compliance Gaps", str(len(compliance_gaps)), "Privacy and regulatory gaps")
    with top4:
        render_metric_card("Implementation Issues", str(len(incorrect_implementations)), "Potential parity defects")

    summary_tab, comparison_tab, confidence_tab = st.tabs(["Gap Summary", "Rule Comparison", "Confidence"])

    with summary_tab:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="gap-card risk-medium">', unsafe_allow_html=True)
            st.markdown("**Missing Features**")
            render_bullets(missing_features, "No missing features detected.")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="gap-card risk-high">', unsafe_allow_html=True)
            st.markdown("**Compliance Gaps**")
            render_bullets(compliance_gaps, "No compliance gaps detected.")
            st.markdown("</div>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="gap-card risk-medium">', unsafe_allow_html=True)
            st.markdown("**Incorrect Implementations**")
            render_bullets(incorrect_implementations, "No incorrect implementations detected.")
            st.markdown("</div>", unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="gap-card risk-high">', unsafe_allow_html=True)
            st.markdown("**Risks**")
            if risks and all(isinstance(item, dict) for item in risks):
                render_table(risks, "No risks detected.")
            else:
                render_bullets(risks, "No risks detected.")
            st.markdown("</div>", unsafe_allow_html=True)

    with comparison_tab:
        comparison_df = normalize_for_table(gap_analysis.get("rule_comparison", []))
        if not comparison_df.empty and "confidence" in comparison_df.columns:
            comparison_df["confidence"] = comparison_df["confidence"].map(
                lambda value: f"{value:.0%}" if isinstance(value, (int, float)) else value
            )
        if comparison_df.empty:
            st.info("No rule comparison data available.")
        else:
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    with confidence_tab:
        render_table(gap_analysis.get("confidence", {}), "No confidence data available.")


def render_logs(logs: list[dict]) -> None:
    if not logs:
        st.info("No execution logs yet.")
        return

    log_df = pd.DataFrame(logs)
    if "timestamp" in log_df.columns:
        log_df["timestamp"] = pd.to_datetime(log_df["timestamp"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

    st.markdown("**Execution Timeline**")
    for entry in logs:
        ts = entry.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%H:%M:%S")
        except ValueError:
            pass
        st.markdown(
            f"""
            <div class="panel-card" style="margin-bottom: 0.7rem;">
                <div class="small-label">{ts} | {entry.get("agent", "system")}</div>
                <div>{entry.get("message", "")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Structured Log Table", expanded=False):
        st.dataframe(log_df, use_container_width=True, hide_index=True)


def render_flow_map(flow_map: dict, title: str) -> None:
    st.subheader(title)
    if not flow_map:
        st.info("No flow map available.")
        return

    nodes = flow_map.get("nodes", [])
    edges = flow_map.get("edges", [])
    if not nodes or not edges:
        st.info("No flow map nodes or edges available.")
        return

    dot_lines = [
        "digraph G {",
        'graph [rankdir=LR, pad="0.6", nodesep="0.7", ranksep="1.1", bgcolor="transparent"];',
        'node [shape=box, style="rounded,filled", fillcolor="#eef4fb", color="#6f94bf", fontname="Helvetica", fontsize="16", margin="0.25,0.18", penwidth="1.4"];',
        'edge [color="#4f6f96", fontname="Helvetica", fontsize="13", penwidth="1.2"];',
    ]
    for node in nodes:
        dot_lines.append(f'"{node.get("id", "")}" [label="{node.get("label", "")}"];')
    for edge in edges:
        dot_lines.append(f'"{edge.get("from", "")}" -> "{edge.get("to", "")}" [label="{edge.get("label", "")}"];')
    dot_lines.append("}")
    dot_graph = "\n".join(dot_lines)

    try:
        st.graphviz_chart(dot_graph, use_container_width=True)
    except Exception:
        st.code(dot_graph, language="dot")

    if flow_map.get("diagram_text"):
        st.caption(flow_map["diagram_text"])

    linear_flow = " -> ".join(node.get("label", "") for node in nodes if node.get("label"))
    if linear_flow:
        st.markdown("**Linear View**")
        st.code(linear_flow, language="text")

    node_tab, edge_tab = st.tabs(["Flow Nodes", "Flow Edges"])
    with node_tab:
        render_table(nodes, "No flow nodes available.")
    with edge_tab:
        render_table(edges, "No flow edges available.")


def render_step_outputs(result: dict) -> None:
    (
        legacy_code_reverse_step,
        legacy_sql_reverse_step,
        legacy_collate_step,
        target_code_reverse_step,
        target_sql_reverse_step,
        target_collate_step,
        gap_step,
    ) = st.tabs(
        [
            "Step 1: Legacy Code Reverse",
            "Step 2: Legacy SQL Reverse",
            "Step 3: Legacy Collate",
            "Step 4: Target Code Reverse",
            "Step 5: Target SQL Reverse",
            "Step 6: Target Collate",
            "Step 7: Gap Analysis",
        ]
    )

    with legacy_code_reverse_step:
        render_spec(result.get("legacy_code_reverse_spec", {}), "Legacy Source Code Reverse Engineering Output")

    with legacy_sql_reverse_step:
        render_spec(result.get("legacy_sql_reverse_spec", {}), "Legacy SQL Reverse Engineering Output")

    with legacy_collate_step:
        render_spec(result.get("legacy_spec", {}), "Legacy Consolidated Specification")
        render_flow_map(result.get("legacy_spec", {}).get("flow_map", {}), "Legacy Flow Map")

    with target_code_reverse_step:
        render_spec(result.get("target_code_reverse_spec", {}), "Target Source Code Reverse Engineering Output")

    with target_sql_reverse_step:
        render_spec(result.get("target_sql_reverse_spec", {}), "Target SQL Reverse Engineering Output")

    with target_collate_step:
        render_spec(result.get("target_spec", {}), "Target Consolidated Specification")
        render_flow_map(result.get("target_spec", {}).get("flow_map", {}), "Target Flow Map")

    with gap_step:
        render_gap(result.get("gap_analysis", {}))


def render_comparison(collated: dict, gap_analysis: dict) -> None:
    domains_tab, differences_tab, focus_tab, rules_tab = st.tabs(
        ["Shared Domains", "Key Differences", "Focus Areas", "Rule Comparison"]
    )

    with domains_tab:
        render_table(collated.get("shared_domains", []), "No shared domains available.")

    with differences_tab:
        render_table(collated.get("key_differences", []), "No key differences available.")

    with focus_tab:
        render_table(collated.get("modernization_focus_areas", []), "No focus areas available.")

    with rules_tab:
        render_table(gap_analysis.get("rule_comparison", []), "No rule comparison available.")


def main() -> None:
    apply_enterprise_theme()
    st.title("AI Modernization Platform")
    st.caption("Reverse engineer legacy and target insurance systems, collate structured specs, and highlight migration gaps.")

    default_legacy_code = str(settings.sample_inputs_dir / "legacy" / "quote_generation")
    default_legacy_sql = str(settings.sample_inputs_dir / "legacy" / "quote_generation" / "sql")
    default_target_code = str(settings.sample_inputs_dir / "target" / "quote_generation")
    default_target_sql = str(settings.sample_inputs_dir / "target" / "quote_generation" / "sql")
    model_options = MODEL_OPTIONS if settings.model in MODEL_OPTIONS else [settings.model, *MODEL_OPTIONS]

    with st.sidebar:
        st.markdown("## Control Center")
        st.caption("Configure inputs, start the workflow, and review runtime settings.")
        st.markdown("### Legacy Inputs")
        legacy_code_folder = st.text_input(
            "Legacy source code root",
            value=default_legacy_code,
            help="Point this to the legacy code root. The code reverse pass will read VB/VB.NET files and ignore SQL.",
        )
        legacy_sql_folder = st.text_input(
            "Legacy SQL folder",
            value=default_legacy_sql,
            help="Point this to the legacy SQL folder only.",
        )
        st.markdown("### Target Inputs")
        target_code_folder = st.text_input(
            "Target source code root",
            value=default_target_code,
            help="Point this to the target code root. The code reverse pass will read Angular/Node files and ignore SQL.",
        )
        target_sql_folder = st.text_input(
            "Target SQL folder",
            value=default_target_sql,
            help="Point this to the target SQL folder only.",
        )
        selected_model = st.selectbox(
            "Model",
            options=model_options,
            index=model_options.index(settings.model),
        )
        cache_enabled = st.toggle("Caching", value=settings.cache_enabled)
        run_clicked = st.button("Run Modernization Analysis", type="primary", use_container_width=True)
        st.markdown("### Workflow")
        st.markdown("- Reverse legacy source code")
        st.markdown("- Reverse legacy SQL")
        st.markdown("- Collate legacy canonical specification")
        st.markdown("- Reverse target source code")
        st.markdown("- Reverse target SQL")
        st.markdown("- Collate target canonical specification")
        st.markdown("- Build graphical flow maps")
        st.markdown("- Run gap and compliance analysis")
        if st.session_state.get("analysis_result"):
            st.success("Latest analysis is loaded in the workspace.")

    settings.model = selected_model
    settings.cache_enabled = cache_enabled

    intro_col, stat_col = st.columns([2, 1])
    with intro_col:
        st.markdown(
            """
            <div class="hero-card">
                <div class="eyebrow">Insurance Transformation Intelligence</div>
                <div class="hero-title">Enterprise modernization analysis for legacy-to-target migration.</div>
                <div class="hero-copy">
                    Analyze two sets of insurance artifacts, reverse engineer their behavior, and surface migration gaps,
                    compliance exposures, and implementation risk in a single executive-ready workspace.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with stat_col:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-title">Launch Ready</div>
                <div class="muted-copy">Sample folders are preloaded so the platform can be demonstrated immediately.</div>
                <div style="margin-top: 0.85rem;">
                    <span class="status-chip">Legacy VB.NET</span>
                    <span class="status-chip">Sybase SQL</span>
                    <span class="status-chip">Angular</span>
                    <span class="status-chip">Node.js</span>
                    <span class="status-chip">PostgreSQL</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if run_clicked:
        st.session_state.pop("analysis_error", None)
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        try:
            progress_bar = progress_placeholder.progress(0, text="Initializing modernization workflow...")
            status_placeholder.info("Preparing artifact discovery and analysis context.")
            progress_bar.progress(20, text="Loading source folders and building execution plan...")
            progress_bar.progress(45, text="Reverse engineering source code and SQL for both systems...")
            result = run_workflow(
                legacy_code_folder=legacy_code_folder,
                legacy_sql_folder=legacy_sql_folder,
                target_code_folder=target_code_folder,
                target_sql_folder=target_sql_folder,
            )
            progress_bar.progress(80, text="Formatting findings, confidence scores, and comparison outputs...")
            st.session_state["analysis_result"] = result
            progress_bar.progress(100, text="Analysis complete.")
            status_placeholder.success("Modernization analysis completed successfully.")
        except Exception as exc:
            st.session_state["analysis_error"] = str(exc)
            status_placeholder.error("Analysis failed. Review the error message below.")

    if st.session_state.get("analysis_error"):
        st.error(st.session_state["analysis_error"])

    result = st.session_state.get("analysis_result")
    if not result:
        st.markdown("### Ready to analyze")
        st.write("Use the sample folders or point the app at separate source-code and SQL folders for legacy and target systems.")
        return

    render_phase_progress(result.get("logs", []))

    overview_tab, step_outputs_tab, legacy_tab, target_tab, flow_tab, comparison_tab, gap_tab, logs_tab, raw_tab = st.tabs(
        ["Overview", "Step Outputs", "Legacy Spec", "Target Spec", "Flow Maps", "Comparison", "Gap Analysis", "Execution Logs", "Raw JSON"]
    )

    with overview_tab:
        gap_analysis = result.get("gap_analysis", {})
        collated = result.get("collated_spec", {})
        top1, top2, top3 = st.columns(3)
        with top1:
            render_metric_card("Missing Features", str(len(gap_analysis.get("missing_features", []))), "Feature parity shortfalls")
        with top2:
            render_metric_card("Compliance Gaps", str(len(gap_analysis.get("compliance_gaps", []))), "Regulatory exposures detected")
        with top3:
            render_metric_card("Gap Confidence", f"{gap_analysis.get('confidence', {}).get('gap_confidence', 0.0):.0%}", "Confidence in assessment quality")

        st.markdown("**Modernization Focus Areas**")
        render_table(collated.get("modernization_focus_areas", []), "No focus areas available.")
        st.markdown("**Key Differences**")
        render_table(collated.get("key_differences", []), "No key differences available.")

    with step_outputs_tab:
        render_step_outputs(result)

    with legacy_tab:
        render_spec(result.get("legacy_spec", {}), "Legacy Insurance System")

    with target_tab:
        render_spec(result.get("target_spec", {}), "Target Insurance System")

    with flow_tab:
        legacy_flow_tab, target_flow_tab = st.tabs(["Legacy Flow Map", "Target Flow Map"])
        with legacy_flow_tab:
            render_flow_map(result.get("legacy_spec", {}).get("flow_map", {}), "Legacy System Flow Map")
        with target_flow_tab:
            render_flow_map(result.get("target_spec", {}).get("flow_map", {}), "Target System Flow Map")

    with comparison_tab:
        render_comparison(result.get("collated_spec", {}), result.get("gap_analysis", {}))

    with gap_tab:
        render_gap(result.get("gap_analysis", {}))

    with logs_tab:
        render_logs(result.get("logs", []))

    with raw_tab:
        st.json(result, expanded=False)


if __name__ == "__main__":
    main()
