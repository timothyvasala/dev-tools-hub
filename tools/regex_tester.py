import streamlit as st
import re
import json
import time

def render():
    """
    Professional Regex Tester - Matches industry standards like regex101.com and regexr.com
    """

    st.title("🔍 Regex Tester")
    st.markdown("*Test and debug regular expressions with real-time highlighting*")

    # Create two-column layout like professional tools
    col1, col2 = st.columns([3, 2])

    with col1:
        # Pattern input with quick examples
        st.subheader("🎯 Regular Expression")

        # Quick pattern selection
        quick_patterns = {
            "Custom Pattern": "",
            "Email Address": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "Phone Number (US)": r'\b\d{3}-\d{3}-\d{4}\b',
            "URL/Website": r'https?://[^\s]+',
            "Numbers Only": r'\d+',
            "Words Only": r'\b[a-zA-Z]+\b',
            "IPv4 Address": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            "Date (YYYY-MM-DD)": r'\d{4}-\d{2}-\d{2}',
            "Hexadecimal Color": r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})',
        }

        selected_example = st.selectbox("Choose a pattern or enter custom:", list(quick_patterns.keys()))

        if selected_example == "Custom Pattern":
            pattern = st.text_input(
                "Enter your regex pattern:",
                value="",
                placeholder="\\d+ or [a-zA-Z]+ or \\b\\w+@\\w+\\.\\w+\\b",
                help="Enter your regular expression pattern"
            )
        else:
            pattern = st.text_input(
                "Regex pattern:",
                value=quick_patterns[selected_example],
                help=f"Pre-filled pattern for {selected_example}"
            )

        # Test string input
        st.subheader("📝 Test String")
        test_string = st.text_area(
            "Enter text to test against:",
            value="Sample text: Contact john@example.com or call 123-456-7890. Visit https://example.com or check IP 192.168.1.1. Today is 2024-09-17 and color is #FF5733.",
            height=120,
            help="Enter the text you want to test your regex pattern against"
        )

    with col2:
        # Regex flags (like regex101.com)
        st.subheader("⚙️ Flags")

        flags = 0
        flag_g = st.checkbox("🌐 Global (g)", value=True, help="Find all matches, not just the first")
        flag_i = st.checkbox("🔤 Ignore Case (i)", value=False, help="Case-insensitive matching")
        flag_m = st.checkbox("📄 Multiline (m)", value=False, help="^ and $ match line boundaries")
        flag_s = st.checkbox("🔘 Dot All (s)", value=False, help=". matches newline characters")

        if flag_i:
            flags |= re.IGNORECASE
        if flag_m:
            flags |= re.MULTILINE
        if flag_s:
            flags |= re.DOTALL

        # Function selection
        st.subheader("🔧 Function")
        function_type = st.selectbox(
            "Regex function:",
            ["Match", "Search", "Find All", "Split", "Substitute"],
            help="Choose what operation to perform"
        )

        if function_type == "Substitute":
            replacement = st.text_input("Replacement:", value="[MATCH]", help="Replacement string for substitution")

    # Processing section
    st.markdown("---")

    # Test button
    if st.button("🚀 Test Regex", type="primary", use_container_width=True):
        if not pattern:
            st.error("❌ Please enter a regex pattern!")
            return

        if not test_string:
            st.error("❌ Please enter test text!")
            return

        try:
            # Compile pattern (no caching to avoid errors)
            compiled_pattern = re.compile(pattern, flags)

            # Execute based on function type
            if function_type == "Match":
                match = compiled_pattern.match(test_string)
                if match:
                    st.success(f"✅ **Match found!** `{match.group()}`")
                    st.info(f"📍 Position: {match.start()}-{match.end()}")
                else:
                    st.warning("🔍 No match at string beginning")

            elif function_type == "Search":
                match = compiled_pattern.search(test_string)
                if match:
                    st.success(f"✅ **First match found!** `{match.group()}`")
                    st.info(f"📍 Position: {match.start()}-{match.end()}")
                else:
                    st.warning("🔍 No match found anywhere")

            elif function_type == "Find All":
                matches = compiled_pattern.findall(test_string)
                if matches:
                    st.success(f"✅ **Found {len(matches)} matches!**")

                    # Display matches in a nice format
                    for i, match in enumerate(matches, 1):
                        st.write(f"**Match {i}:** `{match}`")

                    # Get detailed match information
                    match_objects = list(compiled_pattern.finditer(test_string))

                    # Create results table
                    if match_objects:
                        st.subheader("📊 Match Details")
                        results_data = []
                        for i, match in enumerate(match_objects, 1):
                            results_data.append({
                                "Match #": i,
                                "Text": match.group(),
                                "Start": match.start(),
                                "End": match.end(),
                                "Length": len(match.group())
                            })

                        st.table(results_data)

                        # Export functionality
                        st.subheader("💾 Export Results")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            # JSON export
                            export_data = {
                                "pattern": pattern,
                                "flags": flags,
                                "test_string": test_string,
                                "matches": matches,
                                "match_details": results_data,
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                            }
                            json_str = json.dumps(export_data, indent=2)
                            st.download_button(
                                "📋 JSON",
                                data=json_str,
                                file_name="regex_results.json",
                                mime="application/json"
                            )

                        with col2:
                            # Python code export
                            python_code = f'''import re

# Regex pattern
pattern = r"{pattern}"
flags = {flags}

# Test string
test_string = """{test_string}"""

# Compile and execute
compiled_pattern = re.compile(pattern, flags)
matches = compiled_pattern.findall(test_string)

print(f"Found {{len(matches)}} matches:")
for i, match in enumerate(matches, 1):
    print(f"Match {{i}}: {{match}}")
'''
                            st.download_button(
                                "🐍 Python",
                                data=python_code,
                                file_name="regex_code.py",
                                mime="text/python"
                            )

                        with col3:
                            # Text export
                            text_output = f"Regex Pattern: {pattern}\nTest String: {test_string}\n\nMatches Found: {len(matches)}\n\n"
                            for i, match in enumerate(matches, 1):
                                text_output += f"Match {i}: {match}\n"

                            st.download_button(
                                "📄 Text",
                                data=text_output,
                                file_name="regex_results.txt",
                                mime="text/plain"
                            )
                else:
                    st.warning("🔍 No matches found")

            elif function_type == "Split":
                parts = compiled_pattern.split(test_string)
                st.success(f"✅ **Split into {len(parts)} parts:**")
                for i, part in enumerate(parts, 1):
                    if part:  # Only show non-empty parts
                        st.write(f"**Part {i}:** `{part}`")

            elif function_type == "Substitute":
                result = compiled_pattern.sub(replacement, test_string)
                st.success("✅ **Substitution result:**")
                st.code(result, language="text")

                # Show number of replacements
                count = len(compiled_pattern.findall(test_string))
                st.info(f"📊 Made {count} replacement(s)")

        except re.error as e:
            st.error(f"❌ **Invalid regex pattern:** {str(e)}")
            st.info("💡 Check your pattern syntax and try again")
        except Exception as e:
            st.error(f"❌ **Error:** {str(e)}")

    # Help section (like regex101.com)
    with st.expander("📚 Regex Reference & Help"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 🎯 **Common Patterns**
            | Pattern | Matches |
            |---------|---------|
            | `\\d` | Any digit (0-9) |
            | `\\w` | Word character (a-z, A-Z, 0-9, _) |
            | `\\s` | Whitespace (space, tab, newline) |
            | `.` | Any character (except newline) |
            | `^` | Start of string/line |
            | `$` | End of string/line |
            | `\\b` | Word boundary |

            ### 🔢 **Quantifiers**
            | Pattern | Matches |
            |---------|---------|
            | `*` | 0 or more |
            | `+` | 1 or more |
            | `?` | 0 or 1 |
            | `{n}` | Exactly n |
            | `{n,m}` | Between n and m |
            """)

        with col2:
            st.markdown("""
            ### 📦 **Groups & Classes**
            | Pattern | Matches |
            |---------|---------|
            | `[abc]` | Any of a, b, or c |
            | `[^abc]` | Not a, b, or c |
            | `[a-z]` | Any lowercase letter |
            | `[A-Z]` | Any uppercase letter |
            | `[0-9]` | Any digit |
            | `(abc)` | Group |
            | `(?:abc)` | Non-capturing group |

            ### 🚩 **Flags**
            | Flag | Effect |
            |------|--------|
            | `i` | Ignore case |
            | `m` | Multiline mode |
            | `s` | Dot matches newline |
            | `g` | Global (find all) |
            """)

# Alternative function name for compatibility
def show_regex_tester():
    render()

if __name__ == "__main__":
    render()
