import html
import io
import json
import os

import requests
import streamlit as st
from PIL import Image

from streamlit_compat import button_wide, image_wide

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(
    page_title="YHealth | Think Future Technologies",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0f1724;
    color: #e8edf4;
}
.stApp { background: #0f1724; }

.block-container {
    padding: 0.6rem 1rem 1.2rem !important;
    max-width: 880px;
}

.brand-wrap {
    text-align: center;
    padding: 0.75rem 0 1rem;
    border-bottom: 1px solid #1e2d42;
    margin-bottom: 0.85rem;
}
.brand-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.03em;
    line-height: 1.2;
}
.brand-company {
    font-size: 0.8rem;
    font-weight: 500;
    color: #5b8def;
    margin-top: 0.25rem;
}
.brand-tagline {
    font-size: 0.85rem;
    color: #8fa3bc;
    margin-top: 0.45rem;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.7rem;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    margin: 0.5rem auto 0;
}
.status-wrap { text-align: center; }
.status-ok { background: #122238; color: #5b8def; border: 1px solid #1e3a5f; }
.status-err { background: #2a1818; color: #e88; border: 1px solid #4a2828; }

.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #6b849e;
    margin: 0.35rem 0 0.35rem;
}

.insight-pill {
    display: inline-block;
    background: #122238;
    color: #7eb8ff;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 0.35rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.upload-hint-box {
    background: #141e2e;
    border: 1px dashed #2a3d55;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    color: #6b849e;
    font-size: 0.8rem;
}

.card {
    background: #141e2e;
    border: 1px solid #1e2d42;
    border-radius: 10px;
    padding: 0.7rem 0.85rem;
    margin-bottom: 0.4rem;
    transition: border-color 0.15s ease;
}
.card:hover { border-color: #2a4a6e; }

[data-testid="stImage"] img {
    border-radius: 10px !important;
    max-height: 180px !important;
    object-fit: contain !important;
    width: auto !important;
    max-width: 100% !important;
    margin: 0 auto;
    display: block;
    background: #141e2e;
}

.stButton > button {
    width: 100%;
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    transition: background 0.15s ease !important;
}
.stButton > button:hover { background: #1d4ed8 !important; }
.stButton > button:disabled {
    background: #1e2d42 !important;
    color: #6b849e !important;
}

[data-testid="stFileUploader"] section {
    background: #141e2e !important;
    border: 1px dashed #2a3d55 !important;
    border-radius: 10px !important;
    padding: 0.65rem !important;
}

[data-testid="stMetric"] {
    background: #141e2e;
    border: 1px solid #1e2d42;
    border-radius: 10px;
    padding: 0.5rem 0.4rem;
}

[data-testid="stSpinner"] { color: #2563eb !important; }

#MainMenu, footer, header { visibility: hidden; }
hr { border-color: #1e2d42 !important; margin: 0.6rem 0 !important; }

.app-footer {
    text-align: center;
    color: #4a6278;
    font-size: 0.7rem;
    padding: 0.4rem 0;
}
</style>
""",
    unsafe_allow_html=True,
)


def esc(text) -> str:
    return html.escape(str(text))


def check_api_health():
    try:
        resp = requests.get(f"{API_URL}/health", timeout=5)
        if resp.status_code == 200:
            return True, "API connected"
        return False, f"API error ({resp.status_code})"
    except requests.exceptions.ConnectionError:
        return False, "API offline — start backend on port 8000"
    except Exception:
        return False, "API unreachable"


def analyze_image(image_bytes: bytes, filename: str, mime: str):
    return requests.post(
        f"{API_URL}/analyze",
        files={"file": (filename, image_bytes, mime)},
        timeout=90,
    )


def get_confidence_map(data: dict) -> dict:
    return {
        entry["name"]: float(entry.get("confidence", 0))
        for entry in data.get("confidence_scores", [])
    }


def api_json_for_display(data: dict) -> dict:
    return {
        "items": data.get("items", []),
        "total_macros": data.get("total_macros", {}),
    }


def load_image_from_source(uploaded, camera):
    if uploaded is not None:
        data = uploaded.getvalue()
        return Image.open(io.BytesIO(data)), data, uploaded.name, uploaded.type or "image/jpeg"
    if camera is not None:
        data = camera.getvalue()
        return Image.open(io.BytesIO(data)), data, "camera.jpg", "image/jpeg"
    return None, None, "", ""


def render_food_card(item: dict, confidence: float):
    name = esc(item["name"])
    qty = esc(item.get("quantity", "1 serving"))
    cal = int(item["calories"])
    p, c, f = item["protein_g"], item["carbs_g"], item["fat_g"]
    conf_color = "#5b8def" if confidence >= 70 else "#8fa3bc" if confidence >= 40 else "#c9a227"

    st.markdown(
        f"""
        <div class="card" style="display:flex;justify-content:space-between;
        align-items:center;flex-wrap:wrap;gap:0.35rem;">
            <div>
                <div style="font-weight:600;font-size:0.9rem;color:#e8edf4;">{name}</div>
                <div style="font-size:0.74rem;color:#6b849e;margin-top:0.12rem;">
                    {qty} · Protein {p}g · Carbs {c}g · Fat {f}g
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.68rem;color:{conf_color};">{confidence:.0f}% match</div>
                <div style="font-weight:700;font-size:0.92rem;color:#5b8def;">{cal} kcal</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


for key, default in (("result", None), ("error", None), ("analyzing", False)):
    if key not in st.session_state:
        st.session_state[key] = default

# Branding (center-aligned)
st.markdown(
    """
    <div class="brand-wrap">
        <div class="brand-title">YHealth</div>
        <div class="brand-company">by Think Future Technologies</div>
        <div class="brand-tagline">Your Food &amp; Nutrition Analyzer</div>
    </div>
    """,
    unsafe_allow_html=True,
)

api_ok, api_msg = check_api_health()
pill_cls = "status-ok" if api_ok else "status-err"
st.markdown(
    f'<div class="status-wrap"><span class="status-pill {pill_cls}">'
    f'{"●" if api_ok else "○"} {esc(api_msg)}</span></div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1], gap="medium")

with left:
    st.markdown('<div class="section-title">Upload Meal</div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["Upload", "Camera"])
    uploaded = camera = None
    with t1:
        uploaded = st.file_uploader("Upload", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
    with t2:
        camera = st.camera_input("Camera", label_visibility="collapsed")

    image, image_bytes, fname, mime = load_image_from_source(uploaded, camera)

    if image:
        image_wide(image)
        if button_wide("Analyze meal", disabled=not api_ok):
            st.session_state["analyzing"] = True
            st.session_state["error"] = None
            with st.spinner("Analyzing meal..."):
                try:
                    resp = analyze_image(image_bytes, fname, mime)
                    if resp.status_code == 200:
                        st.session_state["result"] = resp.json()
                        st.session_state["error"] = None
                    else:
                        try:
                            detail = resp.json().get("detail", "Analysis failed.")
                        except Exception:
                            detail = "Analysis failed."
                        st.session_state["error"] = detail
                        st.session_state["result"] = None
                except requests.exceptions.ConnectionError:
                    st.session_state["error"] = "Cannot reach API. Is the backend running?"
                    st.session_state["result"] = None
                except requests.exceptions.Timeout:
                    st.session_state["error"] = "Request timed out. Try a smaller image."
                    st.session_state["result"] = None
                except Exception as exc:
                    st.session_state["error"] = esc(str(exc))
                    st.session_state["result"] = None
                finally:
                    st.session_state["analyzing"] = False
            st.rerun()
    else:
        st.markdown(
            '<div class="upload-hint-box">JPG, PNG or WEBP · max 10MB<br>Use upload or camera</div>',
            unsafe_allow_html=True,
        )

with right:
    if st.session_state.get("analyzing"):
        st.info("Analyzing meal...")

    if st.session_state.get("error"):
        st.error(st.session_state["error"])

    if st.session_state.get("result"):
        data = st.session_state["result"]
        total = data["total_macros"]
        items = data["items"]
        conf_map = get_confidence_map(data)
        insight = data.get("meal_insight", "")

        st.markdown('<div class="section-title">Nutrition Summary</div>', unsafe_allow_html=True)

        if insight:
            st.markdown(
                f'<span class="insight-pill">{esc(insight)}</span>',
                unsafe_allow_html=True,
            )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Calories", f"{total['calories']}")
        m2.metric("Protein", f"{total['protein_g']}g")
        m3.metric("Carbs", f"{total['carbs_g']}g")
        m4.metric("Fat", f"{total['fat_g']}g")

        cal = total["calories"]
        if cal > 0:
            p_pct = min(100, round((total["protein_g"] * 4 / cal) * 100))
            c_pct = min(100, round((total["carbs_g"] * 4 / cal) * 100))
            f_pct = min(100, round((total["fat_g"] * 9 / cal) * 100))
            st.caption(f"Macro split: Protein {p_pct}% · Carbs {c_pct}% · Fat {f_pct}%")

        st.markdown('<div class="section-title">Detected Meal</div>', unsafe_allow_html=True)
        for item in items:
            render_food_card(item, conf_map.get(item["name"], 0))

        with st.expander("View API Response"):
            st.code(json.dumps(api_json_for_display(data), indent=2), language="json")

    elif not st.session_state.get("error") and not st.session_state.get("analyzing"):
        st.markdown(
            """
            <div style="text-align:center;padding:1.5rem 0.5rem;color:#4a6278;">
                <div style="font-size:1.6rem;margin-bottom:0.35rem;">📋</div>
                <div style="font-size:0.85rem;">Nutrition summary appears here</div>
                <div style="font-size:0.74rem;margin-top:0.2rem;">Upload a meal photo to begin</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    '<hr><div class="app-footer">YHealth · Think Future Technologies · tftus.com</div>',
    unsafe_allow_html=True,
)
