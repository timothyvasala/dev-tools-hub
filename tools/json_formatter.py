import streamlit as st
import json
from utils.common import setup_page, show_result, handle_file_upload, validate_input, add_footer
import sys
from functools import wraps

# ── Security wrapper for JSON operations ─────────────────────────────────────
def json_security_check(data: str, max_size_mb=10, max_depth=50):
    size_mb = len(data.encode('utf-8')) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise ValueError(f"JSON too large: {size_mb:.1f}MB (max: {max_size_mb}MB)")

    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")

    def check_depth(obj, current_depth=0):
        if current_depth > max_depth:
            raise ValueError(f"JSON too deeply nested: {current_depth} levels (max: {max_depth})")
        if isinstance(obj, dict):
            for value in obj.values():
                check_depth(value, current_depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                check_depth(item, current_depth + 1)

    check_depth(parsed_data)
    return True
# ────────────────────────────────────────────────────────────────────────────────

# ── Cache heavy JSON operations ─────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def format_json(data: str, indent: int, sort_keys: bool, ensure_ascii: bool) -> str:
    json_security_check(data)
    parsed = json.loads(data)
    return json.dumps(parsed, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)

@st.cache_data(show_spinner=False)
def minify_json(data: str) -> str:
    json_security_check(data)
    parsed = json.loads(data)
    return json.dumps(parsed, separators=(',', ':'))
# ────────────────────────────────────────────────────────────────────────────────

def render():
    setup_page(
        "📝 JSON Formatter & Validator",
        "Format, validate, and beautify JSON data with error detection."
    )

    indent, sort_keys, ensure_ascii, raw_json = 2, False, False, ""

    # Layout for options and input
    with st.form(key="json_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            indent = st.selectbox("Indentation:", [2, 4, 8], index=0)
        with col2:
            sort_keys = st.checkbox("Sort keys alphabetically")
        with col3:
            ensure_ascii = st.checkbox("Ensure ASCII output")

        method = st.radio("Input method:", ["Paste JSON", "Upload File"], key="json_method")
        if method == "Paste JSON":
            raw_json = st.text_area(
                "Paste your JSON here:", height=200,
                placeholder='{"name": "Alice", "age": 30}', key="json_paste"
            )
        else:
            content = handle_file_upload(["json", "txt"], max_mb=10)
            if content:
                raw_json = content

        format_btn = st.form_submit_button("✨ Format & Validate")
        minify_btn = st.form_submit_button("🗜️ Minify JSON")

    # Handle formatting
    if raw_json and format_btn:
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

    # Handle minify
    if raw_json and minify_btn:
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

    # add_footer()
