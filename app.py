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
    initial_sidebar_state="expanded"
)

# ── 2. Inject Global CSS for theming ────────────────────────────────────────────
st.markdown(
    """
    <style>
      .main-header { text-align:center; color:#00d4aa; font-size:2.5rem; margin-bottom:0.5rem; }
      .sub-header  { text-align:center; color:#fafafa; font-size:1.2rem; margin-bottom:2rem; }
      .tool-card   { background:#262730; padding:1rem; border-radius:0.5rem; margin:0.5rem 0; border-left:4px solid #00d4aa; }
      .sidebar .sidebar-content { background:#0e1117; }
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

def render_home_page():
    """Render the home page with tool overview"""

    st.markdown("## 🛠️ Available Tools")
    st.markdown("Select any tool from the sidebar to get started. All tools support bulk operations, file uploads, and instant downloads.")

    # Create tool cards in a grid
    col1, col2 = st.columns(2)

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

    for i, (title, desc, key) in enumerate(tools_info):
        col = col1 if i % 2 == 0 else col2

        with col:
            st.markdown(f"""
            <div style="background:#262730; padding:1rem; border-radius:0.5rem; margin:0.5rem 0; border-left:4px solid #00d4aa;">
                <h4 style="color:#00d4aa; margin:0 0 0.5rem 0;">{title}</h4>
                <p style="color:#b0b0b0; margin:0; font-size:0.9rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

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

    # Sidebar navigation
    st.sidebar.title("🔧 Developer Tools")
    st.sidebar.markdown("---")

    tools_menu = {
        "🏠 Home": "home",
        "🔑 JWT Decoder": "jwt",
        "📝 JSON Formatter": "json",
        "⏰ Timestamp Converter": "timestamp",
        "🆔 UUID Generator": "uuid",
        "🔤 Base64 Converter": "base64",
        "🔗 URL Encoder": "url",
        "🔍 Regex Tester": "regex",
        "📄 Markdown Converter": "markdown",
        "🎨 Color Palette": "color",
        "🤖 Robots.txt Generator": "robots"
    }

    selected = st.sidebar.selectbox("Choose a tool:", list(tools_menu.keys()))
    tool_key = tools_menu[selected]

    # 4. Wrap each tool render in a styled div
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)

    if tool_key == "home":
        render_home_page()
    elif tool_key == "jwt":
        jwt_decoder.render()
    elif tool_key == "json":
        json_formatter.render()
    elif tool_key == "timestamp":
        timestamp_converter.render()
    elif tool_key == "uuid":
        uuid_generator.render()
    elif tool_key == "base64":
        base64_converter.render()
    elif tool_key == "url":
        url_encoder.render()
    elif tool_key == "regex":
        regex_tester.render()
    elif tool_key == "markdown":
        markdown_converter.render()
    elif tool_key == "color":
        color_palette.render()
    elif tool_key == "robots":
        robots_generator.render()

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    add_footer()

if __name__ == "__main__":
    main()
