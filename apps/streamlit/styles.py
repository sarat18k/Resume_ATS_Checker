import html

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --brand-600: #1d4ed8;
    --brand-700: #1e40af;
    --surface: #f4f6f9;
    --surface-card: #ffffff;
    --border: #e5e7eb;
    --text: #111827;
    --text-muted: #6b7280;
    --sidebar-bg: #0b1220;
    --sidebar-border: #1f2937;
    --success: #047857;
    --warning: #b45309;
    --danger: #b91c1c;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--surface);
}

/*
  Clear Streamlit's fixed top header (~3.5rem). Too little padding overlaps content;
  too much leaves a large empty band above the dashboard card.
*/
.stApp [data-testid="stAppViewContainer"] [data-testid="stMain"] [data-testid="block-container"],
.stApp .main .block-container {
    padding-top: 4.25rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
    max-width: 1120px !important;
}

header[data-testid="stHeader"] {
    background: rgba(244, 246, 249, 0.96) !important;
    border-bottom: 1px solid var(--border);
    z-index: 999;
}

.main [data-testid="stMarkdownContainer"] {
    overflow: visible !important;
}
.main .stMarkdown {
    overflow: visible !important;
}

/* Tighter vertical rhythm in main content */
.main [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    gap: 0.65rem;
}
.main [data-testid="column"] {
    padding-left: 0.4rem !important;
    padding-right: 0.4rem !important;
}
.main [data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0.75rem 0.9rem !important;
}
.main .stTextArea textarea {
    min-height: 168px !important;
    max-height: 280px;
    font-size: 0.8125rem !important;
    line-height: 1.45 !important;
}
.main .stMarkdown h3, .main .stMarkdown h4, .main .stMarkdown h5 {
    font-size: 0.875rem !important;
    margin-bottom: 0.35rem !important;
}
.main hr {
    margin: 0.75rem 0 !important;
}

/* —— Sidebar (enterprise dark) —— */
section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--sidebar-border);
}
section[data-testid="stSidebar"] {
    min-width: 17rem !important;
    max-width: 17rem !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
    padding-left: 0.85rem;
    padding-right: 0.85rem;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
    font-size: 0.8125rem !important;
    line-height: 1.4 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    font-size: 0.8125rem !important;
    min-height: 2.1rem !important;
    padding: 0.35rem 0.75rem !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] hr {
    color: #cbd5e1 !important;
    border-color: #334155 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] strong {
    color: #f8fafc !important;
}
section[data-testid="stSidebar"] .stSelectbox label {
    color: #94a3b8 !important;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.logo-mark {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.75rem;
    height: 1.75rem;
    border-radius: 6px;
    background: var(--brand-600);
    color: #fff;
    font-weight: 700;
    font-size: 0.65rem;
    margin-right: 0.5rem;
    flex-shrink: 0;
}
.logo-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.15rem;
}
.logo-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.02em;
}
.logo-sub {
    font-size: 0.7rem;
    color: #94a3b8;
    margin: 0 0 0.85rem 0;
    line-height: 1.35;
}

.sidebar-panel {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 10px;
    padding: 0.75rem 0.85rem;
    margin-bottom: 1rem;
    font-size: 0.8rem;
    color: #cbd5e1;
    line-height: 1.45;
}
.sidebar-panel b { color: #f1f5f9; }

.nav-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #64748b;
    margin: 0.65rem 0 0.35rem 0;
}
.nav-item-active {
    background: rgba(29, 78, 216, 0.25);
    border: 1px solid rgba(59, 130, 246, 0.35);
    border-radius: 8px;
    padding: 0.45rem 0.6rem;
    color: #dbeafe !important;
    font-weight: 600;
    font-size: 0.8125rem;
    margin-bottom: 0.25rem;
}

