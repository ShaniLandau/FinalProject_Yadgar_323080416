
import streamlit as st
import textwrap
import pandas as pd
import plotly.express as px
from pathlib import Path




# BONUS_RETURNS_STRONG_CHART_CONTRAST
def strengthen_returns_chart_contrast(figure):
    """Apply readable text and axis colors to Returns charts."""

    figure.update_layout(
        font=dict(
            family="Arial",
            size=14,
            color="#10233f"
        ),
        legend=dict(
            font=dict(
                size=13,
                color="#10233f"
            ),
            title_font=dict(
                size=13,
                color="#10233f"
            )
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#6f4b87",
            font=dict(
                size=14,
                color="#10233f"
            )
        )
    )

    figure.update_xaxes(
        tickfont=dict(
            size=12,
            color="#10233f"
        ),
        title_font=dict(
            size=13,
            color="#10233f"
        ),
        linecolor="#8795a8",
        gridcolor="#dce4ec",
        zerolinecolor="#8795a8"
    )

    figure.update_yaxes(
        tickfont=dict(
            size=12,
            color="#10233f"
        ),
        title_font=dict(
            size=13,
            color="#10233f"
        ),
        linecolor="#8795a8",
        gridcolor="#dce4ec",
        zerolinecolor="#8795a8"
    )

    for trace in figure.data:
        if getattr(trace, "type", "") == "pie":
            trace.update(
                insidetextfont=dict(
                    size=13,
                    color="white"
                ),
                outsidetextfont=dict(
                    size=13,
                    color="#10233f"
                )
            )

    return figure

@st.cache_data
def load_returns_data(data_folder):

    data_folder = Path(data_folder)

    returns = pd.read_csv(
        data_folder / "returns.csv"
    )

    category_summary = pd.read_csv(
        data_folder / "returns_by_category.csv"
    )

    customer_summary = pd.read_csv(
        data_folder / "returns_by_customer.csv"
    )

    reason_summary = pd.read_csv(
        data_folder / "returns_by_reason.csv"
    )

    returns["OrderDate"] = pd.to_datetime(
        returns["OrderDate"],
        errors="coerce"
    )

    returns["ReturnDate"] = pd.to_datetime(
        returns["ReturnDate"],
        errors="coerce"
    )

    returns["ReturnYear"] = (
        returns["ReturnDate"]
        .dt.year
    )

    returns["ReturnMonth"] = (
        returns["ReturnDate"]
        .dt.to_period("M")
        .astype(str)
    )

    return (
        returns,
        category_summary,
        customer_summary,
        reason_summary
    )


def style_returns_chart(figure, height=390):

    figure.update_layout(
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#172033"
        ),
        legend_title_text="",
        hoverlabel=dict(
            bgcolor="white"
        )
    )

    figure.update_xaxes(
        showgrid=False
    )

    figure.update_yaxes(
        gridcolor="#ece8f3"
    )

    return figure


