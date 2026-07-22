
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


@st.cache_data
def load_customer_data(data_folder):
    data_folder = Path(data_folder)

    customers = pd.read_csv(
        data_folder / "customer_analysis.csv"
    )

    text_columns = [
        "Country",
        "Continent",
        "AgeGroup",
        "IncomeGroup"
    ]

    for column in text_columns:
        if column in customers.columns:
            customers[column] = (
                customers[column]
                .fillna("Unknown")
                .astype(str)
            )

    return customers


def style_customer_chart(figure, height=390):
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


def customer_card(title, value):
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
                {title}
            </div>
            <div style="
                color:#10233f !important;
                font-size:29px;
                line-height:1.1;
                font-weight:800;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



def render_customers(data_folder):

    # צבע ברור לכותרות הפילטרים
    st.markdown(
        """
        <style>
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stMultiSelect"] label p,
        div[data-testid="stSlider"] label,
        div[data-testid="stSlider"] label p,
        div[data-testid="stWidgetLabel"],
        div[data-testid="stWidgetLabel"] p {
            color: #172033 !important;
            -webkit-text-fill-color: #172033 !important;
            opacity: 1 !important;
            font-weight: 800 !important;
            font-size: 14px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">CUSTOMER INTELLIGENCE</div>
            <h1>Understand who creates business value</h1>
            <p>
                Explore customer value, purchasing behavior,
                demographics and geographic performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    customers = load_customer_data(data_folder)

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    continent_options = sorted(
        customers["Continent"].unique().tolist()
    )

    income_options = sorted(
        customers["IncomeGroup"].unique().tolist()
    )

    with filter_col1:
        selected_continents = st.multiselect(
            "Continent",
            options=continent_options,
            default=continent_options
        )

    with filter_col2:
        selected_income_groups = st.multiselect(
            "Income group",
            options=income_options,
            default=income_options
        )

    with filter_col3:
        top_n = st.slider(
            "Number of leading customers",
            min_value=5,
            max_value=20,
            value=10,
            step=1
        )

    filtered = customers[
        customers["Continent"].isin(selected_continents)
        & customers["IncomeGroup"].isin(selected_income_groups)
    ].copy()

    if filtered.empty:
        st.warning(
            "No customers match the selected filters."
        )
        return

    total_customers = filtered["UserID"].nunique()
    total_revenue = filtered["CustomerRevenue"].sum()
    total_orders = filtered["CustomerOrders"].sum()

    average_revenue_customer = (
        total_revenue / total_customers
    )

    average_orders_customer = (
        total_orders / total_customers
    )

    repeat_rate = (
        filtered["CustomerOrders"].gt(1).mean()
        * 100
    )

    cards = [
        (
            "Customers",
            f"{total_customers:,}"
        ),
        (
            "Customer Revenue",
            f"${total_revenue / 1_000_000:.2f}M"
        ),
        (
            "Revenue per Customer",
            f"${average_revenue_customer:,.2f}"
        ),
        (
            "Orders per Customer",
            f"{average_orders_customer:.2f}"
        ),
        (
            "Repeat Customer Rate",
            f"{repeat_rate:.1f}%"
        ),
        (
            "Units Purchased",
            f"{int(filtered['CustomerUnits'].sum()):,}"
        )
    ]

    first_row = st.columns(3)

    for column, card in zip(
        first_row,
        cards[:3]
    ):
        with column:
            customer_card(card[0], card[1])

    second_row = st.columns(3)

    for column, card in zip(
        second_row,
        cards[3:]
    ):
        with column:
            customer_card(card[0], card[1])

    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.markdown("### Revenue by age group")

        age_order = [
            "18-24",
            "25-34",
            "35-44",
            "45-54",
            "55+",
            "Unknown"
        ]

        age_summary = (
            filtered
            .groupby("AgeGroup", as_index=False)
            .agg(
                Revenue=("CustomerRevenue", "sum"),
                Customers=("UserID", "nunique")
            )
        )

        age_summary["AgeGroup"] = pd.Categorical(
            age_summary["AgeGroup"],
            categories=age_order,
            ordered=True
        )

        age_summary = age_summary.sort_values(
            "AgeGroup"
        )

        age_figure = px.bar(
            age_summary,
            x="AgeGroup",
            y="Revenue",
            color="Revenue",
            color_continuous_scale=[
                "#b9ddd8",
                "#277c78",
                "#10233f"
            ],
            labels={
                "AgeGroup": "Age group",
                "Revenue": "Revenue"
            }
        )

        age_figure.update_layout(
            coloraxis_showscale=False
        )

        age_figure.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: $%{y:,.0f}"
                "<extra></extra>"
            )
        )

        style_customer_chart(
            age_figure,
            height=390
        )

        st.plotly_chart(
            age_figure,
            use_container_width=True
        )

    with right_chart:
        st.markdown("### Revenue by income group")

        income_summary = (
            filtered
            .groupby("IncomeGroup", as_index=False)
            .agg(
                Revenue=("CustomerRevenue", "sum"),
                Customers=("UserID", "nunique")
            )
            .sort_values(
                "Revenue",
                ascending=True
            )
        )

        income_figure = px.bar(
            income_summary,
            x="Revenue",
            y="IncomeGroup",
            orientation="h",
            color="Revenue",
            color_continuous_scale=[
                "#b9ddd8",
                "#277c78",
                "#10233f"
            ],
            labels={
                "IncomeGroup": "",
                "Revenue": "Revenue"
            }
        )

        income_figure.update_layout(
            coloraxis_showscale=False
        )

        income_figure.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: $%{x:,.0f}"
                "<extra></extra>"
            )
        )

        style_customer_chart(
            income_figure,
            height=390
        )

        st.plotly_chart(
            income_figure,
            use_container_width=True
        )

    country_column, insights_column = st.columns(
        [1.35, 1]
    )

    country_summary = (
        filtered
        .groupby("Country", as_index=False)
        .agg(
            Revenue=("CustomerRevenue", "sum"),
            Customers=("UserID", "nunique")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    with country_column:
        st.markdown("### Top countries by revenue")

        country_figure = px.bar(
            country_summary.sort_values(
                "Revenue",
                ascending=True
            ),
            x="Revenue",
            y="Country",
            orientation="h",
            color_discrete_sequence=["#277c78"],
            labels={
                "Country": "",
                "Revenue": "Revenue"
            }
        )

        country_figure.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: $%{x:,.0f}"
                "<extra></extra>"
            )
        )

        style_customer_chart(
            country_figure,
            height=430
        )

        st.plotly_chart(
            country_figure,
            use_container_width=True
        )

    with insights_column:
        st.markdown("### Customer insights")

        top_age = (
            age_summary
            .sort_values(
                "Revenue",
                ascending=False
            )
            .iloc[0]
        )

        top_income = (
            income_summary
            .sort_values(
                "Revenue",
                ascending=False
            )
            .iloc[0]
        )

        top_country = country_summary.iloc[0]

        top_country_share = (
            top_country["Revenue"]
            / total_revenue
            * 100
        )

        insights = [
            (
                f"{top_age['AgeGroup']} is the highest-value "
                "age group in the selected population."
            ),
            (
                f"{top_income['IncomeGroup']} generates the "
                "largest revenue among income groups."
            ),
            (
                f"{top_country['Country']} is the leading "
                f"country with {top_country_share:.1f}% "
                "of selected revenue."
            ),
            (
                f"{repeat_rate:.1f}% of selected customers "
                "placed more than one order."
            )
        ]

        for number, insight in enumerate(
            insights,
            start=1
        ):
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #dce5ec;
                    border-left:5px solid #277c78;
                    border-radius:12px;
                    padding:14px 16px;
                    margin-bottom:12px;
                    color:#172033 !important;
                ">
                    <b>Insight {number}</b><br>
                    {insight}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        f"### Top {top_n} customers by revenue"
    )

    top_customers = (
        filtered
        .nlargest(
            top_n,
            "CustomerRevenue"
        )[
            [
                "UserID",
                "FirstName",
                "LastName",
                "Country",
                "CustomerRevenue",
                "CustomerOrders",
                "CustomerAverageOrderValue",
                "CustomerUnits"
            ]
        ]
        .copy()
    )

    top_customers = top_customers.rename(
        columns={
            "UserID": "Customer ID",
            "FirstName": "First name",
            "LastName": "Last name",
            "Country": "Country",
            "CustomerRevenue": "Revenue",
            "CustomerOrders": "Orders",
            "CustomerAverageOrderValue": "Average order",
            "CustomerUnits": "Units"
        }
    )

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn(
                format="$%.2f"
            ),
            "Average order": st.column_config.NumberColumn(
                format="$%.2f"
            )
        }
    )
