import streamlit as st
import jwt
import json
import base64
from utils.common import setup_page, show_result, handle_file_upload

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
        content = handle_file_upload(["txt","json"], max_mb=2)
        if content:
            # Try JSON array else newline-split
            try:
                arr = json.loads(content)
                tokens = arr if isinstance(arr, list) else [str(arr)]
            except:
                tokens = [line.strip() for line in content.split("\n") if line.strip()]

    else:  # Bulk Paste
        bulk = st.text_area("Enter one token per line:", height=150)
        if bulk:
            tokens = [line.strip() for line in bulk.split("\n") if line.strip()]

    # 3. Decode button
    if tokens and st.button("🔓 Decode"):
        for idx, token in enumerate(tokens, 1):
            st.markdown(f"**Token #{idx}:**")
            parts = token.split(".")
            if len(parts) != 3:
                st.error("❌ Invalid JWT format (must have 3 segments).")
                continue

            header_b64, payload_b64, _ = parts
            # Fix padding
            def fix(b): return b + "=" * (-len(b) % 4)

            try:
                # Decode header
                header = json.loads(base64.urlsafe_b64decode(fix(header_b64)))
                show_result(json.dumps(header, indent=2), language="json")

                # Decode payload
                payload = json.loads(base64.urlsafe_b64decode(fix(payload_b64)))
                show_result(json.dumps(payload, indent=2), language="json")

            except Exception as e:
                st.error(f"❌ Error decoding token: {e}")

    # 4. Footer
    from utils.common import add_footer
    add_footer()
