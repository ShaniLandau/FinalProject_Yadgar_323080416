
import streamlit as st
from pathlib import Path
from home import render_home as render_home_page
from overview import render_overview
from customers import render_customers
from products import render_products
from retention import render_retention
from data_quality import render_data_quality
from returns import render_returns

st.set_page_config(
    page_title="ArielLeaf BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# עיצוב בסיסי ורספונסיבי
# -------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background:
            linear-gradient(135deg, #f7f9fc 0%, #eef3f8 100%);
        color: #172033;
    }

    [data-testid="stSidebar"] {
        background: #10233f;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .hero {
        padding: 42px;
        border-radius: 24px;
        color: white;
        background:
            linear-gradient(135deg, #10233f 0%, #236a73 100%);
        box-shadow: 0 18px 45px rgba(16, 35, 63, 0.18);
        margin-bottom: 28px;
    }

    .hero h1 {
        font-size: 44px;
        margin-bottom: 12px;
    }

    .hero p {
        font-size: 18px;
        max-width: 760px;
        opacity: 0.92;
    }

    .section-card {
        padding: 24px;
        border-radius: 18px;
        background: white;
        border: 1px solid #dfe7ef;
        box-shadow: 0 8px 24px rgba(16, 35, 63, 0.07);
        min-height: 160px;
        margin-bottom: 16px;
    }

    .eyebrow {
        color: #2e7d7b;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
    }

    @media (max-width: 768px) {
        .hero {
            padding: 24px;
        }

        .hero h1 {
            font-size: 30px;
        }

        .hero p {
            font-size: 15px;
        }
    }

    .track-badge {
        margin-top: 12px;
        padding: 10px 12px;
        border: 1px solid rgba(80, 211, 199, 0.55);
        border-radius: 10px;
        color: #5ee0d2 !important;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-align: center;
    }

    .group-badge {
        margin-top: 10px;
        color: white !important;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-align: center;
    }

    div.stButton > button {
        background: #16243a;
        color: white !important;
        border: 1px solid #2f455f;
        border-radius: 9px;
        font-weight: 650;
    }

    div.stButton > button p {
        color: white !important;
    }

    div.stButton > button:hover {
        background: #236a73;
        color: white !important;
        border-color: #42b9ad;
    }

    [data-testid="stSidebar"] div.stButton > button {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.22);
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background: #236a73;
        border-color: #5ee0d2;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# ניהול העמוד הפעיל
# -------------------------------------------------
pages = [
    "Home",
    "Executive Overview",
    "Customers",
    "Products",
    "Customer Value & Retention",
    "Returns Intelligence",
    "Data Quality & Cleaning"
]

page_icons = {
    "Home": "⌂",
    "Returns Intelligence": "↩",
    "Data Quality & Cleaning": "✓",
    "Executive Overview": "▣",
    "Customers": "◎",
    "Products": "◇",
    "Customer Value & Retention": "↗"
}

if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

def navigate_to(page_name):
    st.session_state.active_page = page_name

# -------------------------------------------------
# ניווט צדדי באמצעות כפתורים
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ArielLeaf")
    st.caption("Business Intelligence Dashboard")
    st.markdown("---")


    for page_name in pages:

        if page_name == "Returns Intelligence":
            st.markdown(
                """
                <div style="
                    height:28px;
                    border-bottom:1px solid
                    rgba(255,255,255,0.22);
                    margin-bottom:8px;
                ">
                </div>

                <div style="
                    color:#d8b4fe;
                    font-size:0.76rem;
                    font-weight:900;
                    letter-spacing:1.5px;
                    margin:14px 0 10px 0;
                ">
                    BONUS ANALYTICS
                </div>
                """,
                unsafe_allow_html=True
            )

        if page_name == "Data Quality & Cleaning":
            st.markdown(
                """
                <div style="
                    height:28px;
                    border-bottom:1px solid
                    rgba(255,255,255,0.22);
                    margin-bottom:18px;
                "></div>
                <div style="
                    color:#f4bd73;
                    font-size:11px;
                    font-weight:900;
                    letter-spacing:1.4px;
                    margin-bottom:8px;
                ">
                    DATA DOCUMENTATION
                </div>
                """,
                unsafe_allow_html=True
            )

        st.button(
            f"{page_icons[page_name]}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            on_click=navigate_to,
            args=(page_name,)
        )

    st.markdown("---")
    st.markdown(
        """
        <div class="track-badge">
            CODING VIBE TRACK
        </div>
        <div class="group-badge">
            GROUP J
        </div>
        """,
        unsafe_allow_html=True
    )

active_page = st.session_state.active_page

# -------------------------------------------------
# HOME
# -------------------------------------------------
if active_page == "Home":
    render_home_page()

    # HOME_RETURNS_BONUS_SHORTCUT
    st.html(
        """
<div style="
    margin-top:24px;
    padding:22px 26px;
    border:1px solid #c8a7dc;
    border-left:6px solid #76508f;
    border-radius:16px;
    background:linear-gradient(135deg,#f5eef9,#fff8ed);
">
    <div style="
        color:#68407d;
        font-size:0.78rem;
        font-weight:900;
        letter-spacing:1.4px;
        margin-bottom:8px;
    ">
        BONUS ANALYTICS
    </div>

    <h3 style="
        color:#37234f;
        margin:0 0 8px 0;
    ">
        Returns Intelligence
    </h3>

    <p style="
        color:#503f5b;
        margin:0;
    ">
        Explore simulated return patterns by category,
        customer, reason and time.
    </p>
</div>
        """
    )

    st.button(
        "Open Returns Intelligence",
        key="home_returns_bonus",
        use_container_width=True,
        on_click=navigate_to,
        args=("Returns Intelligence",)
    )

elif active_page == "Returns Intelligence":
    render_returns(
        Path(__file__).resolve().parent
    )


elif active_page == "Data Quality & Cleaning":
    render_data_quality(
        Path(__file__).resolve().parent
    )


elif active_page == "Executive Overview":
    render_overview(
        Path(__file__).resolve().parent
    )


elif active_page == "Customers":
    render_customers(
        Path(__file__).resolve().parent
    )



elif active_page == "Products":
    render_products(
        Path(__file__).resolve().parent
    )



elif active_page == "Customer Value & Retention":
    render_retention(
        Path(__file__).resolve().parent
    )


else:
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">ARIELLEAF DASHBOARD</div>
            <h1>{active_page}</h1>
            <p>
                This page is ready. Interactive KPIs, charts,
                filters and insights will be added next.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "The application shell and button-based navigation "
        "are working correctly."
    )

# ADVANCED_NAVIGATION_BONUS
# ניווט רציף בתחתית כל מסך שאינו דף הבית

if active_page != "Home":

    navigation_order = pages.copy()

    current_page_index = navigation_order.index(
        active_page
    )

    previous_page = (
        navigation_order[current_page_index - 1]
        if current_page_index > 0
        else None
    )

    next_page = (
        navigation_order[current_page_index + 1]
        if current_page_index
        < len(navigation_order) - 1
        else None
    )

    st.html(
        f"""
        <div style="
            margin-top:34px;
            padding:18px 22px;
            border-radius:14px;
            border:1px solid #cad6e2;
            background:linear-gradient(
                135deg,
                #ffffff,
                #eef4f8
            );
            text-align:center;
        ">
            <div style="
                color:#607084;
                font-size:0.74rem;
                font-weight:800;
                letter-spacing:1.2px;
                margin-bottom:5px;
            ">
                CURRENT VIEW
            </div>

            <div style="
                color:#10233f;
                font-size:1.05rem;
                font-weight:800;
            ">
                {active_page}
            </div>
        </div>
        """
    )

    previous_column, home_column, next_column = (
        st.columns(3)
    )

    with previous_column:

        if previous_page is not None:
            st.button(
                f"← Previous: {previous_page}",
                key="advanced_previous_page",
                use_container_width=True,
                on_click=navigate_to,
                args=(previous_page,)
            )

    with home_column:

        st.button(
            "⌂ Back to Home",
            key="advanced_home_page",
            use_container_width=True,
            on_click=navigate_to,
            args=("Home",)
        )

    with next_column:

        if next_page is not None:
            st.button(
                f"Next: {next_page} →",
                key="advanced_next_page",
                use_container_width=True,
                on_click=navigate_to,
                args=(next_page,)
            )

