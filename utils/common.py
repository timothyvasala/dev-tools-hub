import streamlit as st

def setup_page(title, description=""):
    """
    Render a consistent header for each tool page.
    - title: Displayed as the tool’s main heading.
    - description: Short blurb explaining the tool.
    """
    st.markdown(f"""
    <div style="background: #262730; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #00d4aa; margin-bottom:1rem;">
        <h2 style="color: #00d4aa; margin: 0;">{title}</h2>
        <p style="color: #b0b0b0; margin: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def show_result(result, language="text"):
    """
    Display the tool’s result in a code block.
    - result: The text to display.
    - language: Syntax highlighting (e.g., 'json', 'html', 'css').
    """
    st.code(result, language=language)

def handle_file_upload(allowed_types=None, max_mb=5):
    """
    Provide a file uploader and return its decoded text.
    - allowed_types: List of extensions, e.g. ['txt','json'].
    - max_mb: Maximum file size in megabytes.
    """
    allowed = allowed_types or ["txt", "json", "csv", "md"]
    file = st.file_uploader("Or upload a file:", type=allowed)
    if file:
        if file.size > max_mb * 1024 * 1024:
            st.error(f"File too large (max {max_mb} MB).")
            return None
        try:
            text = file.read().decode("utf-8")
            return text
        except Exception:
            st.error("Could not decode file. Ensure it’s a valid text file.")
            return None
    return None

def validate_input(text, min_len=1, max_len=1_000_000):
    """
    Validate text input length.
    Returns (is_valid, message).
    """
    if not text:
        return False, "Input cannot be empty."
    if len(text) < min_len:
        return False, f"Input too short (min {min_len} chars)."
    if len(text) > max_len:
        return False, f"Input too long (max {max_len:,} chars)."
    return True, "Valid input."

def add_footer():
    """
    Render a consistent footer on every page.
    """
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#666; margin-top:2rem;">
      Made with ❤️ by DevTools Hub • <a href="https://github.com/your-username/dev-tools-hub" target="_blank">Star on GitHub</a> • Free Forever
    </div>
    """, unsafe_allow_html=True)
