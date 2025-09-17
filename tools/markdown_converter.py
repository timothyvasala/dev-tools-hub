import streamlit as st
import markdown2
from utils.common import setup_page, show_result, handle_file_upload, validate_input, add_footer

# ── Cache Markdown conversion ──────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def convert_markdown_to_html(md_text: str) -> str:
    """Convert Markdown text to HTML."""
    return markdown2.markdown(md_text)
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Header
    setup_page(
        "📄 Markdown → HTML Converter",
        "Convert Markdown text or files into HTML code."
    )

    # 2. Input method
    method = st.radio("Input method:", ["Paste Markdown", "Upload File"])
    md_text = ""

    if method == "Paste Markdown":
        md_text = st.text_area(
            "Enter Markdown content:", height=200,
            placeholder="# Title\n\nSome **bold** text."
        )
    else:
        content = handle_file_upload(["md", "txt"], max_mb=10)
        if content:
            md_text = content

    # 3. Convert button
    if md_text and st.button("🔄 Convert to HTML"):
        valid, msg = validate_input(md_text, min_len=2)
        if not valid:
            st.error(f"❌ {msg}")
        else:
            try:
                html = convert_markdown_to_html(md_text)
                st.success("✅ Conversion successful!")
                show_result(html, language="html")
                st.download_button(
                    label="📥 Download HTML",
                    data=html,
                    file_name="converted.html",
                    mime="text/html"
                )
            except Exception as e:
                st.error(f"❌ Conversion error: {e}")

    # 4. Footer
    # add_footer()
