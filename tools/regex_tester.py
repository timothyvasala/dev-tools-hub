import streamlit as st
import re
import pandas as pd
from io import StringIO
import json
import time

def show_regex_tester():
    """
    Enhanced Regex Tester - No caching issues, works guaranteed!
    """

    st.title("🔍 Regex Tester")
    st.markdown("*Test and debug regular expressions with sample text*")

    # Create columns for better layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Input method tabs
        tab1, tab2, tab3 = st.tabs(["📝 Single Text", "📄 Bulk Text", "📁 File Upload"])

        texts_to_test = []

        with tab1:
            pattern = st.text_input(
                "**Enter regex pattern:**",
                value="",
                placeholder="\\d+",
                help="Enter your regular expression pattern"
            )

            test_text = st.text_area(
                "**Sample text to test against:**",
                value="Testing 123 with numbers 456 and text. Email: john@example.com Phone: 123-456-7890",
                height=120,
                help="Enter your text to test the regex pattern against"
            )

            if test_text:
                texts_to_test = [test_text]

        with tab2:
            pattern_bulk = st.text_input(
                "**Enter regex pattern:**",
                value="",
                placeholder="\\d+",
                key="bulk_pattern"
            )

            bulk_text = st.text_area(
                "**Multiple texts (separate with double newlines):**",
                placeholder="Text 1 here\n\nText 2 here\n\nText 3 here",
                height=150,
                key="bulk_input"
            )

            if bulk_text:
                texts_to_test = [text.strip() for text in bulk_text.split('\n\n') if text.strip()]
                pattern = pattern_bulk

        with tab3:
            pattern_file = st.text_input(
                "**Enter regex pattern:**",
                value="",
                placeholder="\\d+",
                key="file_pattern"
            )

            uploaded_file = st.file_uploader(
                "**Upload text file:**",
                type=['txt', 'csv', 'log', 'py', 'js', 'html'],
                help="Upload a text file to test regex against"
            )

            if uploaded_file:
                try:
                    content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
                    texts_to_test = [content]
                    pattern = pattern_file
                    st.info(f"✅ File loaded: {uploaded_file.name} ({len(content)} characters)")
                except Exception as e:
                    st.error(f"❌ Error reading file: {e}")

    with col2:
        st.subheader("⚙️ Options")

        # Regex flags
        flags = 0
        flag_options = st.multiselect(
            "**Regex Flags:**",
            ["Case Insensitive (i)", "Multiline (m)", "Dot All (s)", "Verbose (x)"],
            help="Select regex flags to apply"
        )

        if "Case Insensitive (i)" in flag_options:
            flags |= re.IGNORECASE
        if "Multiline (m)" in flag_options:
            flags |= re.MULTILINE
        if "Dot All (s)" in flag_options:
            flags |= re.DOTALL
        if "Verbose (x)" in flag_options:
            flags |= re.VERBOSE

        # Quick patterns
        st.subheader("🎯 Quick Patterns")
        quick_patterns = {
            "Numbers": r'\d+',
            "Words": r'\b\w+\b',
            "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "Phone (US)": r'\b\d{3}-\d{3}-\d{4}\b',
            "URL": r'https?://[^\s]+',
            "IPv4": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            "Date (YYYY-MM-DD)": r'\d{4}-\d{2}-\d{2}',
        }

        selected_pattern = st.selectbox("Choose preset:", ["Custom"] + list(quick_patterns.keys()))
        if selected_pattern != "Custom":
            pattern = quick_patterns[selected_pattern]
            st.code(pattern, language="regex")

    # Main processing section
    st.markdown("---")

    if st.button("🚀 Test Regex", type="primary", use_container_width=True):
        if not pattern:
            st.error("❌ Please enter a regex pattern!")
            return

        if not texts_to_test:
            st.error("❌ Please enter some text to test!")
            return

        # Process without ANY caching - this is the key fix!
        try:
            # Create progress bar for multiple texts
            if len(texts_to_test) > 1:
                progress_bar = st.progress(0)
                status_text = st.empty()

            # Compile pattern fresh each time (NO CACHE!)
            compiled_pattern = re.compile(pattern, flags)

            all_results = []
            total_matches = 0

            for idx, text in enumerate(texts_to_test):
                # Update progress
                if len(texts_to_test) > 1:
                    progress_bar.progress((idx + 1) / len(texts_to_test))
                    status_text.text(f"Processing text {idx + 1} of {len(texts_to_test)}...")

                # Find matches - direct execution, no caching
                matches = compiled_pattern.findall(text)
                match_objects = list(compiled_pattern.finditer(text))

                result = {
                    "text_index": idx + 1,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "full_text": text,
                    "match_count": len(matches),
                    "matches": matches,
                    "positions": [(m.start(), m.end(), m.group()) for m in match_objects]
                }
                all_results.append(result)
                total_matches += len(matches)

            # Clear progress indicators
            if len(texts_to_test) > 1:
                progress_bar.empty()
                status_text.empty()

            # Display results
            if total_matches == 0:
                st.warning("🔍 No matches found!")
                st.info("💡 Try adjusting your regex pattern or check your text.")
            else:
                st.success(f"✅ Found **{total_matches}** total matches across **{len(texts_to_test)}** text(s)!")

                # Results display tabs
                result_tab1, result_tab2, result_tab3 = st.tabs(["📊 Summary", "🔍 Matches", "💾 Export"])

                with result_tab1:
                    # Statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Matches", total_matches)
                    with col2:
                        st.metric("Texts Processed", len(texts_to_test))
                    with col3:
                        st.metric("Pattern Length", len(pattern))
                    with col4:
                        avg_matches = total_matches / len(texts_to_test)
                        st.metric("Avg per Text", f"{avg_matches:.1f}")

                    # Pattern info
                    st.subheader("🎯 Pattern Analysis")
                    st.code(pattern, language="regex")

                    if flags:
                        flag_names = []
                        if flags & re.IGNORECASE: flag_names.append("Case Insensitive")
                        if flags & re.MULTILINE: flag_names.append("Multiline")
                        if flags & re.DOTALL: flag_names.append("Dot All")
                        if flags & re.VERBOSE: flag_names.append("Verbose")
                        st.write(f"**Flags:** {', '.join(flag_names)}")

                with result_tab2:
                    # Detailed match results
                    for result in all_results:
                        if result["match_count"] > 0:
                            with st.expander(f"📄 Text {result['text_index']} - {result['match_count']} matches", expanded=len(all_results)==1):
                                st.write(f"**Text Preview:** {result['text_preview']}")

                                # Show matches in a nice format
                                for i, (start, end, match) in enumerate(result["positions"], 1):
                                    col1, col2, col3 = st.columns([2, 1, 1])
                                    with col1:
                                        st.code(match, language="text")
                                    with col2:
                                        st.write(f"Start: {start}")
                                    with col3:
                                        st.write(f"End: {end}")

                with result_tab3:
                    # Export functionality
                    export_data = {
                        "pattern": pattern,
                        "flags": flags,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "total_matches": total_matches,
                        "results": [
                            {
                                "text_index": r["text_index"],
                                "match_count": r["match_count"],
                                "matches": r["matches"],
                                "positions": r["positions"]
                            } for r in all_results
                        ]
                    }

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        # JSON Export
                        json_str = json.dumps(export_data, indent=2)
                        st.download_button(
                            label="📋 Download JSON",
                            data=json_str,
                            file_name=f"regex_results_{int(time.time())}.json",
                            mime="application/json",
                            use_container_width=True
                        )

                    with col2:
                        # CSV Export
                        csv_data = []
                        for result in all_results:
                            for start, end, match in result["positions"]:
                                csv_data.append({
                                    "text_index": result["text_index"],
                                    "match": match,
                                    "start": start,
                                    "end": end,
                                    "length": len(match)
                                })

                        if csv_data:
                            df = pd.DataFrame(csv_data)
                            csv_str = df.to_csv(index=False)
                            st.download_button(
                                label="📊 Download CSV",
                                data=csv_str,
                                file_name=f"regex_matches_{int(time.time())}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                    with col3:
                        # Python Code Export
                        python_code = f'''import re

# Generated regex pattern
pattern = r"{pattern}"
flags = {flags}

# Compile pattern
compiled_pattern = re.compile(pattern, flags)

# Example usage
text = "Your text here"
matches = compiled_pattern.findall(text)
print(f"Found {{len(matches)}} matches: {{matches}}")
'''
                        st.download_button(
                            label="🐍 Download Python",
                            data=python_code,
                            file_name=f"regex_code_{int(time.time())}.py",
                            mime="text/python",
                            use_container_width=True
                        )

        except re.error as e:
            st.error(f"❌ Invalid regex pattern: {str(e)}")
        except Exception as e:
            st.error(f"❌ Processing error: {str(e)}")

    # Help section
    with st.expander("📚 Regex Help & Examples"):
        st.markdown("""
        ### 🎯 Common Patterns:

        | Pattern | Matches | Example |
        |---------|---------|---------|
        | `\\d+` | One or more digits | `123`, `456` |
        | `[a-zA-Z]+` | Letters only | `hello`, `World` |
        | `\\w+` | Word characters | `hello123`, `test_var` |
        | `\\s+` | Whitespace | spaces, tabs, newlines |
        | `.*` | Any characters | everything |
        | `^` | Start of line | beginning |
        | `$` | End of line | ending |
        | `\\b` | Word boundary | whole words only |

        ### 🚩 Flags:
        - **Case Insensitive (i):** `Hello` matches `hello`
        - **Multiline (m):** `^` and `$` match line boundaries
        - **Dot All (s):** `.` matches newline characters
        - **Verbose (x):** Allow whitespace and comments in pattern

        ### 💡 Tips:
        - Test with simple patterns first
        - Use word boundaries `\\b` for exact word matches
        - Escape special characters with backslash `\\`
        - Use parentheses `()` for grouping
        """)

# Run the function if called directly
if __name__ == "__main__":
    show_regex_tester()
