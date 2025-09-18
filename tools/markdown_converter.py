import streamlit as st
import markdown2
import bleach
from utils.common import setup_page, show_result, handle_file_upload, validate_input, add_footer

# ── HTML Sanitization ──────────────────────────────────────────────────────────
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'strike',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'code', 'pre',
    'a', 'img', 'table', 'thead', 'tbody', 'tr', 'td', 'th'
]
ALLOWED_ATTRS = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'code': ['class']
}

def sanitize_html(html: str) -> str:
    """
    Clean HTML to remove disallowed tags and attributes, preventing XSS.
    """
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True
    )
# ──────────────────────────────────────────────────────────────────────────────

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
                # Convert Markdown to raw HTML
                raw_html = convert_markdown_to_html(md_text)
                # Sanitize the HTML output
                clean_html = sanitize_html(raw_html)

                st.success("✅ Conversion successful!")
                show_result(clean_html, language="html")
                st.download_button(
                    label="📥 Download HTML",
                    data=clean_html,
                    file_name="converted.html",
                    mime="text/html"
                )
            except Exception as e:
                st.error(f"❌ Conversion error: {e}")

    # 4. Footer
    # add_footer()
