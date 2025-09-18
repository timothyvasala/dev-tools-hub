import streamlit as st
import base64
from utils.common import setup_page, show_result, handle_file_upload, validate_input, add_footer

# ── File Type Security ─────────────────────────────────────────────────────────
ALLOWED_FILE_EXTENSIONS = ['.txt', '.json', '.csv', '.md', '.py', '.js', '.html', '.css', '.xml', '.yaml', '.yml']
MAX_FILE_SIZE_MB = 5

def validate_file_for_encoding(filename: str, size_bytes: int):
    """Basic file validation for Base64 encoding"""
    import os

    # Check file extension
    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_FILE_EXTENSIONS:
        raise ValueError(f"File type '{ext}' not allowed. Allowed: {', '.join(ALLOWED_FILE_EXTENSIONS)}")

    # Check file size
    size_mb = size_bytes / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"File too large: {size_mb:.1f}MB (max: {MAX_FILE_SIZE_MB}MB)")
# ──────────────────────────────────────────────────────────────────────────────

# ── Cache Base64 operations ────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def encode_text(data: str) -> str:
    return base64.b64encode(data.encode()).decode()

@st.cache_data(show_spinner=False)
def decode_text(data: str) -> str:
    return base64.b64decode(data).decode()

@st.cache_data(show_spinner=False)
def encode_file_content(data: str) -> str:
    return base64.b64encode(data.encode()).decode()

@st.cache_data(show_spinner=False)
def decode_file_content(data: str) -> str:
    return base64.b64decode(data).decode()
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Header
    setup_page(
        "🔤 Base64 Encoder / Decoder",
        "Encode text/files to Base64 or decode Base64 to text."
    )

    # 2. Input method
    mode = st.radio("Mode:", ["Encode Text", "Decode Text", "Encode File", "Decode File"])

    # 3. Encode Text
    if mode == "Encode Text":
        text = st.text_area("Enter text to encode:", height=150)
        if st.button("🔒 Encode Text"):
            valid, msg = validate_input(text)
            if not valid:
                st.error(f"❌ {msg}")
            else:
                encoded = encode_text(text)
                show_result(encoded)
                st.download_button("📥 Download as .txt", encoded, "encoded.txt", "text/plain")

    # 4. Decode Text
    elif mode == "Decode Text":
        b64 = st.text_area("Enter Base64 text to decode:", height=150)
        if st.button("🔓 Decode Text"):
            valid, msg = validate_input(b64)
            if not valid:
                st.error(f"❌ {msg}")
            else:
                try:
                    decoded = decode_text(b64)
                    show_result(decoded)
                    st.download_button("📥 Download as .txt", decoded, "decoded.txt", "text/plain")
                except Exception as e:
                    st.error(f"❌ Decoding error: {e}")

    # 5. Encode File
    elif mode == "Encode File":
        content = handle_file_upload(max_mb=10)
        if content and st.button("🔒 Encode File"):
            encoded = encode_file_content(content)
            show_result(encoded)
            st.download_button("📥 Download as .txt", encoded, "file_encoded.txt", "text/plain")

    # 6. Decode File
    else:  # mode == "Decode File"
        b64file = handle_file_upload(["txt"], max_mb=10)
        if b64file and st.button("🔓 Decode File"):
            try:
                decoded = decode_file_content(b64file)
                show_result(decoded)
                st.download_button("📥 Download as .txt", decoded, "file_decoded.txt", "text/plain")
            except Exception as e:
                st.error(f"❌ Decoding error: {e}")

    # 7. Footer
    # add_footer()
