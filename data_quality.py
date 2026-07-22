
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


@st.cache_data
def load_quality_data(data_folder):
    data_folder = Path(data_folder)

    findings = pd.read_csv(
        data_folder / "data_quality_findings.csv"
    )

    row_summary = pd.read_csv(
        data_folder / "row_count_summary.csv"
    )

    validation = pd.read_csv(
        data_folder / "post_cleaning_validation.csv"
    )

    decisions = (
        data_folder / "cleaning_decisions.txt"
    ).read_text(encoding="utf-8")

    return findings, row_summary, validation, decisions


def quality_card(title, value, note):
    st.markdown(
        f"""<div style="
        background:#fffaf3;
        border:1px solid #e5c79e;
        border-top:5px solid #c77828;
        border-radius:14px;
        padding:17px 19px;
        min-height:132px;
        box-shadow:0 4px 12px rgba(91,54,17,0.07);
        ">
        <div style="
        color:#71502f;
        font-size:13px;
        font-weight:800;
        margin-bottom:7px;
        ">{title}</div>
        <div style="
        color:#3d260f;
        font-size:28px;
        font-weight:900;
        margin-bottom:5px;
        ">{value}</div>
        <div style="
        color:#7a6855;
        font-size:12px;
        ">{note}</div>
        </div>""",
        unsafe_allow_html=True
    )


def style_quality_chart(figure, height=390):
    figure.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(
            family="Arial",
            color="#2f251b",
            size=13
        ),
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_color="#2f251b"
        )
    )

    figure.update_xaxes(
        showgrid=False,
        color="#2f251b",
        tickfont=dict(color="#2f251b"),
        title_font=dict(color="#2f251b")
    )

    figure.update_yaxes(
        gridcolor="#eadfce",
        color="#2f251b",
        tickfont=dict(color="#2f251b"),
        title_font=dict(color="#2f251b")
    )

    return figure


