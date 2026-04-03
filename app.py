from __future__ import annotations

from datetime import datetime
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


def render_table(items: Any, empty_message: str = "No data available.") -> None:
    dataframe = normalize_for_table(items)
    if dataframe.empty:
        st.info(empty_message)
        return
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
        "reverse_legacy": "Legacy reverse engineering",
        "collate_legacy": "Legacy collation",
        "reverse_target": "Target reverse engineering",
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

    summary_tab, fields_tab, rules_tab, country_tab, validations_tab, calculations_tab, notes_tab = st.tabs(
        ["Summary", "Fields", "Business Rules", "Country Rules", "Validations", "Calculations", "Notes"]
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


def render_step_outputs(result: dict) -> None:
    legacy_reverse_step, legacy_collate_step, target_reverse_step, target_collate_step, gap_step = st.tabs(
        ["Step 1: Legacy Reverse", "Step 2: Legacy Collate", "Step 3: Target Reverse", "Step 4: Target Collate", "Step 5: Gap Analysis"]
    )

    with legacy_reverse_step:
        render_spec(result.get("legacy_reverse_spec", {}), "Legacy Reverse Engineering Output")

    with legacy_collate_step:
        render_spec(result.get("legacy_spec", {}), "Legacy Consolidated Specification")

    with target_reverse_step:
        render_spec(result.get("target_reverse_spec", {}), "Target Reverse Engineering Output")

    with target_collate_step:
        render_spec(result.get("target_spec", {}), "Target Consolidated Specification")

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

    default_legacy = str(settings.sample_inputs_dir / "legacy")
    default_target = str(settings.sample_inputs_dir / "target")
    model_options = MODEL_OPTIONS if settings.model in MODEL_OPTIONS else [settings.model, *MODEL_OPTIONS]

    with st.sidebar:
        st.markdown("## Control Center")
        st.caption("Configure inputs, start the workflow, and review runtime settings.")
        st.markdown("### Inputs")
        legacy_folder = st.text_input("Legacy system folder", value=default_legacy)
        target_folder = st.text_input("Target system folder", value=default_target)
        selected_model = st.selectbox(
            "Model",
            options=model_options,
            index=model_options.index(settings.model),
        )
        cache_enabled = st.toggle("Caching", value=settings.cache_enabled)
        run_clicked = st.button("Run Modernization Analysis", type="primary", use_container_width=True)
        st.markdown("### Workflow")
        st.markdown("- Reverse legacy system")
        st.markdown("- Reverse target system")
        st.markdown("- Collate structured specs")
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
            progress_bar.progress(45, text="Reverse engineering legacy and target systems...")
            result = run_workflow(legacy_folder=legacy_folder, target_folder=target_folder)
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
        st.write("Use the sample folders or point the app at your own legacy and target system artifacts.")
        return

    render_phase_progress(result.get("logs", []))

    overview_tab, step_outputs_tab, legacy_tab, target_tab, comparison_tab, gap_tab, logs_tab, raw_tab = st.tabs(
        ["Overview", "Step Outputs", "Legacy Spec", "Target Spec", "Comparison", "Gap Analysis", "Execution Logs", "Raw JSON"]
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