/* —— Main header —— */
.page-header {
    background: var(--surface-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.85rem 1rem 0.75rem;
    margin: 0 0 0.55rem 0;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.page-header-main {
    flex: 1;
    min-width: 0;
}
.page-header h1 {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: var(--text);
    line-height: 1.25;
}
.breadcrumb {
    font-size: 0.6875rem;
    color: var(--text-muted);
    margin: 0.35rem 0 0 0;
    padding: 0;
    font-weight: 500;
    line-height: 1.3;
}
.page-desc {
    margin: 0.35rem 0 0 0;
    color: var(--text-muted);
    font-size: 0.8125rem;
    max-width: 34rem;
    line-height: 1.45;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.28rem 0.6rem;
    border-radius: 999px;
    font-size: 0.6875rem;
    font-weight: 600;
    white-space: nowrap;
    flex-shrink: 0;
    margin-top: 0.1rem;
}
@media (max-width: 768px) {
    .page-header {
        flex-direction: column;
        align-items: flex-start;
    }
    .status-badge { margin-top: 0.5rem; }
}
.status-idle {
    background: #f3f4f6;
    color: #374151;
    border: 1px solid #e5e7eb;
}
.status-ready {
    background: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
}
.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: currentColor;
}

.compliance-strip {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
    color: #92400e;
    margin-bottom: 0.65rem;
    line-height: 1.4;
}

.workflow {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.45rem;
    margin-bottom: 0.85rem;
}
@media (max-width: 768px) {
    .workflow { grid-template-columns: 1fr; }
}
.workflow-step {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 0.65rem;
    font-size: 0.75rem;
    color: var(--text-muted);
    line-height: 1.3;
}
.workflow-step.active {
    border-color: #93c5fd;
    background: #eff6ff;
    color: #1e40af;
    font-weight: 600;
}
.workflow-step.done {
    border-color: #bbf7d0;
    background: #f0fdf4;
    color: #166534;
}
.workflow-step span {
    display: block;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.2rem;
    opacity: 0.85;
}

.section-head {
    margin: 0.85rem 0 0.5rem 0;
}
.section-head h2 {
    margin: 0 0 0.15rem 0;
    font-size: 0.9375rem;
    font-weight: 700;
    color: var(--text);
}
.section-head p {
    margin: 0;
    font-size: 0.78rem;
    color: var(--text-muted);
    line-height: 1.35;
}

.lead-card {
    background: #fff;
    border: 1px solid var(--border);
    border-left: 3px solid var(--brand-600);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.65rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.lead-card-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
}
@media (max-width: 640px) {
    .lead-card-inner { flex-direction: column; align-items: flex-start; }
    .lead-score { text-align: left !important; }
}
.lead-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--brand-600);
    margin-bottom: 0.35rem;
}
.lead-name {
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0 0 0.15rem 0;
    color: var(--text);
    line-height: 1.25;
}
.lead-meta {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin: 0;
    line-height: 1.35;
    word-break: break-word;
}
.lead-score {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--brand-700);
    margin: 0;
    text-align: right;
    line-height: 1;
}

