import streamlit as st
import sys
from pathlib import Path

# Version info
__version__ = "1.0.0"

# Ensure project root is in path
sys.path.append(str(Path(__file__).parent))

# Import modules
from tools import (
    jwt_decoder, json_formatter, timestamp_converter,
    uuid_generator, base64_converter, url_encoder,
    regex_tester, markdown_converter,
    color_palette, robots_generator
)
from utils.common import add_footer

# ── 1. Configure page BEFORE any markdown──
st.set_page_config(
    page_title="DevTools Hub - Free Developer Utilities",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# ── 2. Inject Global CSS for theming ────────────────────────────────────────────
st.markdown(
    """
    <style>
      .main-header { text-align:center; color:#00d4aa; font-size:2.5rem; margin-bottom:0.5rem; }
      .sub-header  { text-align:center; color:#fafafa; font-size:1.2rem; margin-bottom:2rem; }
      .tool-card   { background:#262730; padding:1rem; border-radius:0.5rem; margin:0.5rem 0; border-left:4px solid #00d4aa; }
      .stButton > button {
        background:#262730 !important;
        border:1px solid transparent !important;
        border-left:4px solid #00d4aa !important;
        color:#fafafa !important;
        padding:1.5rem !important;
        border-radius:0.5rem !important;
        text-align:left !important;
        width:100% !important;
        height:auto !important;
        transition: all 0.3s ease !important;
      }
      .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 170, 0.3) !important;
        border: 1px solid #00d4aa !important;
        background:#2a2d3a !important;
      }
      .back-button { background: #00d4aa; color: #0e1117; border: none; padding: 8px 16px; border-radius: 4px; margin-bottom: 1rem; }
    </style>
    """,
    unsafe_allow_html=True
)
# ────────────────────────────────────────────────────────────────────────────────

# ── SEO & Social Metadata ──────────────────────────────────────────────────────
st.markdown(
    """
    <meta property="og:title" content="DevTools Hub – Free Developer Utilities" />
    <meta property="og:description" content="Professional developer tools: JWT decoder, JSON formatter, Base64 converter, and more. Free & unlimited usage." />
    <meta property="og:image" content="https://raw.githubusercontent.com/timothyvasala/dev-tools-hub/main/static/devtools-logo.png" />
    <meta property="og:url" content="https://devtools-hub.streamlit.app" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="DevTools Hub – Free Developer Utilities" />
    <meta name="twitter:description" content="Professional developer tools: JWT decoder, JSON formatter, Base64 converter, and more." />
    <meta name="twitter:image" content="https://raw.githubusercontent.com/timothyvasala/dev-tools-hub/main/static/devtools-logo.png" />
    """,
    unsafe_allow_html=True
)
# ────────────────────────────────────────────────────────────────────────────────

# Initialize session state
if 'current_tool' not in st.session_state:
    st.session_state.current_tool = 'home'

def render_home_page():
    """Render the home page with clickable tool cards"""

    st.markdown("## 🛠️ Available Tools")

    # Search functionality
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        search_term = st.text_input("", placeholder="🔍 Search tools...", key="search_tools")

    st.markdown("Select any tool below. All tools support bulk operations, file uploads, and instant downloads.")

    # Tools information
    tools_info = [
        ("🔑 JWT Decoder", "Decode JSON Web Tokens without verification", "jwt"),
        ("📝 JSON Formatter", "Format, validate, and beautify JSON data", "json"),
        ("⏰ Timestamp Converter", "Convert Unix timestamps to human dates", "timestamp"),
        ("🆔 UUID Generator", "Generate unique identifiers in bulk", "uuid"),
        ("🔤 Base64 Converter", "Encode/decode text and files to Base64", "base64"),
        ("🔗 URL Encoder", "Encode special characters for URLs", "url"),
        ("🔍 Regex Tester", "Test regular expressions with sample text", "regex"),
        ("📄 Markdown Converter", "Convert Markdown to HTML instantly", "markdown"),
        ("🎨 Color Palette", "Generate colors and check WCAG contrast", "color"),
        ("🤖 Robots.txt Generator", "Create robots.txt for search engines", "robots")
    ]

    # Filter tools based on search
    if search_term:
        filtered_tools = [tool for tool in tools_info if search_term.lower() in tool[0].lower() or search_term.lower() in tool[1].lower()]
    else:
        filtered_tools = tools_info

    # Create tool cards in a grid
    col1, col2 = st.columns(2)

    for i, (title, desc, key) in enumerate(filtered_tools):
        col = col1 if i % 2 == 0 else col2

        with col:
            # Create a tall, styled button with title and description
            button_content = f"""### {title}

{desc}"""

            if st.button(button_content, key=f"btn_{key}", use_container_width=True):
                st.session_state.current_tool = key
                st.rerun()

    if not filtered_tools:
        st.info("No tools found matching your search.")

    st.markdown("---")
    st.markdown("### ✨ Features")

    features_col1, features_col2 = st.columns(2)

    with features_col1:
        st.markdown("""
        • **Free & Unlimited** - No registration required
        • **File Upload Support** - Process files directly
        • **Bulk Operations** - Handle multiple inputs
        • **Instant Downloads** - Get results as files
        • **Mobile Friendly** - Works on all devices
        """)

    with features_col2:
        st.markdown("""
        • **Privacy Focused** - No data stored
        • **Open Source** - MIT licensed on GitHub
        • **Fast & Cached** - Optimized performance
        • **Developer Made** - By developers, for developers
        • **Always Updated** - Regular improvements
        """)

def main():
    # 3. Use your styled headers
    st.markdown('<div class="main-header">DevTools Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional, free developer utilities</div>', unsafe_allow_html=True)

    # Back to home button (only show when not on home)
    if st.session_state.current_tool != 'home':
        if st.button("← Back to Home", key="back_home"):
            st.session_state.current_tool = 'home'
            st.rerun()

    # 4. Wrap each tool render in a styled div
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)

    # Route to current tool
    if st.session_state.current_tool == 'home':
        render_home_page()
    elif st.session_state.current_tool == 'jwt':
        jwt_decoder.render()
    elif st.session_state.current_tool == 'json':
        json_formatter.render()
    elif st.session_state.current_tool == 'timestamp':
        timestamp_converter.render()
    elif st.session_state.current_tool == 'uuid':
        uuid_generator.render()
    elif st.session_state.current_tool == 'base64':
        base64_converter.render()
    elif st.session_state.current_tool == 'url':
        url_encoder.render()
    elif st.session_state.current_tool == 'regex':
        regex_tester.render()
    elif st.session_state.current_tool == 'markdown':
        markdown_converter.render()
    elif st.session_state.current_tool == 'color':
        color_palette.render()
    elif st.session_state.current_tool == 'robots':
        robots_generator.render()

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    add_footer()

if __name__ == "__main__":
    main()
