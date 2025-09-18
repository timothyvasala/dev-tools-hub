import streamlit as st
import re
import json
import time
import signal
import re
import json
import time
from utils.common import setup_page, show_result, handle_file_upload, add_footer

# ── ReDoS Protection ─────────────────────────────────────────────────────────
class RegexTimeoutError(Exception):
    pass

def _timeout_handler(signum, frame):
    raise RegexTimeoutError("Regex execution timed out (complex pattern)")

def safe_findall(pattern: str, text: str, flags=0, timeout: int = 5):
    """
    Run re.findall with a timeout to prevent ReDoS attacks.
    """
    # Install the signal handler
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)

    try:
        compiled = re.compile(pattern, flags)
        return compiled.findall(text)
    finally:
        signal.alarm(0)  # Cancel alarm
# ──────────────────────────────────────────────────────────────────────────────

def render():
    """
    Simple, clean Regex Tester - Easy to use like your other tools
    """

    st.title("🔍 Regex Tester")
    st.markdown("*Test and debug regular expressions with sample text*")

    # Simple two-column layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Pattern input with common examples
        pattern = st.text_input(
            "**Enter regex pattern:**",
            value="",
            placeholder="\\d+ or [a-zA-Z]+ or \\w+@\\w+\\.\\w+",
            help="Enter your regular expression pattern"
        )

        # Test string input
        test_string = st.text_area(
            "**Sample text to test against:**",
            value="Sample text: Contact john@example.com or call 123-456-7890. Visit https://example.com",
            height=100,
            help="Enter text to test your regex pattern against"
        )

    with col2:
        # Simple quick patterns
        st.markdown("**🎯 Quick Patterns:**")
        quick_patterns = {
            "Numbers": "\\d+",
            "Words": "\\b[a-zA-Z]+\\b",
            "Email": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
            "Phone": "\\b\\d{3}-\\d{3}-\\d{4}\\b",
            "URL": "https?://[^\\s]+",
        }

        for name, regex in quick_patterns.items():
            if st.button(f"📋 {name}", key=f"quick_{name}", use_container_width=True):
                pattern = regex
                st.rerun()

        # Simple flags
        st.markdown("**⚙️ Options:**")
        ignore_case = st.checkbox("🔤 Ignore Case", help="Case-insensitive matching")
        global_match = st.checkbox("🌐 Find All", value=True, help="Find all matches")

    # Test button
    if st.button("🚀 Test Regex", type="primary", use_container_width=True):
        if not pattern:
            st.error("❌ Please enter a regex pattern!")
            return

        if not test_string:
            st.error("❌ Please enter test text!")
            return

        try:
            # Set flags
            flags = 0
            if ignore_case:
                flags |= re.IGNORECASE

            # Compile pattern
            compiled_pattern = re.compile(pattern, flags)

            if global_match:
                # Find all matches
                try:
                    matches = safe_findall(pattern, test_string, flags)
                except RegexTimeoutError as e:
                    st.error(f"❌ {e}")
                    return
                if matches:
                    st.success(f"✅ **Found {len(matches)} matches!**")

                    # Show matches in a simple list
                    for i, match in enumerate(matches, 1):
                        st.write(f"**Match {i}:** `{match}`")

                    # Simple export options
                    col1, col2 = st.columns(2)

                    with col1:
                        # JSON export
                        export_data = {
                            "pattern": pattern,
                            "matches": matches,
                            "total_matches": len(matches),
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                        json_str = json.dumps(export_data, indent=2)
                        st.download_button(
                            "📋 Download JSON",
                            data=json_str,
                            file_name="regex_results.json",
                            mime="application/json"
                        )

                    with col2:
                        # Python code export
                        python_code = f'''import re

pattern = r"{pattern}"
text = """{test_string}"""

matches = re.findall(pattern, text{', re.IGNORECASE' if ignore_case else ''})
print(f"Found {{len(matches)}} matches: {{matches}}")
'''
                        st.download_button(
                            "🐍 Python Code",
                            data=python_code,
                            file_name="regex_code.py",
                            mime="text/python"
                        )
                else:
                    st.warning("🔍 No matches found!")
            else:
                # Find first match only
                match = compiled_pattern.search(test_string)
                if match:
                    st.success(f"✅ **First match found:** `{match.group()}`")
                    st.info(f"📍 Position: {match.start()}-{match.end()}")
                else:
                    st.warning("🔍 No match found!")

        except re.error as e:
            st.error(f"❌ **Invalid regex pattern:** {str(e)}")
            st.info("💡 Check your pattern syntax and try again")
        except Exception as e:
            st.error(f"❌ **Error:** {str(e)}")

    # Simple help section
    with st.expander("📚 Regex Help"):
        st.markdown("""
        ### 🎯 Common Patterns:
        - `\\d+` - One or more digits (123, 456)
        - `[a-zA-Z]+` - Letters only (hello, World)
        - `\\w+@\\w+\\.\\w+` - Simple email pattern
        - `\\b\\w+\\b` - Whole words only
        - `https?://[^\\s]+` - URLs starting with http/https

        ### 💡 Tips:
        - Use `\\b` for word boundaries
        - Use `+` for one or more, `*` for zero or more
        - Use `[]` to match any character inside brackets
        - Use `\\` to escape special characters
        """)

# Keep compatibility
def show_regex_tester():
    render()

if __name__ == "__main__":
    render()
