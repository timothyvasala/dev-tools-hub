import streamlit as st
import re
import pandas as pd
from io import StringIO
import json

def show_regex_tester():
    """Enhanced Regex Tester with bulk processing and advanced features"""

    st.title("🔍 Regex Tester")
    st.markdown("*Test and debug regular expressions with sample text*")

    # Input method selection
    input_method = st.radio(
        "**Input Method:**",
        ["Single Text", "Bulk Text", "File Upload"],
        horizontal=True
    )

    # Advanced options in sidebar
    with st.sidebar:
        st.subheader("⚙️ Regex Flags")
        flags = 0
        if st.checkbox("🔍 Case Insensitive (i)", value=False):
            flags |= re.IGNORECASE
        if st.checkbox("🌍 Multiline (m)", value=False):
            flags |= re.MULTILINE
        if st.checkbox("🔘 Dot All (s)", value=False):
            flags |= re.DOTALL
        if st.checkbox("📝 Verbose (x)", value=False):
            flags |= re.VERBOSE

        st.subheader("🎯 Quick Patterns")
        quick_patterns = {
            "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "Phone": r'\b\d{3}-\d{3}-\d{4}\b',
            "URL": r'https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?',
            "IPv4": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            "Date (YYYY-MM-DD)": r'\d{4}-\d{2}-\d{2}',
        }

        selected_pattern = st.selectbox("Choose a pattern:", ["Custom"] + list(quick_patterns.keys()))

    # Pattern input
    if selected_pattern == "Custom":
        pattern = st.text_input(
            "**Enter regex pattern:**",
            value="",
            placeholder="e.g., \\d+|[a-zA-Z]+|\\b\\w+@\\w+\\.\\w+\\b",
            help="Enter your regular expression pattern"
        )
    else:
        pattern = st.text_input(
            "**Enter regex pattern:**",
            value=quick_patterns[selected_pattern],
            help=f"Pre-filled pattern for {selected_pattern}"
        )

    # Text input based on method
    texts_to_test = []

    if input_method == "Single Text":
        test_text = st.text_area(
            "**Sample text to test against:**",
            height=150,
            placeholder="Enter your text here to test the regex pattern...",
            value="Sample text: Contact us at john@example.com or call 123-456-7890. Visit https://example.com for more info."
        )
        if test_text:
            texts_to_test = [test_text]

    elif input_method == "Bulk Text":
        st.info("💡 Enter multiple texts separated by blank lines")
        bulk_text = st.text_area(
            "**Multiple texts to test (separate with blank lines):**",
            height=200,
            placeholder="Text 1 here\n\nText 2 here\n\nText 3 here..."
        )
        if bulk_text:
            texts_to_test = [text.strip() for text in bulk_text.split('\n\n') if text.strip()]

    elif input_method == "File Upload":
        uploaded_file = st.file_uploader(
            "**Upload text file:**",
            type=['txt', 'csv', 'log'],
            help="Upload a text file to test the regex against"
        )
        if uploaded_file:
            try:
                content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
                texts_to_test = [content]
                st.info(f"✅ File loaded: {uploaded_file.name} ({len(content)} characters)")
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")

    # Processing and Results
    if st.button("🚀 Test Regex", type="primary") and pattern:
        if not texts_to_test:
            st.warning("⚠️ Please enter some text to test!")
            return

        # Progress bar for bulk processing
        if len(texts_to_test) > 1:
            progress_bar = st.progress(0)

        try:
            # Compile pattern (NO CACHING - this fixes the error!)
            compiled_pattern = re.compile(pattern, flags)

            all_results = []
            total_matches = 0

            for idx, text in enumerate(texts_to_test):
                # Update progress
                if len(texts_to_test) > 1:
                    progress_bar.progress((idx + 1) / len(texts_to_test))

                # Find all matches (NO CACHE DECORATOR!)
                matches = compiled_pattern.findall(text)
                match_objects = list(compiled_pattern.finditer(text))

                result = {
                    "text_index": idx + 1,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "match_count": len(matches),
                    "matches": matches,
                    "match_positions": [(m.start(), m.end(), m.group()) for m in match_objects]
                }
                all_results.append(result)
                total_matches += len(matches)

            # Display Results
            if total_matches == 0:
                st.warning("🔍 No matches found!")
            else:
                st.success(f"✅ Found {total_matches} total matches!")

                # Results tabs
                tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Detailed Results", "💾 Export"])

                with tab1:
                    # Summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Matches", total_matches)
                    with col2:
                        st.metric("Texts Processed", len(texts_to_test))
                    with col3:
                        st.metric("Pattern Length", len(pattern))
                    with col4:
                        avg_matches = total_matches / len(texts_to_test) if texts_to_test else 0
                        st.metric("Avg Matches/Text", f"{avg_matches:.1f}")

                with tab2:
                    # Detailed results for each text
                    for i, result in enumerate(all_results):
                        if result["match_count"] > 0:
                            with st.expander(f"📄 Text {result['text_index']}: {result['match_count']} matches"):
                                st.write(f"**Text Preview:** {result['text_preview']}")

                                # Show matches with positions
                                matches_df = pd.DataFrame([
                                    {"Match": match[2], "Start": match[0], "End": match[1]}
                                    for match in result["match_positions"]
                                ])
                                st.dataframe(matches_df, use_container_width=True)

                with tab3:
                    # Export options
                    export_data = {
                        "pattern": pattern,
                        "flags": flags,
                        "total_matches": total_matches,
                        "results": all_results
                    }

                    col1, col2 = st.columns(2)

                    with col1:
                        # JSON Export
                        json_data = json.dumps(export_data, indent=2)
                        st.download_button(
                            label="📋 Download JSON",
                            data=json_data,
                            file_name="regex_results.json",
                            mime="application/json"
                        )

                    with col2:
                        # CSV Export (matches only)
                        all_matches = []
                        for result in all_results:
                            for pos in result["match_positions"]:
                                all_matches.append({
                                    "text_index": result["text_index"],
                                    "match": pos[2],
                                    "start_position": pos[0],
                                    "end_position": pos[1]
                                })

                        if all_matches:
                            matches_df = pd.DataFrame(all_matches)
                            csv_data = matches_df.to_csv(index=False)
                            st.download_button(
                                label="📊 Download CSV",
                                data=csv_data,
                                file_name="regex_matches.csv",
                                mime="text/csv"
                            )

        except re.error as e:
            st.error(f"❌ Invalid regex pattern: {e}")
        except Exception as e:
            st.error(f"❌ Error processing regex: {e}")

    elif not pattern:
        st.info("👆 Enter a regex pattern above to get started!")

    # Help section
    with st.expander("📚 Regex Help & Examples"):
        st.markdown("""
        ### 🎯 Common Patterns:
        - **Digits:** `\\d+` (one or more digits)
        - **Letters:** `[a-zA-Z]+` (one or more letters)
        - **Words:** `\\b\\w+\\b` (whole words only)
        - **Email:** `\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b`
        - **Phone:** `\\b\\d{3}-\\d{3}-\\d{4}\\b` (US format)
        - **URL:** `https?://[^\\s]+` (basic URL matching)

        ### 🚩 Flags:
        - **i (Case Insensitive):** Ignore case differences
        - **m (Multiline):** ^ and $ match line boundaries
        - **s (Dot All):** . matches newline characters
        - **x (Verbose):** Allow whitespace and comments in pattern
        """)

if __name__ == "__main__":
    show_regex_tester()
