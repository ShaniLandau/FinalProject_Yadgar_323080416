
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


@st.cache_data
def load_overview_data(data_folder):
    data_folder = Path(data_folder)

    kpis = pd.read_csv(
        data_folder / "main_kpis_by_year.csv"
    )

    monthly = pd.read_csv(
        data_folder / "monthly_performance.csv"
    )

    categories = pd.read_csv(
        data_folder / "category_yearly_trend.csv"
    )

    monthly["YearMonth"] = monthly["YearMonth"].astype(str)

    monthly["Year"] = (
        monthly["YearMonth"]
        .str[:4]
        .astype(int)
    )

    return kpis, monthly, categories


def apply_chart_style(figure, height=390):
    figure.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#172033"
        ),
        legend_title_text="",
        hoverlabel=dict(bgcolor="white")
    )

    figure.update_xaxes(
        showgrid=False,
        color="#334155",
        tickfont=dict(
            color="#334155",
            size=12
        ),
        title_font=dict(
            color="#334155",
            size=13
        )
    )
    figure.update_yaxes(
        gridcolor="#dbe4ec",
        color="#334155",
        tickfont=dict(
            color="#334155",
            size=12
        ),
        title_font=dict(
            color="#334155",
            size=13
        )
    )

    return figure



def render_overview(data_folder):

    # תיקון צבעי הסלייסר וכרטיסי ה-KPI
    st.markdown(
        """
        <style>
        /* כותרת הסלייסר */
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] label p {
            color: #172033 !important;
            font-weight: 700 !important;
        }

        /* תיבת הבחירה */
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1px solid #cbd7e1 !important;
            color: #172033 !important;
        }

        div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
            color: #172033 !important;
        }

        /* כרטיסי KPI */
        div[data-testid="stMetric"] {
            background-color: #ffffff !important;
            border: 1px solid #dce5ec !important;
            border-radius: 14px !important;
            padding: 18px 20px !important;
            box-shadow: 0 4px 14px rgba(16, 35, 63, 0.06);
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] p {
            color: #536273 !important;
            font-weight: 700 !important;
        }

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] div {
            color: #10233f !important;
            font-weight: 800 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">EXECUTIVE OVERVIEW</div>
            <h1>Business performance at a glance</h1>
            <p>
                Track revenue, demand, customer activity and category
                performance across 2020–2023.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    kpis, monthly, categories = load_overview_data(
        data_folder
    )

    year_options = [
        "All",
        "2020",
        "2021",
        "2022",
        "2023"
    ]

    selected_year = st.selectbox(
        "Filter the entire page by year",
        options=year_options,
        index=0
    )

    selected_kpis = kpis[
        kpis["Year"].astype(str) == selected_year
    ].iloc[0]

    if selected_year == "All":
        monthly_filtered = monthly.copy()

        category_filtered = (
            categories
            .groupby("CategoryName", as_index=False)
            .agg(
                Revenue=("Revenue", "sum"),
                UnitsSold=("UnitsSold", "sum")
            )
        )
    else:
        selected_year_number = int(selected_year)

        monthly_filtered = monthly[
            monthly["Year"] == selected_year_number
        ].copy()

        category_filtered = categories[
            categories["Year"] == selected_year_number
        ].copy()

    # כרטיסי KPI בעיצוב עצמאי וברור
    kpi_cards = [
        (
            "Total Revenue",
            f"${selected_kpis['Revenue'] / 1_000_000:.2f}M"
        ),
        (
            "Total Orders",
            f"{int(selected_kpis['Orders']):,}"
        ),
        (
            "Active Customers",
            f"{int(selected_kpis['ActiveCustomers']):,}"
        ),
        (
            "Average Order Value",
            f"${selected_kpis['AverageOrderValue']:,.2f}"
        ),
        (
            "Units Sold",
            f"{int(selected_kpis['UnitsSold']):,}"
        ),
        (
            "Repeat Customer Rate",
            f"{selected_kpis['RepeatCustomerRate']:.1f}%"
        )
    ]

    first_row = st.columns(3)

    for column, card in zip(
        first_row,
        kpi_cards[:3]
    ):
        with column:
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #d7e2ea;
                    border-radius:14px;
                    padding:18px 20px;
                    margin-bottom:12px;
                    box-shadow:0 4px 14px rgba(16,35,63,0.06);
                ">
                    <div style="
                        color:#586779 !important;
                        font-size:14px;
                        font-weight:700;
                        margin-bottom:8px;
                    ">
                        {card[0]}
                    </div>
                    <div style="
                        color:#10233f !important;
                        font-size:29px;
                        line-height:1.1;
                        font-weight:800;
                    ">
                        {card[1]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    second_row = st.columns(3)

    for column, card in zip(
        second_row,
        kpi_cards[3:]
    ):
        with column:
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #d7e2ea;
                    border-radius:14px;
                    padding:18px 20px;
                    margin-bottom:18px;
                    box-shadow:0 4px 14px rgba(16,35,63,0.06);
                ">
                    <div style="
                        color:#586779 !important;
                        font-size:14px;
                        font-weight:700;
                        margin-bottom:8px;
                    ">
                        {card[0]}
                    </div>
                    <div style="
                        color:#10233f !important;
                        font-size:29px;
                        line-height:1.1;
                        font-weight:800;
                    ">
                        {card[1]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # DYNAMIC_TOOLTIP_BONUS
    monthly_filtered = (
        monthly_filtered
        .sort_values("YearMonth")
        .copy()
    )

    monthly_filtered["RevenueChangeDisplay"] = (
        monthly_filtered["Revenue"]
        .pct_change()
        .mul(100)
        .apply(
            lambda value:
                "First month in selection"
                if pd.isna(value)
                else f"{value:+.1f}%"
        )
    )

    st.caption(
        "Hover over any point to view the month's complete "
        "business profile."
    )

    st.markdown("### Revenue trend")

    trend_figure = px.area(
        monthly_filtered,
        x="YearMonth",
        y="Revenue",
        markers=True,
        color_discrete_sequence=["#277c78"],
        labels={
            "YearMonth": "Month",
            "Revenue": "Revenue"
        }
    )

    trend_figure.update_traces(
        line=dict(width=3),
        fillcolor="rgba(39, 124, 120, 0.16)",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: $%{y:,.0f}"
            "<extra></extra>"
        )
    )

    trend_figure.update_traces(
        customdata=monthly_filtered[[
            "Orders",
            "ActiveCustomers",
            "AverageOrderValue",
            "RevenueChangeDisplay"
        ]].to_numpy(),
        hovertemplate=(
            "<b>Month: %{x}</b><br>"
            "Revenue: $%{y:,.0f}<br>"
            "Change from previous month: %{customdata[3]}<br>"
            "Orders: %{customdata[0]:,.0f}<br>"
            "Active customers: %{customdata[1]:,.0f}<br>"
            "Average order value: $%{customdata[2]:,.2f}"
            "<extra></extra>"
        )
    )

    trend_figure.update_layout(
        hovermode="closest"
    )

    apply_chart_style(trend_figure, height=410)

    # TOOLTIP_CONTRAST_FIX
    trend_figure.update_layout(
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#277c78",
            font=dict(
                family="Arial",
                size=14,
                color="#10233f"
            )
        )
    )

    st.plotly_chart(
        trend_figure,
        use_container_width=True
    )

    left_column, right_column = st.columns(
        [1.35, 1]
    )

    with left_column:
        st.markdown("### Revenue by category")

        category_chart_data = (
            category_filtered
            .sort_values("Revenue", ascending=True)
        )

        category_figure = px.bar(
            category_chart_data,
            x="Revenue",
            y="CategoryName",
            orientation="h",
            color="Revenue",
            color_continuous_scale=[
                "#b9ddd8",
                "#277c78",
                "#10233f"
            ],
            labels={
                "CategoryName": "",
                "Revenue": "Revenue"
            }
        )

        category_figure.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: $%{x:,.0f}"
                "<extra></extra>"
            )
        )

        category_figure.update_layout(
            coloraxis_showscale=False
        )

        apply_chart_style(
            category_figure,
            height=410
        )

        st.plotly_chart(
            category_figure,
            use_container_width=True
        )

    with right_column:
        st.markdown("### Management insights")

        top_category_row = (
            category_filtered
            .sort_values("Revenue", ascending=False)
            .iloc[0]
        )

        category_total = category_filtered[
            "Revenue"
        ].sum()

        top_category_share = (
            top_category_row["Revenue"]
            / category_total
            * 100
        )

        if selected_year == "All":
            insight_1 = (
                "Revenue declined by 7.93% between "
                "2020 and 2023."
            )

            insight_2 = (
                "Average order value declined by 6.33% "
                "during the same period."
            )
        else:
            insight_1 = (
                f"Revenue in {selected_year} reached "
                f"${selected_kpis['Revenue'] / 1_000_000:.2f}M."
            )

            insight_2 = (
                f"The average order value in {selected_year} "
                f"was ${selected_kpis['AverageOrderValue']:,.2f}."
            )

        insight_3 = (
            f"{top_category_row['CategoryName']} is the "
            f"leading category with {top_category_share:.1f}% "
            "of selected revenue."
        )

        insight_4 = (
            f"The repeat customer rate is "
            f"{selected_kpis['RepeatCustomerRate']:.1f}%, "
            "indicating strong recurring demand."
        )

        insights = [
            insight_1,
            insight_2,
            insight_3,
            insight_4
        ]

        for number, insight in enumerate(
            insights,
            start=1
        ):
            st.markdown(
                f"""
                <div style="
                    background:white;
                    border:1px solid #dce5ec;
                    border-left:5px solid #277c78;
                    border-radius:12px;
                    padding:14px 16px;
                    margin-bottom:12px;
                    color:#172033;
                ">
                    <b>Insight {number}</b><br>
                    {insight}
                </div>
                """,
                unsafe_allow_html=True
            )
