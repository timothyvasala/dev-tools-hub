import streamlit as st
import regex as re
from utils.common import setup_page, show_result, add_footer

# ── Cache regex compilation & matching ─────────────────────────────────────────
@st.cache_data(show_spinner=False)
def compile_regex(pattern: str, flags_value: int):
    """Compile the regex pattern with given flags."""
    return re.compile(pattern, flags=flags_value)

@st.cache_data(show_spinner=False)
def find_matches(compiled_regex, text: str):
    """Find all matches of the compiled regex in the text."""
    return compiled_regex.findall(text)
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Header
    setup_page(
        "🔍 Regex Tester",
        "Test and debug regular expressions with sample text."
    )

    # 2. Input pattern and flags
    pattern = st.text_input("Enter regex pattern:", value=r"^\w+$")
    flags = st.multiselect(
        "Flags:",
        options=["IGNORECASE", "MULTILINE", "DOTALL", "VERBOSE"],
        default=[]
    )

    # Map flag names to re constants
    flag_value = 0
    for f in flags:
        flag_value |= getattr(re, f)

    # 3. Sample text
    sample = st.text_area(
        "Sample text to test against:",
        height=200,
        placeholder="Enter text here..."
    )

    # 4. Test button
    if st.button("✅ Test Regex"):
        try:
            compiled = compile_regex(pattern, flag_value)
            matches = find_matches(compiled, sample)
            if matches:
                st.success(f"Found {len(matches)} match(es):")
                for m in matches:
                    show_result(str(m))
            else:
                st.info("No matches found.")
        except Exception as e:
            st.error(f"❌ Regex error: {e}")

    # 5. Export option
    if st.button("📥 Export as Python Code"):
        code = (
            f"import regex as re\n"
            f"pattern = r\"{pattern}\"\n"
            f"flags = {flag_value}\n"
            f"regex = re.compile(pattern, flags=flags)\n"
            f"matches = regex.findall(sample_text)\n"
        )
        show_result(code, language="python")
        st.download_button("Download code", code, "regex_test.py", "text/x-python")

    # 6. Footer
    # add_footer()
