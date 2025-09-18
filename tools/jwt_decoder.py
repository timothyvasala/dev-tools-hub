import streamlit as st
import jwt
import json
import base64
from utils.common import setup_page, show_result, handle_file_upload, add_footer

# ── Input Limits for JWT Tokens ───────────────────────────────────────────────
MAX_TOKEN_LENGTH = 5000       # maximum characters per token
MAX_TOKENS_BULK = 50          # maximum tokens in bulk mode
# ──────────────────────────────────────────────────────────────────────────────

# ── Cache JWT decoding ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def decode_jwt(token: str) -> tuple[dict, dict]:
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
    setup_page(
        "🔑 JWT Decoder & Debugger",
        "Decode JSON Web Tokens without verifying signatures."
    )

    # Use a form so the Decode button is always visible
    with st.form(key="jwt_form", clear_on_submit=False):
        method = st.radio("Input method:", ["Paste Token", "Upload File", "Bulk Paste"])

        tokens = []
        if method == "Paste Token":
            txt = st.text_area("Paste your JWT token here:", height=100, key="paste_token")
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
            bulk = st.text_area("Enter one token per line:", height=150, key="bulk_token")
            if bulk:
                tokens = [line.strip() for line in bulk.split("\n") if line.strip()]

        submit = st.form_submit_button("🔓 Decode")

    if submit:
        if not tokens:
            st.error("❌ Please provide at least one token to decode.")
            return

        if len(tokens) > MAX_TOKENS_BULK:
            st.error(f"❌ Too many tokens ({len(tokens)}). Max allowed in bulk is {MAX_TOKENS_BULK}.")
            return

        for idx, token in enumerate(tokens, 1):
            if len(token) > MAX_TOKEN_LENGTH:
                st.error(f"❌ Token #{idx} too long ({len(token)} chars). Max allowed is {MAX_TOKEN_LENGTH}.")
                return

            st.markdown(f"**Token #{idx}:**")
            try:
                header, payload = decode_jwt(token)
                show_result(json.dumps(header, indent=2), language="json")
                show_result(json.dumps(payload, indent=2), language="json")
            except Exception as e:
                st.error(f"❌ {e}")

    # add_footer()
