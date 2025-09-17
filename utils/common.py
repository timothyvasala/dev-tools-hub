import streamlit as st
import re
import json
import logging
from datetime import datetime

# ── Content Security Policy ────────────────────────────────────────────────────
CSP_META = (
    "<meta http-equiv='Content-Security-Policy' "
    "content=\"default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; "
    "font-src 'self';\">"
)
st.markdown(CSP_META, unsafe_allow_html=True)
# ────────────────────────────────────────────────────────────────────────────────

def setup_page(title, description=""):
    """
    Render a consistent header for each tool page.
    - title: Displayed as the tool's main heading.
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
    Display the tool's result in a code block.
    - result: The text to display.
    - language: Syntax highlighting (e.g., 'json', 'html', 'css').
    """
    st.code(result, language=language)

def handle_file_upload(allowed_types=None, max_mb=10):
    """
    Secure file uploader with enhanced validation.
    - allowed_types: List of extensions, e.g. ['txt','json'].
    - max_mb: Maximum file size in megabytes.
    """
    allowed = allowed_types or ["txt", "json", "csv", "md"]
    file = st.file_uploader("Or upload a file:", type=allowed)

    if not file:
        return None

    # Enhanced size validation
    size_mb = file.size / (1024 * 1024)
    if size_mb > max_mb:
        st.error(f"❌ File too large ({size_mb:.1f} MB). Max allowed is {max_mb} MB.")
        return None

    # Sanitize filename - only allow alphanumeric, spaces, hyphens, and valid extensions
    if not re.match(r'^[\w,\s-]+\.[A-Za-z]{1,5}$', file.name):
        st.error("❌ Invalid filename. Use only letters, numbers, spaces, and hyphens.")
        return None

    # Log file upload for monitoring
    logging.info(f"File uploaded: {file.name} ({size_mb:.1f} MB)")

    try:
        text = file.read().decode("utf-8")
        return text
    except UnicodeDecodeError:
        st.error("❌ Unable to decode file. Ensure it's a valid UTF-8 text file.")
        return None
    except Exception as e:
        st.error("❌ Could not read file. Please try again.")
        logging.error(f"File read error: {str(e)}")
        return None

def validate_input(text, min_len=1, max_len=1_000_000):
    """
    Validate text input length with enhanced checks.
    Returns (is_valid, message).
    """
    if not text or not text.strip():
        return False, "Input cannot be empty."

    stripped_len = len(text.strip())
    if stripped_len < min_len:
        return False, f"Input too short (min {min_len} chars)."
    if len(text) > max_len:
        return False, f"Input too long (max {max_len:,} chars)."

    return True, "Valid input."

def add_footer():
    """
    Render a consistent footer on every page.
    """
    st.markdown("---")
    year = datetime.now().year
    st.markdown(f"""
    <div style="text-align:center; color:#666; margin-top:2rem;">
      © {year} DevTools Hub • Made with ❤️ for developers • Free Forever
    </div>
    """, unsafe_allow_html=True)


# Initialize logging for security monitoring
logging.basicConfig(
    filename='devtools_hub.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
