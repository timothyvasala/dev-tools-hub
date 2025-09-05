import streamlit as st
import regex as re
from utils.common import setup_page, show_result

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
            regex = re.compile(pattern, flags=flag_value)
            matches = regex.findall(sample)
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
        code = f"import regex as re\npattern = r\"{pattern}\"\nflags = {flag_value}\nregex = re.compile(pattern, flags=flags)\nmatches = regex.findall(sample_text)\n"
        show_result(code, language="python")
        st.download_button("Download code", code, "regex_test.py", "text/x-python")

    # 6. Footer
    from utils.common import add_footer
    add_footer()
