import streamlit as st
import sys
from pathlib import Path

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

def main():
    # 3. Use your styled headers
    st.markdown('<div class="main-header">DevTools Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional, free developer utilities</div>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("🔧 Developer Tools")
    st.sidebar.markdown("---")

    tools_menu = {
        "🔑 JWT Decoder": "jwt", "📝 JSON Formatter": "json",
        "⏰ Timestamp Converter": "timestamp","🆔 UUID Generator": "uuid",
        "🔤 Base64 Converter": "base64","🔗 URL Encoder": "url",
        "🔍 Regex Tester": "regex","📄 Markdown Converter": "markdown",
        "🎨 Color Palette": "color","🤖 Robots.txt Generator": "robots"
    }

    selected = st.sidebar.selectbox("Choose a tool:", list(tools_menu.keys()))
    tool_key = tools_menu[selected]

    # 4. Wrap each tool render in a styled div
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    if tool_key == "jwt":
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