def render_returns(data_folder):

    # RETURNS_PAGE_FINAL_CONTRAST
    st.markdown(
        """
        <style>
        /* טקסט הצירים, הערכים והמקרא בכל גרפי ההחזרות */
        [data-testid="stPlotlyChart"] svg text {
            fill: #10233f !important;
            color: #10233f !important;
            font-weight: 600 !important;
            opacity: 1 !important;
        }

        /* אחוזים בתוך גרף הדונאט */
        [data-testid="stPlotlyChart"] .pielayer .slicetext {
            fill: #ffffff !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }

        /* טקסט חלונית המידע */
        [data-testid="stPlotlyChart"] .hovertext text {
            fill: #10233f !important;
            font-weight: 600 !important;
            opacity: 1 !important;
        }

        /* כותרות וערכי KPI בעמוד */
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] *,
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] * {
            color: #10233f !important;
            opacity: 1 !important;
        }

        /* כותרות המסננים */
        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] * {
            color: #10233f !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.html(
        textwrap.dedent(
            """
        <style>
        .returns-hero {
            padding: 34px 38px;
            border-radius: 22px;
            margin-bottom: 18px;
            color: white;
            background:
                linear-gradient(
                    135deg,
                    #37234f 0%,
                    #68407d 58%,
                    #9b6a45 100%
                );
            box-shadow:
                0 16px 34px rgba(55, 35, 79, 0.18);
        }

        .returns-hero h1 {
            color: white;
            margin: 8px 0 12px 0;
        }

        .returns-hero p {
            color: #f7f1fb;
            max-width: 900px;
            font-size: 1.02rem;
        }

        .bonus-badge {
            display: inline-block;
            padding: 7px 14px;
            border: 1px solid #f1c27d;
            border-radius: 999px;
            color: #ffe0a8;
            font-weight: 800;
            letter-spacing: 1.2px;
            font-size: 0.76rem;
        }

        .simulation-note {
            padding: 13px 16px;
            margin: 4px 0 18px 0;
            border-left: 5px solid #8b5ea7;
            border-radius: 8px;
            background: #f4eef8;
            color: #3d2850;
        }

        .return-insight {
            min-height: 105px;
            padding: 16px;
            border: 1px solid #dbcce6;
            border-left: 5px solid #8b5ea7;
            border-radius: 12px;
            background: white;
            margin-bottom: 10px;
        }

        .return-insight strong {
            color: #503268;
        }
        </style>

        <div class="returns-hero">
            <div class="bonus-badge">
                BONUS ANALYTICS · SIMULATED RETURNS
            </div>

            <h1>Returns Intelligence</h1>

            <p>
                Identify return patterns by category, reason, customer
                and time to support product-quality and customer-service
                decisions.
            </p>
        </div>

        <div class="simulation-note">
            <strong>Data disclosure:</strong>
            The supplied dataset did not contain return transactions.
            This page uses a reproducible simulated returns table created
            solely for the course bonus. Original and cleaned source files
            were not modified.
        </div>
            """
        )
    )

    (
        returns,
        category_summary,
        customer_summary,
        reason_summary
    ) = load_returns_data(data_folder)

    category_options = sorted(
        returns["CategoryName"]
        .dropna()
        .unique()
        .tolist()
    )

    reason_options = sorted(
        returns["ReturnReason"]
        .dropna()
        .unique()
        .tolist()
    )

    year_options = sorted(
        returns["ReturnYear"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        selected_categories = st.multiselect(
            "Categories",
            options=category_options,
            default=category_options
        )

    with filter_col2:

        selected_reasons = st.multiselect(
            "Return reasons",
            options=reason_options,
            default=reason_options
        )

    with filter_col3:

        selected_years = st.multiselect(
            "Return years",
            options=year_options,
            default=year_options
        )

    filtered_returns = returns[
        returns["CategoryName"].isin(
            selected_categories
        )
        & returns["ReturnReason"].isin(
            selected_reasons
        )
        & returns["ReturnYear"].isin(
            selected_years
        )
    ].copy()

    if filtered_returns.empty:

        st.warning(
            "No return records match the selected filters."
        )

        return

    selected_category_summary = (
        category_summary[
            category_summary["CategoryName"].isin(
                selected_categories
            )
        ]
    )

    total_returns = len(filtered_returns)

    returned_units = int(
        filtered_returns["ReturnedQuantity"].sum()
    )

    return_amount = float(
        filtered_returns["ReturnAmount"].sum()
    )

    returning_customers = int(
        filtered_returns["UserID"].nunique()
    )

    average_refund = (
        return_amount / total_returns
        if total_returns
        else 0
    )

    selected_sales_lines = (
        selected_category_summary["SalesLines"].sum()
    )

    selected_return_lines = (
        selected_category_summary["ReturnLines"].sum()
    )

    return_line_rate = (
        selected_return_lines
        / selected_sales_lines
        * 100
        if selected_sales_lines
        else 0
    )

    kpi_row1 = st.columns(3)

    kpi_row1[0].metric(
        "Return Transactions",
        f"{total_returns:,}"
    )

    kpi_row1[1].metric(
        "Returned Units",
        f"{returned_units:,}"
    )

    kpi_row1[2].metric(
        "Return Amount",
        f"${return_amount / 1_000_000:.2f}M"
    )

    kpi_row2 = st.columns(3)

    kpi_row2[0].metric(
        "Returning Customers",
        f"{returning_customers:,}"
    )

    kpi_row2[1].metric(
        "Average Refund",
        f"${average_refund:,.2f}"
    )

    kpi_row2[2].metric(
        "Simulated Return-Line Rate",
        f"{return_line_rate:.2f}%"
    )

    filtered_monthly = (
        filtered_returns
        .groupby("ReturnMonth")
        .agg(
            ReturnAmount=("ReturnAmount", "sum"),
            ReturnTransactions=("ReturnID", "count")
        )
        .reset_index()
        .sort_values("ReturnMonth")
    )

    st.markdown("### Return amount over time")

    monthly_figure = px.area(
        filtered_monthly,
        x="ReturnMonth",
        y="ReturnAmount",
        markers=True,
        color_discrete_sequence=[
            "#76508f"
        ],
        labels={
            "ReturnMonth": "Return month",
            "ReturnAmount": "Return amount"
        }
    )

    monthly_figure.update_traces(
        line=dict(width=3),
        fillcolor="rgba(118, 80, 143, 0.17)",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Return amount: $%{y:,.0f}"
            "<extra></extra>"
        )
    )

    style_returns_chart(
        monthly_figure,
        height=390
    )

    monthly_figure = strengthen_returns_chart_contrast(monthly_figure)
    st.plotly_chart(
        monthly_figure,
        theme=None,
        use_container_width=True
    )

    chart_col1, chart_col2 = st.columns(
        [1.25, 1]
    )

    with chart_col1:

        st.markdown(
            "### Return amount by category"
        )

        category_filtered = (
            filtered_returns
            .groupby("CategoryName")
            .agg(
                ReturnAmount=("ReturnAmount", "sum")
            )
            .reset_index()
            .sort_values(
                "ReturnAmount",
                ascending=True
            )
        )

        category_figure = px.bar(
            category_filtered,
            x="ReturnAmount",
            y="CategoryName",
            orientation="h",
            color="ReturnAmount",
            color_continuous_scale=[
                "#d9c7e4",
                "#8b5ea7",
                "#3c244f"
            ],
            labels={
                "CategoryName": "",
                "ReturnAmount": "Return amount"
            }
        )

        category_figure.update_layout(
            coloraxis_showscale=False
        )

        category_figure.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Return amount: $%{x:,.0f}"
                "<extra></extra>"
            )
        )

        style_returns_chart(
            category_figure,
            height=390
        )

        category_figure = strengthen_returns_chart_contrast(category_figure)
        st.plotly_chart(
            category_figure,
            theme=None,
            use_container_width=True
        )

    with chart_col2:

        st.markdown(
            "### Why products were returned"
        )

        reason_filtered = (
            filtered_returns
            .groupby("ReturnReason")
            .agg(
                ReturnTransactions=(
                    "ReturnID",
                    "count"
                )
            )
            .reset_index()
        )

        reason_figure = px.pie(
            reason_filtered,
            names="ReturnReason",
            values="ReturnTransactions",
            hole=0.54,
            color_discrete_sequence=[
                "#342148",
                "#68407d",
                "#946aa6",
                "#c09acb",
                "#d5a566"
            ]
        )

        reason_figure.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Returns: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        style_returns_chart(
            reason_figure,
            height=390
        )

        reason_figure = strengthen_returns_chart_contrast(reason_figure)
        st.plotly_chart(
            reason_figure,
            theme=None,
            use_container_width=True
        )

    customer_filtered = (
        filtered_returns
        .groupby("UserID")
        .agg(
            ReturnTransactions=("ReturnID", "count"),
            ReturnedUnits=("ReturnedQuantity", "sum"),
            ReturnAmount=("ReturnAmount", "sum")
        )
        .reset_index()
        .merge(
            customer_summary[[
                "UserID",
                "FirstName",
                "LastName",
                "Country",
                "CustomerSales"
            ]],
            on="UserID",
            how="left"
        )
    )

    customer_filtered["ReturnAmountRatePct"] = (
        customer_filtered["ReturnAmount"]
        / customer_filtered["CustomerSales"]
        * 100
    ).round(2)

    customer_filtered["Customer"] = (
        customer_filtered["FirstName"]
        .fillna("")
        .astype(str)
        .str.strip()
        + " "
        + customer_filtered["LastName"]
        .fillna("")
        .astype(str)
        .str.strip()
    ).str.strip()

    top_n = st.slider(
        "Number of customers to display",
        min_value=5,
        max_value=20,
        value=10,
        step=1
    )

    top_customers = (
        customer_filtered
        .sort_values(
            "ReturnAmount",
            ascending=False
        )
        .head(top_n)
    )

    st.markdown(
        f"### Top {top_n} customers by return amount"
    )

    top_customer_figure = px.bar(
        top_customers.sort_values(
            "ReturnAmount",
            ascending=True
        ),
        x="ReturnAmount",
        y="Customer",
        orientation="h",
        color="ReturnAmount",
        color_continuous_scale=[
            "#d9c7e4",
            "#8b5ea7",
            "#3c244f"
        ],
        labels={
            "Customer": "",
            "ReturnAmount": "Return amount"
        }
    )

    top_customer_figure.update_layout(
        coloraxis_showscale=False
    )

    top_customer_figure.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Return amount: $%{x:,.0f}"
            "<extra></extra>"
        )
    )

    style_returns_chart(
        top_customer_figure,
        height=420
    )

    top_customer_figure = strengthen_returns_chart_contrast(top_customer_figure)
    st.plotly_chart(
        top_customer_figure,
        theme=None,
        use_container_width=True
    )

    top_category_row = (
        category_filtered
        .sort_values(
            "ReturnAmount",
            ascending=False
        )
        .iloc[0]
    )

    top_reason_row = (
        reason_filtered
        .sort_values(
            "ReturnTransactions",
            ascending=False
        )
        .iloc[0]
    )

    top_customer_row = (
        top_customers
        .sort_values(
            "ReturnAmount",
            ascending=False
        )
        .iloc[0]
    )

    top_category_share = (
        top_category_row["ReturnAmount"]
        / return_amount
        * 100
        if return_amount
        else 0
    )

    top_reason_share = (
        top_reason_row["ReturnTransactions"]
        / total_returns
        * 100
        if total_returns
        else 0
    )

    st.markdown("### Management insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.markdown(
            f"""
            <div class="return-insight">
                <strong>Concentration by category</strong><br>
                {top_category_row["CategoryName"]} generates
                {top_category_share:.1f}% of the selected return amount.
                Management should examine product expectations and
                quality signals in this category first.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="return-insight">
                <strong>Customer-service workload</strong><br>
                {returning_customers:,} customers generated
                {total_returns:,} return transactions, indicating the
                scale of service activity associated with refunds.
            </div>
            """,
            unsafe_allow_html=True
        )

    with insight_col2:

        st.markdown(
            f"""
            <div class="return-insight">
                <strong>Main reported reason</strong><br>
                "{top_reason_row["ReturnReason"]}" represents
                {top_reason_share:.1f}% of selected returns. This points
                to a specific area for product-page or fulfillment
                improvement.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="return-insight">
                <strong>Customer follow-up</strong><br>
                {top_customer_row["Customer"]} has the highest selected
                return amount at
                ${top_customer_row["ReturnAmount"]:,.2f}. The account
                should be reviewed in context before any action is taken.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Customer return details")

    display_table = (
        customer_filtered[[
            "UserID",
            "Customer",
            "Country",
            "ReturnTransactions",
            "ReturnedUnits",
            "ReturnAmount",
            "CustomerSales",
            "ReturnAmountRatePct"
        ]]
        .sort_values(
            "ReturnAmount",
            ascending=False
        )
        .head(100)
        .copy()
    )

    display_table.columns = [
        "Customer ID",
        "Customer",
        "Country",
        "Return transactions",
        "Returned units",
        "Return amount",
        "Customer sales",
        "Return amount rate (%)"
    ]

    st.dataframe(
        display_table,
        use_container_width=True,
        hide_index=True
    )

# RETURNS_CONTRAST_CALLS_APPLIED
