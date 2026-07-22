
import streamlit as st
import textwrap


def html(content):
    st.markdown(
        textwrap.dedent(content),
        unsafe_allow_html=True
    )


def go_to(page):
    st.session_state["active_page"] = page
    st.rerun()


def render_home():
    st.markdown(
        '<div class="hero">'
        '<div class="eyebrow">'
        'ARIELLEAF · BUSINESS INTELLIGENCE'
        '</div>'
        '<div style="'
        'display:inline-block;'
        'margin:10px 0 14px 0;'
        'padding:8px 16px;'
        'border:1px solid #5ee0d2;'
        'border-radius:999px;'
        'color:#5ee0d2;'
        'font-weight:900;'
        'letter-spacing:1.4px;'
        '">'
        'CODING VIBE TRACK'
        '</div>'
        '<h1>'
        'ArielLeaf Business Intelligence Dashboard'
        '</h1>'
        '<p>'
        'Explore sales performance, customer behavior, '
        'product trends, pricing scenarios and customer '
        'retention opportunities across 2020–2023.'
        '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:
        html("""
        <div style="
            background:white;
            border:1px solid #d7e2ea;
            border-radius:15px;
            padding:22px;
            min-height:205px;
            color:#172033;
        ">
            <h3 style="color:#10233f;">Submitted by</h3>
            <div dir="rtl"
                 style="text-align:left;
                        color:#334155;
                        font-size:17px;
                        line-height:1.9;
                        font-weight:700;">
                הדר יאדגר<br>
                שני לנדאו<br>
                איילה בראשי<br>
                דוד תורגמן
            </div>
        </div>
        """)

    with right:
        html("""
        <div style="
            background:white;
            border:1px solid #d7e2ea;
            border-radius:15px;
            padding:22px;
            min-height:205px;
            color:#334155;
            font-size:15px;
            line-height:1.8;
        ">
            <h3 style="color:#10233f;">
                Development environment
            </h3>
            <b>Track:</b> Coding Vibe<br>
            <b>AI tool:</b> ChatGPT–Codex (GPT-5)<br>
            <b>Environment:</b> Google Colab /
            Python 3.12.13<br>
            <b>Dashboard:</b> Streamlit 1.59.2<br>
            <b>Visualization:</b> Plotly 5.24.1
        </div>
        """)

    st.markdown("## Explore the dashboard")

    row1 = st.columns(2)

    with row1[0]:
        st.markdown("### Performance Overview")
        st.write(
            "Revenue, orders, customers and business trends."
        )
        if st.button(
            "Open Executive Overview",
            use_container_width=True
        ):
            go_to("Executive Overview")

    with row1[1]:
        st.markdown("### Customer Intelligence")
        st.write(
            "Customer value, demographics and locations."
        )
        if st.button(
            "Open Customers",
            use_container_width=True
        ):
            go_to("Customers")

    row2 = st.columns(2)

    with row2[0]:
        st.markdown("### Product Performance")
        st.write(
            "Products, categories and What-If pricing."
        )
        if st.button(
            "Open Products",
            use_container_width=True
        ):
            go_to("Products")

    with row2[1]:
        st.markdown("### Customer Value & Retention")
        st.write(
            "Exercise 4: RFM segments and retention actions."
        )
        if st.button(
            "Open Customer Value & Retention",
            use_container_width=True
        ):
            go_to("Customer Value & Retention")

    st.markdown("---")

    st.markdown(
        '<div style="'
        'background:#fff4e2;'
        'border:1px solid #e5c79e;'
        'border-left:6px solid #c77828;'
        'border-radius:14px;'
        'padding:18px 20px;'
        'margin-top:10px;'
        '">'
        '<div style="'
        'color:#9b5d22;'
        'font-size:12px;'
        'font-weight:900;'
        'letter-spacing:1.3px;'
        '">DATA DOCUMENTATION</div>'
        '<h3 style="'
        'color:#3d260f;'
        'margin:7px 0;'
        '">Data Quality & Cleaning Log</h3>'
        '<div style="color:#71502f;">'
        'Review the original data issues, cleaning actions, '
        'row-count summary, key decisions and validation results.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Open Data Quality & Cleaning",
        use_container_width=True,
        key="home_data_quality"
    ):
        go_to("Data Quality & Cleaning")

    st.info(
        "Use the buttons above or the permanent button-based "
        "navigation panel on the left. No tabs are used."
    )