def render_data_quality(data_folder):
    st.markdown(
        """<style>
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stMultiSelect"] label p,
        div[data-testid="stWidgetLabel"],
        div[data-testid="stWidgetLabel"] p {
            color:#3d260f !important;
            -webkit-text-fill-color:#3d260f !important;
            opacity:1 !important;
            font-weight:800 !important;
        }
        </style>""",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="'
        'background:linear-gradient(120deg,#4b2a0e,#9b5d22);'
        'border-radius:20px;'
        'padding:38px 42px;'
        'margin-bottom:20px;'
        'box-shadow:0 12px 28px rgba(76,42,14,0.18);'
        '">'
        '<div style="'
        'color:#f4bd73;'
        'font-size:12px;'
        'font-weight:900;'
        'letter-spacing:1.5px;'
        'margin-bottom:12px;'
        '">DATA QUALITY & CLEANING LOG</div>'
        '<h1 style="color:white;margin:0 0 14px 0;">'
        'From raw data issues to validated information'
        '</h1>'
        '<p style="'
        'color:#fff4e6;'
        'font-size:16px;'
        'max-width:900px;'
        'margin:0;'
        '">'
        'This page documents issues detected in the original '
        'ArielLeaf files, the cleaning actions performed and '
        'the validation results after cleaning.'
        '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """<div style="
        background:#fff4e2;
        border-left:6px solid #c77828;
        border-radius:10px;
        padding:14px 18px;
        color:#4a321b;
        margin-bottom:18px;
        ">
        <b>Audit page:</b> The information below describes the
        original data and its cleaning process. It is not a
        business-performance analysis of the cleaned dataset.
        </div>""",
        unsafe_allow_html=True
    )

    findings, row_summary, validation, decisions = (
        load_quality_data(data_folder)
    )

    supplied_files = row_summary["File"].nunique()
    finding_rules = len(findings)
    reported_impacts = int(findings["AffectedRows"].sum())
    rows_removed = int(row_summary["RowsRemoved"].sum())
    passed_checks = int(
        validation["Status"].eq("PASS").sum()
    )
    total_checks = len(validation)

    card_columns = st.columns(5)

    cards = [
        (
            "Supplied CSV files",
            f"{supplied_files}",
            "Physical files audited"
        ),
        (
            "Documented findings",
            f"{finding_rules}",
            "File-column issue records"
        ),
        (
            "Reported impacts",
            f"{reported_impacts:,}",
            "May include overlapping rows"
        ),
        (
            "Rows removed",
            f"{rows_removed:,}",
            "Source rows preserved"
        ),
        (
            "Validation checks",
            f"{passed_checks}/{total_checks}",
            "All checks passed"
        )
    ]

    for column, card in zip(card_columns, cards):
        with column:
            quality_card(
                card[0],
                card[1],
                card[2]
            )

    st.markdown("## 1. Issues detected before cleaning")

    filter_col1, filter_col2 = st.columns(2)

    file_options = sorted(
        findings["File"].unique().tolist()
    )

    issue_options = sorted(
        findings["IssueType"].unique().tolist()
    )

    with filter_col1:
        selected_files = st.multiselect(
            "Filter by source file",
            options=file_options,
            default=file_options
        )

    with filter_col2:
        selected_issues = st.multiselect(
            "Filter by issue type",
            options=issue_options,
            default=issue_options
        )

    filtered_findings = findings[
        findings["File"].isin(selected_files)
        & findings["IssueType"].isin(selected_issues)
    ].copy()

    if filtered_findings.empty:
        st.warning(
            "No findings match the selected filters."
        )
    else:
        chart_column, explanation_column = st.columns(
            [1.45, 1]
        )

        issue_summary = (
            filtered_findings
            .groupby("IssueType", as_index=False)
            .agg(
                AffectedRows=("AffectedRows", "sum"),
                FindingRecords=("IssueType", "size")
            )
            .sort_values(
                "AffectedRows",
                ascending=True
            )
        )

        with chart_column:
            st.markdown(
                "### Reported impacts by issue type"
            )

            issue_figure = px.bar(
                issue_summary,
                x="AffectedRows",
                y="IssueType",
                orientation="h",
                color="AffectedRows",
                color_continuous_scale=[
                    "#f4d5aa",
                    "#d28a3b",
                    "#704016"
                ],
                labels={
                    "IssueType": "",
                    "AffectedRows": "Affected rows"
                }
            )

            issue_figure.update_layout(
                coloraxis_showscale=False
            )

            issue_figure.update_traces(
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Reported impacts: %{x:,.0f}"
                    "<extra></extra>"
                )
            )

            style_quality_chart(
                issue_figure,
                height=420
            )

            st.plotly_chart(
                issue_figure,
                use_container_width=True
            )

        with explanation_column:
            st.markdown(
                "### How to read this chart"
            )

            st.info(
                "Affected-row counts are reported for each "
                "quality rule. The same source row may appear "
                "in more than one finding, so totals must not "
                "be interpreted as unique customers or orders."
            )

            st.markdown(
                f"""
                **Visible finding records:**  
                {len(filtered_findings):,}

                **Visible reported impacts:**  
                {int(filtered_findings["AffectedRows"].sum()):,}

                **Issue types displayed:**  
                {filtered_findings["IssueType"].nunique():,}
                """
            )

        st.markdown(
            "### Complete findings and cleaning actions"
        )

        findings_display = filtered_findings.rename(
            columns={
                "File": "Source file",
                "Column": "Column",
                "IssueType": "Issue found",
                "AffectedRows": "Affected rows",
                "PlannedAction": "Cleaning action performed"
            }
        )

        st.dataframe(
            findings_display,
            use_container_width=True,
            hide_index=True,
            height=480
        )

    st.markdown("## 2. Rows before and after cleaning")

    total_before = int(
        row_summary["RowsBefore"].sum()
    )

    total_after = int(
        row_summary["RowsAfter"].sum()
    )

    summary_col1, summary_col2, summary_col3 = (
        st.columns(3)
    )

    with summary_col1:
        quality_card(
            "Rows before cleaning",
            f"{total_before:,}",
            "Across all physical CSV files"
        )

    with summary_col2:
        quality_card(
            "Rows after cleaning",
            f"{total_after:,}",
            "After all documented corrections"
        )

    with summary_col3:
        quality_card(
            "Net rows removed",
            f"{total_before - total_after:,}",
            "No source rows were deleted"
        )

    st.dataframe(
        row_summary,
        use_container_width=True,
        hide_index=True,
        height=420
    )

    st.markdown("## 3. Key cleaning decisions")

    decision_columns = st.columns(2)

    decision_notes = [
        (
            "Preserve source records",
            "No source rows were deleted. Recoverable values "
            "were corrected and unresolved values were flagged."
        ),
        (
            "Protect sensitive data",
            "The Password column was removed because it was "
            "irrelevant to analysis and contained sensitive data."
        ),
        (
            "Handle missing birth dates",
            "Twenty unresolved BirthDate values were preserved "
            "as missing and documented instead of being invented."
        ),
        (
            "Correct systematic order errors",
            "Inflated 2022 and 2023 detail values were corrected "
            "using the identified factors and reconciled to orders."
        )
    ]

    for index, decision in enumerate(decision_notes):
        with decision_columns[index % 2]:
            st.markdown(
                f"""<div style="
                background:#fffaf3;
                border:1px solid #e5c79e;
                border-left:6px solid #c77828;
                border-radius:12px;
                padding:15px 17px;
                margin-bottom:12px;
                color:#3d260f;
                min-height:116px;
                ">
                <b>{decision[0]}</b><br>
                {decision[1]}
                </div>""",
                unsafe_allow_html=True
            )

    with st.expander(
        "Open the complete cleaning-decisions record"
    ):
        st.text(decisions)

    st.markdown("## 4. Post-cleaning validation")

    validation_display = validation.copy()

    validation_display["Result"] = (
        validation_display["Status"].map(
            {
                "PASS": "✓ PASS",
                "FAIL": "✕ FAIL"
            }
        )
    )

    st.dataframe(
        validation_display[
            [
                "Check",
                "IssueCount",
                "Result"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    if validation["Status"].eq("PASS").all():
        st.success(
            "All post-cleaning validation checks passed. "
            "The cleaned files are ready for dashboard analysis."
        )
    else:
        st.error(
            "At least one validation check failed."
        )
