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
# ────────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def convert_markdown_to_html(md_text: str) -> str:
    """Convert Markdown text to HTML."""
    return markdown2.markdown(md_text)

def render():
    setup_page(
        "📄 Markdown → HTML Converter",
        "Convert Markdown text or files into HTML code."
    )

    raw_md = ""

    # Wrap inputs and buttons in a form so buttons are always visible
    with st.form("md_form", clear_on_submit=False):
        method = st.radio("Input method:", ["Paste Markdown", "Upload File"], key="md_method")
        if method == "Paste Markdown":
            raw_md = st.text_area(
                "Enter Markdown content:", height=200,
                placeholder="# Title\n\nSome **bold** text.", key="md_paste"
            )
        else:
            content = handle_file_upload(["md", "txt"], max_mb=10)
            if content:
                raw_md = content

        convert_btn = st.form_submit_button("🔄 Convert to HTML")

    if convert_btn:
        if not raw_md or not raw_md.strip():
            st.error("❌ Please enter or upload some Markdown before converting.")
        else:
            is_valid, msg = validate_input(raw_md, min_len=2)
            if not is_valid:
                st.error(f"❌ {msg}")
            else:
                try:
                    raw_html = convert_markdown_to_html(raw_md)
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

    # add_footer()

if __name__ == "__main__":
    render()
