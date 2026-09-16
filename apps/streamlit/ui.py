from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import streamlit as st

from apps.streamlit.styles import (
    compliance_banner_html,
    inject_styles,
    keywords_html,
    lead_candidate_html,
    page_header_html,
    runner_cards_html,
    score_pill_html,
    workflow_html,
)
from jdmatcher.constants import EXPERIENCE_LEVELS
from jdmatcher.models import ResumeEvaluation
from jdmatcher.services.evaluation import evaluate_resume
from jdmatcher.services.pdf import extract_pdf_text
from jdmatcher.services.reporting import format_full_text_report
from jdmatcher.settings import get_settings


def _init_session_state() -> None:
    defaults = {
        "results": [],
        "errors": [],
        "report_date": "",
        "evaluated_at": "",
        "run_experience_level": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


@st.cache_data(show_spinner=False)
def extract_pdf_cached(pdf_bytes: bytes) -> str:
    return extract_pdf_text(pdf_bytes)


def _load_jd_text(jd_input_method: str, jd_text: str, jd_file) -> str:
    if jd_input_method == "Text Input":
        return jd_text
    if not jd_file:
        return ""
    raw = jd_file.getvalue()
    if jd_file.name.lower().endswith(".pdf"):
        return extract_pdf_text(raw)
    return raw.decode(errors="replace")


def _evaluate_one(filename: str, pdf_bytes: bytes, jd_text: str, level: str):
    resume_text = extract_pdf_cached(pdf_bytes)
    if not resume_text:
        raise ValueError("Could not extract text from PDF.")
    return filename, evaluate_resume(resume_text, jd_text, level)


def _run_evaluation(resume_files, jd_text: str, experience_level: str):
    settings = get_settings()
    progress = st.progress(0, text="Processing candidate batch…")
    status = st.empty()
    results: list[tuple[str, ResumeEvaluation]] = []
    errors: list[str] = []

    with ThreadPoolExecutor(max_workers=settings.max_concurrent_evaluations) as pool:
        futures = {
            pool.submit(
                _evaluate_one,
                pdf_file.name,
                pdf_file.getvalue(),
                jd_text,
                experience_level,
            ): pdf_file.name
            for pdf_file in resume_files
        }
        completed = 0
        total = len(resume_files)
        for future in as_completed(futures):
            filename = futures[future]
            try:
                results.append(future.result())
                status.caption(f"Completed: **{filename}** ({completed + 1} of {total})")
            except Exception as exc:
                errors.append(f"**{filename}** — {exc}")
            completed += 1
            progress.progress(completed / total, text=f"Evaluating {completed} of {total}…")

    progress.empty()
    status.empty()
    results.sort(key=lambda item: item[1].ats_score, reverse=True)
    return results, errors


def _workflow_step() -> int:
    if st.session_state.get("results"):
        return 3
    return 1


def _header_status() -> tuple[str, str]:
    if st.session_state.get("results"):
        count = len(st.session_state["results"])
        return f"{count} candidate(s) ranked", "status-ready"
    return "Awaiting evaluation", "status-idle"


def _render_sidebar() -> str:
    with st.sidebar:
        st.markdown(
            """
<div class="logo-row">
  <span class="logo-mark">JM</span>
  <span class="logo-title">JD Matcher</span>
</div>
<p class="logo-sub">Enterprise resume screening workspace</p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="nav-label">Module</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="nav-item-active">Candidate screening</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="nav-label">Parameters</div>', unsafe_allow_html=True)
        experience_level = st.selectbox(
            "Experience band",
            EXPERIENCE_LEVELS,
            help="Calibrates seniority expectations in the match score.",
        )

        if st.session_state.get("evaluated_at"):
            st.markdown(
                f'<div class="sidebar-panel"><b>Last evaluation</b><br>'
                f'{st.session_state["evaluated_at"]}<br>'
                f'Band: {st.session_state.get("run_experience_level", "—")}</div>',
                unsafe_allow_html=True,
            )

        if st.session_state.get("results") and st.button(
            "Reset session", use_container_width=True
        ):
            for key in ("results", "errors", "report_date", "evaluated_at", "run_experience_level"):
                st.session_state[key] = [] if key in ("results", "errors") else ""
            st.rerun()

        st.markdown('<div class="nav-label">Process</div>', unsafe_allow_html=True)
        st.markdown(
            """
1. Submit job description  
2. Attach resume PDFs  
3. Execute batch scoring  
4. Export summary & reports  
            """
        )
    return experience_level


def _render_inputs(experience_level: str) -> None:
    st.markdown(
        """
<div class="section-head">
  <h2>Evaluation intake</h2>
  <p>Define the role and upload candidate resumes for batch ATS analysis.</p>
</div>
        """,
        unsafe_allow_html=True,
    )

    jd_col, resume_col = st.columns(2, gap="medium")

    with jd_col:
        with st.container(border=True):
            st.markdown("**Job description**")
            jd_input_method = st.radio(
                "Input mode",
                ["Text Input", "Upload File"],
                horizontal=True,
                label_visibility="collapsed",
            )
            if jd_input_method == "Text Input":
                jd_text_input = st.text_area(
                    "JD content",
                    height=200,
                    placeholder="Role summary, required skills, experience, certifications…",
                    label_visibility="collapsed",
                )
                jd_file = None
            else:
                jd_text_input = ""
                jd_file = st.file_uploader(
                    "JD file",
                    type=["txt", "pdf"],
                    help="Supported formats: plain text or PDF",
                )

    with resume_col:
        with st.container(border=True):
            st.markdown("**Candidate resumes**")
            resume_files = st.file_uploader(
                "Resume files",
                type=["pdf"],
                accept_multiple_files=True,
                label_visibility="collapsed",
                help=f"Maximum {get_settings().max_batch_resumes} files per batch",
            )
            if resume_files:
                st.caption(f"{len(resume_files)} document(s) queued")

    c1, c2, c3 = st.columns([1.2, 1, 1.2])
    with c2:
        evaluate = st.button(
            "Execute evaluation",
            type="primary",
            use_container_width=True,
        )

    if not evaluate:
        return

    jd_text = _load_jd_text(jd_input_method, jd_text_input, jd_file)
    if not jd_text.strip():
        st.error("Job description is required.")
        return
    if not resume_files:
        st.error("At least one resume PDF is required.")
        return
    if len(resume_files) > get_settings().max_batch_resumes:
        st.error(f"Batch limit exceeded ({get_settings().max_batch_resumes} resumes).")
        return

    with st.spinner("Running ATS and fit analysis…"):
        results, errors = _run_evaluation(resume_files, jd_text, experience_level)

    st.session_state["results"] = results
    st.session_state["errors"] = errors
    st.session_state["report_date"] = pd.Timestamp.now().strftime("%Y-%m-%d")
    st.session_state["evaluated_at"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    st.session_state["run_experience_level"] = experience_level


def _render_kpis(results: list[tuple[str, ResumeEvaluation]]) -> None:
    scores = [ev.ats_score for _, ev in results]
    avg = round(sum(scores) / len(scores), 1)
    strong = sum(1 for s in scores if s >= 75)
    review = sum(1 for s in scores if 50 <= s < 75)

    k1, k2, k3, k4 = st.columns(4, gap="small")
    k1.metric("Total evaluated", len(results))
    k2.metric("Strong match (≥75%)", strong)
    k3.metric("Review band (50–74%)", review)
    k4.metric("Mean match score", f"{avg}%")


def _render_results() -> None:
    results: list[tuple[str, ResumeEvaluation]] = st.session_state.get("results", [])
    errors: list[str] = st.session_state.get("errors", [])
    report_date: str = st.session_state.get("report_date", "")

    st.markdown(
        """
<div class="section-head">
  <h2>Screening results</h2>
  <p>Ranked candidates with exportable summary and per-applicant dossiers.</p>
</div>
        """,
        unsafe_allow_html=True,
    )

    if not results and not errors:
        st.markdown(
            """
<div class="empty-state">
  <h3>No screening data available</h3>
  <p>Submit a job description and resume batch, then execute evaluation to populate this dashboard.</p>
</div>
            """,
            unsafe_allow_html=True,
        )
        return

    for message in errors:
        st.error(message)

    if not results:
        st.warning("No resumes completed evaluation successfully.")
        return

    top_file, top_eval = results[0]
    st.markdown(
        lead_candidate_html(
            top_eval.name, top_eval.email, top_eval.ats_score, top_file
        ),
        unsafe_allow_html=True,
    )

    if len(results) > 1:
        runners = [
            (rank, ev.name, ev.ats_score, ev.email)
            for rank, (_, ev) in enumerate(results[1:4], start=2)
        ]
        st.markdown(runner_cards_html(runners), unsafe_allow_html=True)

    _render_kpis(results)

    filter_query = st.text_input(
        "Search roster",
        placeholder="Filter by candidate name or email…",
    ).strip().lower()

    rows = []
    for rank, (filename, evaluation) in enumerate(results, start=1):
        blob = f"{evaluation.name} {evaluation.email}".lower()
        if filter_query and filter_query not in blob:
            continue
        rows.append(
            {
                "Rank": rank,
                "Candidate": evaluation.name,
                "Match %": evaluation.ats_score,
                "Email": evaluation.email,
                "Source file": filename,
            }
        )

    if not rows:
        st.info("No candidates match the current filter.")
        return

    summary_df = pd.DataFrame(rows)
    st.dataframe(
        summary_df,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Match %": st.column_config.ProgressColumn(
                "Match",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
        },
        hide_index=True,
        use_container_width=True,
    )

    st.download_button(
        label="Export ranking (CSV)",
        data=summary_df.to_csv(index=False).encode("utf-8"),
        file_name="jd_matcher_ranking.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.markdown("**Candidate dossiers**")

    visible = [
        (rank, filename, evaluation)
        for rank, (filename, evaluation) in enumerate(results, start=1)
        if not filter_query
        or filter_query in f"{evaluation.name} {evaluation.email}".lower()
    ]

    for idx, (rank, filename, evaluation) in enumerate(visible):
        header = f"Rank {rank} — {evaluation.name} ({evaluation.ats_score}% match)"
        with st.expander(header, expanded=(idx == 0 and rank == 1)):
            st.markdown(score_pill_html(evaluation.ats_score), unsafe_allow_html=True)

            t1, t2, t3 = st.tabs(
                ["ATS assessment", "Hiring summary", "Skills & profile"]
            )
            with t1:
                st.markdown(evaluation.ats_report)
            with t2:
                st.markdown(evaluation.general_evaluation)
            with t3:
                a, b = st.columns(2)
                with a:
                    st.markdown("**Contact**")
                    st.text(evaluation.email)
                with b:
                    st.markdown("**Source document**")
                    st.text(filename)
                st.markdown("**Work style indicators (heuristic)**")
                st.info(evaluation.personality_profile or "Not available.")
                st.markdown("**Skill gaps vs. job description**")
                st.markdown(
                    keywords_html(evaluation.missing_keywords),
                    unsafe_allow_html=True,
                )

            st.download_button(
                label="Download dossier (.txt)",
                data=format_full_text_report(evaluation, filename, report_date),
                file_name=f"Dossier_{evaluation.name.replace(' ', '_')}.txt",
                mime="text/plain",
                key=f"dossier_{rank}_{idx}",
            )


def render() -> None:
    st.set_page_config(
        page_title="JD Matcher | Screening",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_session_state()
    inject_styles()

    experience_level = _render_sidebar()

    status_label, status_class = _header_status()
    st.markdown(
        page_header_html(
            "Resume screening dashboard",
            "Batch-evaluate applicants against a job description with ATS scoring and structured summaries.",
            status_label,
            status_class,
        )
        + compliance_banner_html()
        + workflow_html(_workflow_step()),
        unsafe_allow_html=True,
    )
    _render_inputs(experience_level)
    _render_results()

    st.markdown(
        '<div class="app-footer">JD Matcher · Internal talent acquisition tooling · '
        "Confidential candidate data</div>",
        unsafe_allow_html=True,
    )
