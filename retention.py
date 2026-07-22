
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


@st.cache_data
def load_retention_data(data_folder):
    data_folder = Path(data_folder)

    segments = pd.read_csv(
        data_folder / "rfm_segment_summary.csv"
    )

    return segments


def style_rfm_chart(figure, height=400):
    figure.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(
            family="Arial",
            color="#172033",
            size=13
        ),
        legend=dict(font=dict(color="#172033")),
        legend_title_text="",
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_color="#172033"
        )
    )

    figure.update_xaxes(
        showgrid=False,
        color="#172033",
        tickfont=dict(color="#172033", size=12),
        title_font=dict(color="#172033", size=13)
    )

    figure.update_yaxes(
        gridcolor="#dbe4ec",
        color="#172033",
        tickfont=dict(color="#172033", size=12),
        title_font=dict(color="#172033", size=13)
    )

    return figure


def rfm_card(title, value):
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
                font-weight:800;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_retention(data_folder):
    st.markdown(
        """
        <style>
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stMultiSelect"] label p,
        div[data-testid="stWidgetLabel"],
        div[data-testid="stWidgetLabel"] p {
            color:#172033 !important;
            -webkit-text-fill-color:#172033 !important;
            opacity:1 !important;
            font-weight:800 !important;
        }
        </style>

        <div class="hero">
            <div class="eyebrow">
                EXERCISE 4 · CUSTOMER VALUE & RETENTION
            </div>
            <h1>Which customers should management prioritize?</h1>
            <p>
                RFM segmentation combines recency, purchasing frequency
                and monetary value to identify retention opportunities
                and guide targeted management actions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    segments = load_retention_data(data_folder)

    segment_order = [
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "At Risk",
        "Needs Attention",
        "Hibernating"
    ]

    available_segments = [
        segment for segment in segment_order
        if segment in segments["Segment"].tolist()
    ]

    selected_segments = st.multiselect(
        "Customer segments",
        options=available_segments,
        default=available_segments
    )

    filtered = segments[
        segments["Segment"].isin(selected_segments)
    ].copy()

    if filtered.empty:
        st.warning(
            "Select at least one customer segment."
        )
        return

    total_customers = int(filtered["Customers"].sum())
    total_revenue = filtered["Revenue"].sum()

    average_revenue_customer = (
        total_revenue / total_customers
    )

    weighted_recency = (
        (
            filtered["AverageRecencyDays"]
            * filtered["Customers"]
        ).sum()
        / total_customers
    )

    cards = [
        ("Selected Customers", f"{total_customers:,}"),
        ("Segment Revenue", f"${total_revenue / 1_000_000:.2f}M"),
        (
            "Revenue per Customer",
            f"${average_revenue_customer:,.2f}"
        ),
        (
            "Average Recency",
            f"{weighted_recency:,.0f} days"
        )
    ]

    card_columns = st.columns(4)

    for column, card in zip(card_columns, cards):
        with column:
            rfm_card(card[0], card[1])

    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.markdown("### Customers by RFM segment")

        customer_chart_data = filtered.sort_values(
            "Customers",
            ascending=True
        )

        customer_figure = px.bar(
            customer_chart_data,
            x="Customers",
            y="Segment",
            orientation="h",
            color="Customers",
            color_continuous_scale=[
                "#b9ddd8",
                "#277c78",
                "#10233f"
            ],
            labels={
                "Segment": "",
                "Customers": "Customers"
            }
        )

        customer_figure.update_layout(
            coloraxis_showscale=False
        )

        customer_figure.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Customers: %{x:,.0f}"
                "<extra></extra>"
            )
        )

        style_rfm_chart(
            customer_figure,
            height=420
        )

        st.plotly_chart(
            customer_figure,
            use_container_width=True
        )

    with right_chart:
        st.markdown("### Revenue contribution by segment")

        revenue_figure = px.pie(
            filtered,
            names="Segment",
            values="Revenue",
            hole=0.58,
            color="Segment",
            color_discrete_sequence=[
                "#10233f",
                "#277c78",
                "#69aaa4",
                "#d38d46",
                "#b55d5d",
                "#7c6da8"
            ]
        )

        revenue_figure.update_traces(
            textinfo="percent+label",
            textfont=dict(
                color="#172033",
                size=12
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Revenue: $%{value:,.0f}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        revenue_figure.update_layout(
            annotations=[
                dict(
                    text="Revenue<br>Mix",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(
                        color="#172033",
                        size=16
                    )
                )
            ]
        )

        style_rfm_chart(
            revenue_figure,
            height=420
        )

        st.plotly_chart(
            revenue_figure,
            use_container_width=True
        )

    st.markdown("### Value and recency relationship")

    bubble_figure = px.scatter(
        filtered,
        x="AverageRecencyDays",
        y="RevenuePerCustomer",
        size="Customers",
        color="Segment",
        text="Segment",
        size_max=55,
        color_discrete_sequence=[
            "#10233f",
            "#277c78",
            "#69aaa4",
            "#d38d46",
            "#b55d5d",
            "#7c6da8"
        ],
        labels={
            "AverageRecencyDays": "Average recency (days)",
            "RevenuePerCustomer": "Revenue per customer"
        }
    )

    bubble_figure.update_traces(
        textposition="top center",
        textfont=dict(
            color="#172033",
            size=12
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Average recency: %{x:,.1f} days<br>"
            "Revenue per customer: $%{y:,.2f}"
            "<extra></extra>"
        )
    )

    style_rfm_chart(
        bubble_figure,
        height=450
    )

    st.plotly_chart(
        bubble_figure,
        use_container_width=True
    )

    st.markdown("### Management insights")

    champion_row = segments[
        segments["Segment"] == "Champions"
    ].iloc[0]

    hibernating_row = segments[
        segments["Segment"] == "Hibernating"
    ].iloc[0]

    at_risk_row = segments[
        segments["Segment"] == "At Risk"
    ].iloc[0]

    loyal_row = segments[
        segments["Segment"] == "Loyal Customers"
    ].iloc[0]

    insights = [
        (
            f"Champions represent "
            f"{champion_row['CustomerSharePct']:.1f}% "
            f"of customers but generate "
            f"{champion_row['RevenueSharePct']:.1f}% "
            "of total revenue."
        ),
        (
            f"Hibernating is the largest segment with "
            f"{int(hibernating_row['Customers']):,} customers, "
            f"but its average recency is "
            f"{hibernating_row['AverageRecencyDays']:.0f} days."
        ),
        (
            f"The At Risk segment contains "
            f"{int(at_risk_row['Customers']):,} historically "
            "valuable customers who require reactivation."
        ),
        (
            f"Champions and Loyal Customers together generate "
            f"{champion_row['RevenueSharePct'] + loyal_row['RevenueSharePct']:.1f}% "
            "of total revenue."
        )
    ]

    insight_columns = st.columns(2)

    for index, insight in enumerate(insights):
        with insight_columns[index % 2]:
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
                    <b>Insight {index + 1}</b><br>
                    {insight}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Recommended management actions")

    action_map = {
        "Champions": (
            "Protect loyalty through VIP benefits, early access "
            "and referral programs."
        ),
        "Loyal Customers": (
            "Use cross-selling, personalized bundles and "
            "loyalty rewards."
        ),
        "Potential Loyalists": (
            "Encourage the next purchase with personalized "
            "recommendations and limited offers."
        ),
        "At Risk": (
            "Launch an urgent win-back campaign with a "
            "personalized incentive."
        ),
        "Needs Attention": (
            "Use reminders, relevant content and a moderate "
            "reactivation offer."
        ),
        "Hibernating": (
            "Run a low-cost reactivation test and suppress "
            "unresponsive customers later."
        )
    }

    action_table = filtered[
        [
            "Segment",
            "Customers",
            "Revenue",
            "AverageRecencyDays",
            "AverageOrders",
            "RevenuePerCustomer"
        ]
    ].copy()

    action_table["Recommended Action"] = (
        action_table["Segment"].map(action_map)
    )

    action_table = action_table.rename(
        columns={
            "AverageRecencyDays": "Average recency",
            "AverageOrders": "Average orders",
            "RevenuePerCustomer": "Revenue per customer"
        }
    )

    st.dataframe(
        action_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn(
                format="$%.2f"
            ),
            "Revenue per customer":
                st.column_config.NumberColumn(
                    format="$%.2f"
                ),
            "Average recency":
                st.column_config.NumberColumn(
                    format="%.1f days"
                ),
            "Average orders":
                st.column_config.NumberColumn(
                    format="%.2f"
                )
        }
    )


    # HIDDEN_BUSINESS_INSIGHT_BONUS
    st.markdown("---")
    st.markdown("### Hidden business insight")
    st.caption(
        "A small customer segment contains a retention opportunity "
        "that is easy to miss in the headline KPIs."
    )

    if "hidden_insight_revealed" not in st.session_state:
        st.session_state.hidden_insight_revealed = False

    insight_button_label = (
        "Hide the analyst insight"
        if st.session_state.hidden_insight_revealed
        else "Reveal the analyst insight"
    )

    if st.button(
        insight_button_label,
        key="reveal_hidden_business_insight",
        use_container_width=True
    ):
        st.session_state.hidden_insight_revealed = (
            not st.session_state.hidden_insight_revealed
        )
        st.rerun()

    if st.session_state.hidden_insight_revealed:

        hidden_rfm = pd.read_csv(
            Path(data_folder)
            / "rfm_segment_summary.csv"
        )

        at_risk = hidden_rfm[
            hidden_rfm["Segment"] == "At Risk"
        ].iloc[0]

        hibernating = hidden_rfm[
            hidden_rfm["Segment"] == "Hibernating"
        ].iloc[0]

        champions = hidden_rfm[
            hidden_rfm["Segment"] == "Champions"
        ].iloc[0]

        value_vs_hibernating = (
            at_risk["RevenuePerCustomer"]
            / hibernating["RevenuePerCustomer"]
        )

        value_vs_champions = (
            at_risk["RevenuePerCustomer"]
            / champions["RevenuePerCustomer"]
            * 100
        )

        st.html(
            f"""
            <div style="
                padding:24px 26px;
                border-radius:16px;
                border:1px solid #d4c3a2;
                border-left:7px solid #b7791f;
                background:linear-gradient(
                    135deg,
                    #fffaf0,
                    #ffffff
                );
                margin:10px 0 18px 0;
            ">
                <div style="
                    color:#9a6319;
                    font-size:0.76rem;
                    font-weight:900;
                    letter-spacing:1.3px;
                    margin-bottom:9px;
                ">
                    ANALYST NOTE · HIGH-VALUE CUSTOMERS GOING QUIET
                </div>

                <div style="
                    color:#172033;
                    font-size:1.08rem;
                    line-height:1.65;
                ">
                    The <strong>At Risk</strong> segment contains only
                    <strong>{int(at_risk["Customers"]):,} customers</strong>
                    ({at_risk["CustomerSharePct"]:.2f}% of the base),
                    but each customer previously generated an average of
                    <strong>${at_risk["RevenuePerCustomer"]:,.0f}</strong>
                    across
                    <strong>{at_risk["AverageOrders"]:.1f} orders</strong>.

                    Their value per customer is
                    <strong>{value_vs_hibernating:.1f} times</strong>
                    that of a Hibernating customer and still equals
                    <strong>{value_vs_champions:.0f}%</strong>
                    of a Champion's value.

                    The concern is not weak purchasing history. These are
                    proven customers who have now been inactive for about
                    <strong>{at_risk["AverageRecencyDays"]:.0f} days</strong>.
                </div>

                <div style="
                    margin-top:14px;
                    padding-top:13px;
                    border-top:1px solid #e7d8bd;
                    color:#6d4a17;
                    font-weight:700;
                ">
                    Management implication:
                    prioritize a focused win-back campaign for this small,
                    high-value group before launching a broad retention
                    campaign.
                </div>
            </div>
            """
        )

        insight_chart = px.scatter(
            hidden_rfm,
            x="AverageRecencyDays",
            y="RevenuePerCustomer",
            size="Customers",
            color="Segment",
            text="Segment",
            size_max=48,
            labels={
                "AverageRecencyDays":
                    "Average days since last activity",
                "RevenuePerCustomer":
                    "Historical revenue per customer"
            },
            color_discrete_map={
                "At Risk": "#c47b19",
                "Champions": "#17324f",
                "Loyal Customers": "#277c78",
                "Potential Loyalists": "#69a8a3",
                "Hibernating": "#9aa6b2",
                "Needs Attention": "#c6ced6"
            }
        )

        insight_chart.update_traces(
            textposition="top center",
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Average inactivity: %{x:.0f} days<br>"
                "Revenue per customer: $%{y:,.0f}"
                "<extra></extra>"
            )
        )

        insight_chart.update_layout(
            height=440,
            margin=dict(
                l=20,
                r=20,
                t=45,
                b=20
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(
                family="Arial",
                color="#172033"
            ),
            showlegend=False
        )

        insight_chart.update_xaxes(
            gridcolor="#edf0f3"
        )

        insight_chart.update_yaxes(
            gridcolor="#edf0f3"
        )

        st.plotly_chart(
            insight_chart,
            use_container_width=True
        )

        st.markdown(
            "#### Size a focused win-back test"
        )

        recovery_target = st.slider(
            "Share of At Risk customers to target",
            min_value=5,
            max_value=30,
            value=15,
            step=5,
            format="%d%%"
        )

        target_customers = round(
            at_risk["Customers"]
            * recovery_target
            / 100
        )

        historical_value_represented = (
            at_risk["Revenue"]
            * recovery_target
            / 100
        )

        scenario_col1, scenario_col2 = st.columns(2)

        scenario_col1.metric(
            "Customers in test group",
            f"{target_customers:,}"
        )

        scenario_col2.metric(
            "Historical value represented",
            f"${historical_value_represented:,.0f}"
        )

        st.caption(
            "This is a campaign-sizing reference based on historical "
            "customer value, not a revenue forecast."
        )
