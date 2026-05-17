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
    page_title="YHealth by TFT",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0f1419;
    color: #e8ecf1;
}
.stApp { background: #0f1419; }

.block-container {
    padding: 0.8rem 1.2rem 1.5rem !important;
    max-width: 920px;
}

.app-header {
    padding: 0.6rem 0 0.9rem;
    border-bottom: 1px solid #1e2833;
    margin-bottom: 0.9rem;
}
.brand {
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
}
.brand span { color: #2dd4a8; }
.tagline {
    font-size: 0.82rem;
    color: #8b9aab;
    margin-top: 0.15rem;
}
.subtitle {
    font-size: 0.78rem;
    color: #6b7c8f;
    margin-top: 0.35rem;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    margin-top: 0.5rem;
}
.status-ok { background: #132820; color: #2dd4a8; border: 1px solid #1f4035; }
.status-err { background: #2a1818; color: #f08080; border: 1px solid #4a2828; }

.section-title {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b7c8f;
    margin: 0.5rem 0 0.4rem;
}

.upload-hint-box {
    background: #151b22;
    border: 1px dashed #2a3544;
    border-radius: 10px;
    padding: 1.2rem 1rem;
    text-align: center;
    color: #6b7c8f;
    font-size: 0.82rem;
}

[data-testid="stImage"] img {
    border-radius: 10px !important;
    max-height: 200px !important;
    object-fit: contain !important;
    width: auto !important;
    max-width: 100% !important;
    margin: 0 auto;
    display: block;
    background: #151b22;
}

.stButton > button {
    width: 100%;
    background: #2dd4a8 !important;
    color: #0a1218 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
.stButton > button:hover { background: #26c49a !important; }
.stButton > button:disabled {
    background: #2a3544 !important;
    color: #6b7c8f !important;
}

[data-testid="stFileUploader"] section {
    background: #151b22 !important;
    border: 1px dashed #2a3544 !important;
    border-radius: 10px !important;
    padding: 0.8rem !important;
}

[data-testid="stSpinner"] { color: #2dd4a8 !important; }

#MainMenu, footer, header { visibility: hidden; }
hr { border-color: #1e2833 !important; margin: 0.8rem 0 !important; }

.app-footer {
    text-align: center;
    color: #4a5a6a;
    font-size: 0.72rem;
    padding: 0.5rem 0;
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
            data = resp.json()
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


def render_food_item(item: dict, confidence: float):
    name = esc(item["name"])
    qty = esc(item.get("quantity", "1 serving"))
    cal = int(item["calories"])
    p, c, f = item["protein_g"], item["carbs_g"], item["fat_g"]

    if confidence >= 70:
        conf_color = "#2dd4a8"
    elif confidence >= 40:
        conf_color = "#8ab4f8"
    else:
        conf_color = "#c9a227"

    st.markdown(
        f"""
        <div style="background:#151b22;border:1px solid #1e2833;border-radius:10px;
        padding:0.75rem 0.9rem;margin-bottom:0.45rem;display:flex;justify-content:space-between;
        align-items:center;flex-wrap:wrap;gap:0.4rem;">
            <div>
                <div style="font-weight:600;font-size:0.92rem;color:#e8ecf1;">{name}</div>
                <div style="font-size:0.75rem;color:#6b7c8f;margin-top:0.15rem;">
                    {qty} · P {p}g · C {c}g · F {f}g
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.7rem;color:{conf_color};">{confidence:.0f}% match</div>
                <div style="font-weight:700;font-size:0.95rem;color:#2dd4a8;">{cal} kcal</div>
            </div>
        </div>
        """.replace("", ""),
        unsafe_allow_html=True,
    )


# Session state
for key, default in (("result", None), ("error", None), ("analyzing", False)):
    if key not in st.session_state:
        st.session_state[key] = default

# Header
st.markdown(
    """
    <div class="app-header">
        <div class="brand">YHealth <span>by TFT</span></div>
        <div class="tagline">AI-Powered Food and Nutrition Analyzer</div>
        <div class="subtitle">Upload or capture a meal image to estimate calories and macros instantly.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

api_ok, api_msg = check_api_health()
pill_cls = "status-ok" if api_ok else "status-err"
st.markdown(
    f'<div class="status-pill {pill_cls}">{"●" if api_ok else "○"} {esc(api_msg)}</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1], gap="medium")

with left:
    st.markdown('<div class="section-title">Photo</div>', unsafe_allow_html=True)
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
            with st.spinner("Analyzing image..."):
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
                    st.session_state["error"] = str(exc)
                    st.session_state["result"] = None
                finally:
                    st.session_state["analyzing"] = False
            st.rerun()
    else:
        st.markdown(
            '<div class="upload-hint-box">Upload JPG, PNG, or WEBP (max 10MB)<br>or use camera</div>'.replace(
                "", ""
            ).replace("", ""),
            unsafe_allow_html=True,
        )

with right:
    if st.session_state.get("analyzing"):
        st.info("Analyzing image...")

    if st.session_state.get("error"):
        st.error(st.session_state["error"])

    if st.session_state.get("result"):
        data = st.session_state["result"]
        total = data["total_macros"]
        items = data["items"]
        conf_map = get_confidence_map(data)

        st.markdown('<div class="section-title">Total nutrition</div>', unsafe_allow_html=True)
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
            st.progress(
                min(1.0, p_pct / 100),
                text=f"Macro split — Protein {p_pct}% · Carbs {c_pct}% · Fat {f_pct}%",
            )

        st.markdown('<div class="section-title">Detected foods</div>', unsafe_allow_html=True)
        for item in items:
            render_food_item(item, conf_map.get(item["name"], 0))

        with st.expander("View API JSON"):
            st.code(json.dumps(api_json_for_display(data), indent=2), language="json")

    elif not st.session_state.get("error") and not st.session_state.get("analyzing"):
        st.markdown(
            """
            <div style="text-align:center;padding:2rem 0.5rem;color:#4a5a6a;">
                <div style="font-size:2rem;margin-bottom:0.4rem;">📋</div>
                <div style="font-size:0.88rem;">Nutrition summary will appear here</div>
                <div style="font-size:0.75rem;margin-top:0.25rem;">Upload a photo and tap Analyze meal</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr><div class="app-footer">YHealth by TFT · Food-101 vision model</div>', unsafe_allow_html=True)
