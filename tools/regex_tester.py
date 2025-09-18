import streamlit as st
import re
import json
import time
import signal
from utils.common import setup_page, show_result, handle_file_upload, add_footer

# ── ReDoS Protection ─────────────────────────────────────────────────────────
class RegexTimeoutError(Exception):
    pass

def _timeout_handler(signum, frame):
    raise RegexTimeoutError("Regex execution timed out (complex pattern)")

def safe_findall(pattern: str, text: str, flags=0, timeout: int = 5):
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)
    try:
        compiled = re.compile(pattern, flags)
        return compiled.findall(text)
    finally:
        signal.alarm(0)
# ──────────────────────────────────────────────────────────────────────────────

def render():
    setup_page(
        "🔍 Regex Tester",
        "Test and debug regular expressions with sample text."
    )

    # Quick pattern dropdown integrated above input
    quick_patterns = {
        "Custom": "",
        "Numbers": r"\d+",
        "Words": r"\b[a-zA-Z]+\b",
        "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "Phone": r"\b\d{3}-\d{3}-\d{4}\b",
        "URL": r"https?://[^\s]+",
    }
    choice = st.selectbox("🎯 Quick Patterns", options=list(quick_patterns.keys()), index=0)
    default_pattern = quick_patterns[choice]
    pattern = st.text_input(
        "Enter Regex Pattern:",
        value=default_pattern,
        placeholder=r"\d+ or [a-zA-Z]+",
    )

    # Main test string
    test_string = st.text_area(
        "Test String:",
        value="Sample text: Contact john@example.com or call 123-456-7890.",
        height=150,
    )

    # Options section below inputs
    st.markdown("---")
    st.subheader("⚙️ Options")
    ignore_case = st.checkbox("🔤 Ignore Case", value=False)
    global_match = st.checkbox("🌐 Find All", value=True)

    # Test button
    if st.button("🚀 Test Regex", use_container_width=True):
        if not pattern:
            st.error("❌ Please enter a regex pattern!")
        elif not test_string:
            st.error("❌ Please enter test text!")
        else:
            flags = re.IGNORECASE if ignore_case else 0
            try:
                if global_match:
                    try:
                        matches = safe_findall(pattern, test_string, flags)
                    except RegexTimeoutError as e:
                        st.error(f"❌ {e}")
                        return
                    if matches:
                        st.success(f"✅ Found {len(matches)} matches!")
                        for i, m in enumerate(matches, 1):
                            st.text(f"{i}: {m}")
                    else:
                        st.warning("🔍 No matches found!")
                else:
                    match = re.compile(pattern, flags).search(test_string)
                    if match:
                        st.success(f"✅ Match: {match.group()}")
                        st.text(f"Position: {match.start()}–{match.end()}")
                    else:
                        st.warning("🔍 No match found!")
            except re.error as e:
                st.error(f"❌ Invalid pattern: {e}")

    add_footer()

if __name__ == "__main__":
    render()