.runner-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin-bottom: 0.65rem;
}
@media (max-width: 900px) { .runner-grid { grid-template-columns: 1fr; } }
.runner-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.65rem 0.75rem;
}
.runner-card .rank {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.runner-card .name {
    font-weight: 600;
    font-size: 0.8125rem;
    margin: 0.15rem 0;
    color: var(--text);
    line-height: 1.25;
}
.runner-card .score {
    font-size: 1.125rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.1;
}
.score-high { color: var(--success); }
.score-mid { color: var(--warning); }
.score-low { color: var(--danger); }

.score-pill {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.78rem;
    border: 1px solid transparent;
}
.score-pill.high { background: #ecfdf5; color: #065f46; border-color: #a7f3d0; }
.score-pill.mid { background: #fffbeb; color: #92400e; border-color: #fde68a; }
.score-pill.low { background: #fef2f2; color: #991b1b; border-color: #fecaca; }

.kw-chip {
    display: inline-block;
    background: #f9fafb;
    color: #374151;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    margin: 0.2rem 0.25rem 0.2rem 0;
    font-size: 0.75rem;
    font-weight: 500;
}

.empty-state {
    background: #fff;
    border: 1px dashed #d1d5db;
    border-radius: 10px;
    padding: 1.75rem 1rem;
    text-align: center;
    margin-top: 0.35rem;
}
.empty-state h3 {
    margin: 0 0 0.25rem 0;
    font-size: 0.9rem;
    font-weight: 600;
}
.empty-state p {
    margin: 0;
    color: var(--text-muted);
    font-size: 0.8125rem;
}

.app-footer {
    margin-top: 1.25rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border);
    font-size: 0.6875rem;
    color: var(--text-muted);
    text-align: center;
}

div[data-testid="stMetric"] {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 0.65rem;
    min-height: 4.25rem;
}
div[data-testid="stMetric"] label {
    font-size: 0.625rem !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted) !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.125rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    line-height: 1.2 !important;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 0.6875rem !important;
}

.stButton > button {
    font-size: 0.8125rem !important;
    min-height: 2.25rem !important;
    padding: 0.4rem 0.85rem !important;
}
.stButton > button[kind="primary"] {
    background: var(--brand-600) !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
.stDownloadButton button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.8125rem !important;
    min-height: 2.15rem !important;
}

div[data-testid="stExpander"] {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 0.35rem;
}
details summary {
    font-size: 0.8125rem !important;
    padding-top: 0.45rem !important;
    padding-bottom: 0.45rem !important;
}

[data-testid="stDataFrame"] {
    font-size: 0.8125rem;
}

.main .stTextInput input {
    font-size: 0.8125rem !important;
    min-height: 2.1rem !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )


def _esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def page_header_html(title: str, subtitle: str, status: str, status_class: str) -> str:
    return f"""
<div class="page-header">
  <div class="page-header-main">
    <h1>{_esc(title)}</h1>
    <div class="breadcrumb">Talent Acquisition · Resume screening</div>
    <p class="page-desc">{_esc(subtitle)}</p>
  </div>
  <div class="status-badge {status_class}">
    <span class="status-dot"></span>{_esc(status)}
  </div>
</div>
"""


def compliance_banner_html() -> str:
    return """
<div class="compliance-strip">
  <strong>Compliance notice:</strong> Resume content is processed by OpenAI for analysis.
  Use only data you are authorized to share. AI-generated scores and personality notes are
  decision-support only—not sole grounds for hiring.
</div>
"""


def workflow_html(step: int) -> str:
    def cls(n: int) -> str:
        if step > n:
            return "workflow-step done"
        if step == n:
            return "workflow-step active"
        return "workflow-step"

    return f"""
<div class="workflow">
  <div class="{cls(1)}"><span>Step 1</span>Configure inputs</div>
  <div class="{cls(2)}"><span>Step 2</span>Run evaluation</div>
  <div class="{cls(3)}"><span>Step 3</span>Review & export</div>
</div>
"""


def score_pill_html(score: int) -> str:
    tier = "high" if score >= 75 else "mid" if score >= 50 else "low"
    label = "Strong match" if tier == "high" else "Moderate match" if tier == "mid" else "Low match"
    return f'<span class="score-pill {tier}">{score}% · {label}</span>'


def score_class(score: int) -> str:
    if score >= 75:
        return "high"
    if score >= 50:
        return "mid"
    return "low"


def keywords_html(keywords: str) -> str:
    parts = [part.strip() for part in keywords.split(",") if part.strip()]
    if not parts:
        return '<p style="color:#6b7280;margin:0;font-size:0.85rem;">No critical skill gaps identified.</p>'
    chips = "".join(f'<span class="kw-chip">{_esc(part)}</span>' for part in parts)
    return f'<div>{chips}</div>'


def lead_candidate_html(name: str, email: str, score: int, filename: str) -> str:
    return f"""
<div class="lead-card">
  <div class="lead-card-inner">
    <div>
      <div class="lead-label">Primary recommendation</div>
      <p class="lead-name">{_esc(name)}</p>
      <p class="lead-meta">{_esc(email)} · {_esc(filename)}</p>
    </div>
    <p class="lead-score">{score}%</p>
  </div>
</div>
"""


def runner_cards_html(items: list[tuple[int, str, int, str]]) -> str:
    cards = []
    for rank, name, score, email in items:
        cards.append(
            f"""
<div class="runner-card">
  <div class="rank">Rank {rank}</div>
  <p class="name">{_esc(name)}</p>
  <p class="score {score_class(score)}">{score}%</p>
  <p class="lead-meta">{_esc(email)}</p>
</div>
"""
        )
    return f'<div class="runner-grid">{"".join(cards)}</div>'
