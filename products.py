
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


@st.cache_data
def load_product_data(data_folder):
    data_folder = Path(data_folder)

    products = pd.read_csv(
        data_folder / "product_performance.csv"
    )

    monthly = pd.read_csv(
        data_folder / "product_monthly_performance.csv"
    )

    monthly["YearMonth"] = monthly["YearMonth"].astype(str)
    monthly["Year"] = monthly["YearMonth"].str[:4].astype(int)

    return products, monthly


def style_chart(figure, height=390):
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


def product_card(title, value):
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


def render_products(data_folder):
    st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] label p,
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stMultiSelect"] label p,
        div[data-testid="stSlider"] label,
        div[data-testid="stSlider"] label p,
        div[data-testid="stWidgetLabel"],
        div[data-testid="stWidgetLabel"] p {
            color:#172033 !important;
            -webkit-text-fill-color:#172033 !important;
            opacity:1 !important;
            font-weight:800 !important;
        }
        </style>

        <div class="hero">
            <div class="eyebrow">PRODUCT PERFORMANCE</div>
            <h1>Turn product data into pricing decisions</h1>
            <p>
                Compare products and categories, follow sales trends
                and simulate the revenue effect of price changes.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    products, monthly = load_product_data(data_folder)

    category_options = sorted(
        products["CategoryName"].dropna().unique().tolist()
    )

    filter1, filter2, filter3 = st.columns(3)

    with filter1:
        selected_categories = st.multiselect(
            "Categories",
            options=category_options,
            default=category_options
        )

    with filter2:
        selected_year = st.selectbox(
            "Year",
            options=["All", "2020", "2021", "2022", "2023"]
        )

    with filter3:
        price_change = st.slider(
            "What-If: price change",
            min_value=-20,
            max_value=20,
            value=0,
            step=1,
            format="%d%%"
        )

    filtered_products = products[
        products["CategoryName"].isin(selected_categories)
    ].copy()

    filtered_monthly = monthly[
        monthly["CategoryName"].isin(selected_categories)
    ].copy()

    if selected_year != "All":
        filtered_monthly = filtered_monthly[
            filtered_monthly["Year"] == int(selected_year)
        ].copy()

    if filtered_products.empty or filtered_monthly.empty:
        st.warning("No products match the selected filters.")
        return

    actual_revenue = filtered_monthly["Revenue"].sum()
    projected_revenue = actual_revenue * (
        1 + price_change / 100
    )
    revenue_impact = projected_revenue - actual_revenue

    total_units = int(filtered_monthly["UnitsSold"].sum())
    total_orders = int(filtered_monthly["Orders"].sum())
    product_count = filtered_products["ProductID"].nunique()

    average_selling_price = (
        actual_revenue / total_units
        if total_units else 0
    )

    cards = [
        ("Revenue", f"${actual_revenue / 1_000_000:.2f}M"),
        ("Units Sold", f"{total_units:,}"),
        ("Orders", f"{total_orders:,}"),
        ("Products", f"{product_count:,}"),
        ("Average Selling Price", f"${average_selling_price:,.2f}"),
        ("Projected Revenue", f"${projected_revenue / 1_000_000:.2f}M")
    ]

    first_row = st.columns(3)
    for column, card in zip(first_row, cards[:3]):
        with column:
            product_card(card[0], card[1])

    second_row = st.columns(3)
    for column, card in zip(second_row, cards[3:]):
        with column:
            product_card(card[0], card[1])

    st.markdown("### Revenue trend by category")

    trend_data = (
        filtered_monthly
        .groupby(
            ["YearMonth", "CategoryName"],
            as_index=False
        )
        .agg(Revenue=("Revenue", "sum"))
    )

    trend_figure = px.line(
        trend_data,
        x="YearMonth",
        y="Revenue",
        color="CategoryName",
        markers=True,
        color_discrete_sequence=[
            "#10233f",
            "#277c78",
            "#69aaa4",
            "#d38d46",
            "#7c6da8"
        ],
        labels={
            "YearMonth": "Month",
            "Revenue": "Revenue",
            "CategoryName": "Category"
        }
    )

    trend_figure.update_traces(
        line=dict(width=3),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: $%{y:,.0f}"
            "<extra></extra>"
        )
    )

    style_chart(trend_figure, height=430)

    st.plotly_chart(
        trend_figure,
        use_container_width=True
    )

    left_column, right_column = st.columns([1.25, 1])

    with left_column:
        st.markdown("### Leading product categories")

        category_summary = (
            filtered_monthly
            .groupby("CategoryName", as_index=False)
            .agg(
                Revenue=("Revenue", "sum"),
                UnitsSold=("UnitsSold", "sum")
            )
            .sort_values("Revenue", ascending=True)
        )

        category_figure = px.bar(
            category_summary,
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

        category_figure.update_layout(
            coloraxis_showscale=False
        )

        category_figure.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: $%{x:,.0f}"
                "<extra></extra>"
            )
        )

        style_chart(category_figure, height=410)

        st.plotly_chart(
            category_figure,
            use_container_width=True
        )

    with right_column:
        st.markdown("### What-If revenue simulation")

        scenario_data = pd.DataFrame({
            "Scenario": [
                "Current revenue",
                f"Price change: {price_change:+d}%"
            ],
            "Revenue": [
                actual_revenue,
                projected_revenue
            ]
        })

        scenario_figure = px.bar(
            scenario_data,
            x="Scenario",
            y="Revenue",
            color="Scenario",
            text="Revenue",
            color_discrete_sequence=[
                "#10233f",
                "#277c78"
            ],
            labels={"Revenue": "Revenue"}
        )

        scenario_figure.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                color="#172033",
                size=13
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: $%{y:,.0f}"
                "<extra></extra>"
            )
        )

        scenario_figure.update_layout(
            showlegend=False
        )

        style_chart(scenario_figure, height=410)

        st.plotly_chart(
            scenario_figure,
            use_container_width=True
        )

        impact_color = (
            "#13795b" if revenue_impact >= 0
            else "#b42318"
        )

        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border:1px solid #d7e2ea;
                border-radius:12px;
                padding:14px 16px;
                color:#172033 !important;
            ">
                <b>Simulated revenue impact:</b>
                <span style="
                    color:{impact_color} !important;
                    font-size:20px;
                    font-weight:800;
                ">
                    ${revenue_impact:,.2f}
                </span>
                <br>
                <small>
                    Assumption: unit demand remains constant.
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Product insights")

    top_category = (
        category_summary
        .sort_values("Revenue", ascending=False)
        .iloc[0]
    )

    top_product = (
        filtered_products
        .sort_values("Revenue", ascending=False)
        .iloc[0]
    )

    top_category_share = (
        top_category["Revenue"]
        / actual_revenue
        * 100
    )

    insight_columns = st.columns(2)

    insights = [
        (
            f"{top_category['CategoryName']} is the leading "
            f"category with {top_category_share:.1f}% of revenue."
        ),
        (
            f"{top_product['Name']} is the highest-revenue "
            "individual product in the selected categories."
        ),
        (
            f"The selected products sold {total_units:,} units "
            f"at an average selling price of "
            f"${average_selling_price:,.2f}."
        ),
        (
            f"A {price_change:+d}% price change produces a "
            f"simulated revenue impact of "
            f"${revenue_impact:,.2f}, assuming constant demand."
        )
    ]

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

    st.markdown("### Top 10 products by revenue")

    top_products = (
        filtered_products
        .sort_values("Revenue", ascending=False)
        .head(10)[
            [
                "ProductID",
                "Name",
                "CategoryName",
                "SubcategoryName",
                "Revenue",
                "UnitsSold",
                "Orders",
                "Customers",
                "AverageSellingPrice"
            ]
        ]
        .rename(
            columns={
                "ProductID": "Product ID",
                "Name": "Product",
                "CategoryName": "Category",
                "SubcategoryName": "Subcategory",
                "UnitsSold": "Units sold",
                "AverageSellingPrice": "Average price"
            }
        )
    )

    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn(
                format="$%.2f"
            ),
            "Average price": st.column_config.NumberColumn(
                format="$%.2f"
            )
        }
    )


    # CLICK_THROUGH_DRILLDOWN_BONUS
    st.markdown("---")
    st.markdown("### Click-through product drilldown")

    st.caption(
        "Click a category column to open its subcategory and "
        "product-level details."
    )

    drilldown_summary = (
        filtered_products
        .groupby(
            "CategoryName",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "sum"),
            UnitsSold=("UnitsSold", "sum"),
            Products=("ProductID", "nunique")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    drilldown_figure = px.bar(
        drilldown_summary,
        x="CategoryName",
        y="Revenue",
        color="Revenue",
        custom_data=[
            "CategoryName",
            "UnitsSold",
            "Products"
        ],
        color_continuous_scale=[
            "#b9ddd8",
            "#277c78",
            "#10233f"
        ],
        labels={
            "CategoryName": "Category",
            "Revenue": "Revenue"
        }
    )

    drilldown_figure.update_traces(
        marker_line_color="#ffffff",
        marker_line_width=1.5,
        selected=dict(
            marker=dict(
                opacity=1,
                color="#d4831f"
            )
        ),
        unselected=dict(
            marker=dict(
                opacity=0.45
            )
        ),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Revenue: $%{y:,.0f}<br>"
            "Units sold: %{customdata[1]:,.0f}<br>"
            "Products: %{customdata[2]:,.0f}"
            "<extra></extra>"
        )
    )

    drilldown_figure.update_layout(
        height=390,
        clickmode="event+select",
        coloraxis_showscale=False,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#172033"
        ),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#277c78",
            font=dict(
                color="#10233f",
                size=14
            )
        )
    )

    drilldown_figure.update_xaxes(
        showgrid=False
    )

    drilldown_figure.update_yaxes(
        gridcolor="#e9eef3"
    )

    drilldown_event = st.plotly_chart(
        drilldown_figure,
        use_container_width=True,
        key="product_category_click_drilldown",
        on_select="rerun",
        selection_mode="points"
    )

    try:
        selected_drilldown_points = (
            drilldown_event.selection.points
        )
    except (AttributeError, TypeError):
        selected_drilldown_points = (
            drilldown_event
            .get("selection", {})
            .get("points", [])
            if isinstance(drilldown_event, dict)
            else []
        )

    if selected_drilldown_points:

        selected_point = (
            selected_drilldown_points[0]
        )

        selected_drilldown_category = (
            selected_point.get("x")
        )

        if not selected_drilldown_category:
            point_custom_data = (
                selected_point.get(
                    "customdata",
                    []
                )
            )

            if point_custom_data:
                selected_drilldown_category = (
                    point_custom_data[0]
                )

        category_drilldown_data = (
            filtered_products[
                filtered_products[
                    "CategoryName"
                ]
                == selected_drilldown_category
            ]
            .copy()
        )

        if not category_drilldown_data.empty:

            category_drilldown_revenue = (
                category_drilldown_data[
                    "Revenue"
                ].sum()
            )

            category_drilldown_units = (
                category_drilldown_data[
                    "UnitsSold"
                ].sum()
            )

            category_drilldown_products = (
                category_drilldown_data[
                    "ProductID"
                ].nunique()
            )

            category_drilldown_customers = (
                category_drilldown_data[
                    "Customers"
                ].sum()
            )

            st.markdown(
                f"#### Selected category: "
                f"{selected_drilldown_category}"
            )

            drilldown_kpis = st.columns(4)

            with drilldown_kpis[0]:
                st.html(
                    f"""
                    <div style="
                        background:#ffffff;
                        border:1px solid #cbd8e5;
                        border-radius:12px;
                        padding:16px 18px;
                        min-height:88px;
                    ">
                        <div style="
                            color:#33455c;
                            font-size:14px;
                            font-weight:700;
                        ">
                            Category Revenue
                        </div>
                        <div style="
                            color:#10233f;
                            font-size:30px;
                            font-weight:800;
                            margin-top:8px;
                        ">
                            ${category_drilldown_revenue / 1_000_000:.2f}M
                        </div>
                    </div>
                    """
                )

            with drilldown_kpis[1]:
                st.html(
                    f"""
                    <div style="
                        background:#ffffff;
                        border:1px solid #cbd8e5;
                        border-radius:12px;
                        padding:16px 18px;
                        min-height:88px;
                    ">
                        <div style="
                            color:#33455c;
                            font-size:14px;
                            font-weight:700;
                        ">
                            Units Sold
                        </div>
                        <div style="
                            color:#10233f;
                            font-size:30px;
                            font-weight:800;
                            margin-top:8px;
                        ">
                            {int(category_drilldown_units):,}
                        </div>
                    </div>
                    """
                )

            with drilldown_kpis[2]:
                st.html(
                    f"""
                    <div style="
                        background:#ffffff;
                        border:1px solid #cbd8e5;
                        border-radius:12px;
                        padding:16px 18px;
                        min-height:88px;
                    ">
                        <div style="
                            color:#33455c;
                            font-size:14px;
                            font-weight:700;
                        ">
                            Products
                        </div>
                        <div style="
                            color:#10233f;
                            font-size:30px;
                            font-weight:800;
                            margin-top:8px;
                        ">
                            {int(category_drilldown_products):,}
                        </div>
                    </div>
                    """
                )

            with drilldown_kpis[3]:
                st.html(
                    f"""
                    <div style="
                        background:#ffffff;
                        border:1px solid #cbd8e5;
                        border-radius:12px;
                        padding:16px 18px;
                        min-height:88px;
                    ">
                        <div style="
                            color:#33455c;
                            font-size:14px;
                            font-weight:700;
                        ">
                            Product-Customer Links
                        </div>
                        <div style="
                            color:#10233f;
                            font-size:30px;
                            font-weight:800;
                            margin-top:8px;
                        ">
                            {int(category_drilldown_customers):,}
                        </div>
                    </div>
                    """
                )

            subcategory_drilldown = (
                category_drilldown_data
                .groupby(
                    "SubcategoryName",
                    as_index=False
                )
                .agg(
                    Revenue=("Revenue", "sum"),
                    UnitsSold=("UnitsSold", "sum"),
                    Products=("ProductID", "nunique")
                )
                .sort_values(
                    "Revenue",
                    ascending=True
                )
            )

            detail_chart_column, detail_table_column = (
                st.columns([1.1, 1])
            )

            with detail_chart_column:

                st.markdown(
                    "##### Revenue by subcategory"
                )

                subcategory_figure = px.bar(
                    subcategory_drilldown,
                    x="Revenue",
                    y="SubcategoryName",
                    orientation="h",
                    color="Revenue",
                    color_continuous_scale=[
                        "#b9ddd8",
                        "#277c78",
                        "#10233f"
                    ],
                    labels={
                        "SubcategoryName": "",
                        "Revenue": "Revenue"
                    }
                )

                subcategory_figure.update_traces(
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Revenue: $%{x:,.0f}"
                        "<extra></extra>"
                    )
                )

                subcategory_figure.update_layout(
                    height=430,
                    coloraxis_showscale=False,
                    margin=dict(
                        l=20,
                        r=20,
                        t=20,
                        b=20
                    ),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    font=dict(
                        family="Arial",
                        color="#172033"
                    )
                )

                subcategory_figure.update_xaxes(
                    gridcolor="#e9eef3"
                )

                subcategory_figure.update_yaxes(
                    showgrid=False
                )

                st.plotly_chart(
                    subcategory_figure,
                    use_container_width=True
                )

            with detail_table_column:

                st.markdown(
                    "##### Leading products in the category"
                )

                category_product_details = (
                    category_drilldown_data
                    .sort_values(
                        "Revenue",
                        ascending=False
                    )
                    .head(10)[
                        [
                            "ProductID",
                            "Name",
                            "SubcategoryName",
                            "Revenue",
                            "UnitsSold",
                            "Orders",
                            "AverageSellingPrice"
                        ]
                    ]
                    .rename(
                        columns={
                            "ProductID": "Product ID",
                            "Name": "Product",
                            "SubcategoryName": "Subcategory",
                            "UnitsSold": "Units sold",
                            "AverageSellingPrice": "Average price"
                        }
                    )
                )

                st.dataframe(
                    category_product_details,
                    use_container_width=True,
                    hide_index=True,
                    height=430,
                    column_config={
                        "Revenue": st.column_config.NumberColumn(
                            format="$%.2f"
                        ),
                        "Average price": st.column_config.NumberColumn(
                            format="$%.2f"
                        )
                    }
                )

            st.info(
                "Drilldown path: Category → Subcategory → Product"
            )

    else:
        st.info(
            "Select a category column above to reveal its "
            "subcategory and product details."
        )


    # DRILLDOWN_STRONG_CONTRAST_FIX
    st.markdown(
        """
        <style>
        div[data-testid="stPlotlyChart"] svg g.xtick text,
        div[data-testid="stPlotlyChart"] svg g.ytick text,
        div[data-testid="stPlotlyChart"] svg g.g-xtitle text,
        div[data-testid="stPlotlyChart"] svg g.g-ytitle text,
        div[data-testid="stPlotlyChart"] svg text.xtitle,
        div[data-testid="stPlotlyChart"] svg text.ytitle {
            fill:#10233f !important;
            color:#10233f !important;
            opacity:1 !important;
            font-weight:600 !important;
        }

        div[data-testid="stPlotlyChart"] svg g.gridlayer path {
            stroke:#d6dee8 !important;
            opacity:1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
