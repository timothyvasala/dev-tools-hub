import streamlit as st
import jwt
import json
import base64
from utils.common import setup_page, show_result, handle_file_upload, add_footer

# ── Cache JWT decoding ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def decode_jwt(token: str) -> tuple[dict, dict]:
    """
    Decode JWT header and payload without verifying signature.
    Returns (header_dict, payload_dict).
    Raises on invalid format or decode errors.
    """
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format (must have 3 segments).")

    def fix_padding(segment: str) -> str:
        return segment + "=" * (-len(segment) % 4)

    header_b64, payload_b64, _ = parts
    header = json.loads(base64.urlsafe_b64decode(fix_padding(header_b64)))
    payload = json.loads(base64.urlsafe_b64decode(fix_padding(payload_b64)))
    return header, payload
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Page header
    setup_page(
        "🔑 JWT Decoder & Debugger",
        "Decode JSON Web Tokens without verifying signatures."
    )

    # 2. Choose input method
    method = st.radio("Input method:", ["Paste Token", "Upload File", "Bulk Paste"])

    tokens = []
    if method == "Paste Token":
        txt = st.text_area("Paste your JWT token here:", height=100)
        if txt:
            tokens = [txt.strip()]

    elif method == "Upload File":
        content = handle_file_upload(["txt", "json"], max_mb=5)
        if content:
            try:
                arr = json.loads(content)
                tokens = arr if isinstance(arr, list) else [str(arr)]
            except json.JSONDecodeError:
                tokens = [line.strip() for line in content.split("\n") if line.strip()]

    else:  # Bulk Paste
        bulk = st.text_area("Enter one token per line:", height=150)
        if bulk:
            tokens = [line.strip() for line in bulk.split("\n") if line.strip()]

    # 3. Decode button
    if tokens and st.button("🔓 Decode"):
        for idx, token in enumerate(tokens, 1):
            st.markdown(f"**Token #{idx}:**")
            try:
                header, payload = decode_jwt(token)
                show_result(json.dumps(header, indent=2), language="json")
                show_result(json.dumps(payload, indent=2), language="json")
            except Exception as e:
                st.error(f"❌ {e}")

    # 4. Footer
    add_footer()
