import streamlit as st
import json
from utils.common import setup_page, show_result, handle_file_upload, validate_input, add_footer

# ── Cache heavy JSON operations ─────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def format_json(data: str, indent: int, sort_keys: bool, ensure_ascii: bool) -> str:
    parsed = json.loads(data)
    return json.dumps(parsed, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)

@st.cache_data(show_spinner=False)
def minify_json(data: str) -> str:
    parsed = json.loads(data)
    return json.dumps(parsed, separators=(',', ':'))
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Page header
    setup_page(
        "📝 JSON Formatter & Validator",
        "Format, validate, and beautify JSON data with error detection."
    )

    # 2. Formatting options
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        indent = st.selectbox("Indentation:", [2, 4, 8], index=0)
    with col2:
        sort_keys = st.checkbox("Sort keys alphabetically")
    with col3:
        ensure_ascii = st.checkbox("Ensure ASCII output")

    # 3. Input methods
    method = st.radio("Input method:", ["Paste JSON", "Upload File"])
    raw_json = ""
    if method == "Paste JSON":
        raw_json = st.text_area(
            "Paste your JSON here:", height=200,
            placeholder='{"name": "Alice", "age": 30, "city": "NY"}'
        )
    else:
        content = handle_file_upload(["json", "txt"], max_mb=10)
        if content:
            raw_json = content

    # 4. Process JSON
    if raw_json and st.button("✨ Format & Validate"):
        is_valid, msg = validate_input(raw_json, min_len=2)
        if not is_valid:
            st.error(f"❌ {msg}")
        else:
            try:
                formatted = format_json(raw_json, indent, sort_keys, ensure_ascii)
                st.success("✅ Valid JSON!")
                show_result(formatted, language="json")
                st.download_button(
                    label="📥 Download JSON",
                    data=formatted,
                    file_name="formatted.json",
                    mime="application/json"
                )
            except json.JSONDecodeError as e:
                st.error(f"❌ JSON Decode Error: {e.msg}")
                if hasattr(e, 'lineno'):
                    st.info(f"Error at line {e.lineno}, column {e.colno}")
            except Exception as e:
                st.error(f"❌ Unexpected Error: {e}")

    # Optional: Minify JSON
    if raw_json and st.button("🗜️ Minify JSON"):
        try:
            minified = minify_json(raw_json)
            st.success("✅ JSON Minified!")
            show_result(minified, language="json")
            st.download_button(
                label="📥 Download Minified",
                data=minified,
                file_name="minified.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"❌ Error Minifying JSON: {e}")

    # 5. Footer
    add_footer()
