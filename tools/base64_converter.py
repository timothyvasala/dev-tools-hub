import streamlit as st
import base64
from utils.common import setup_page, show_result, handle_file_upload, validate_input

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
                encoded = base64.b64encode(text.encode()).decode()
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
                    decoded = base64.b64decode(b64).decode()
                    show_result(decoded)
                    st.download_button("📥 Download as .txt", decoded, "decoded.txt", "text/plain")
                except Exception as e:
                    st.error(f"❌ Decoding error: {e}")

    # 5. Encode File
    elif mode == "Encode File":
        content = handle_file_upload(max_mb=5)
        if content and st.button("🔒 Encode File"):
            encoded = base64.b64encode(content.encode()).decode()
            show_result(encoded)
            st.download_button("📥 Download as .txt", encoded, "file_encoded.txt", "text/plain")

    # 6. Decode File
    else:  # mode == "Decode File"
        b64file = handle_file_upload(["txt"], max_mb=5)
        if b64file and st.button("🔓 Decode File"):
            try:
                decoded = base64.b64decode(b64file).decode()
                show_result(decoded)
                st.download_button("📥 Download as .txt", decoded, "file_decoded.txt", "text/plain")
            except Exception as e:
                st.error(f"❌ Decoding error: {e}")

    # 7. Footer
    from utils.common import add_footer
    add_footer()
