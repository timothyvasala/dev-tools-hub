import streamlit as st
import sys
from pathlib import Path

# Ensure project root is in path
sys.path.append(str(Path(__file__).parent))

# Import all tool modules
from tools import (
    jwt_decoder,
    json_formatter,
    timestamp_converter,
    uuid_generator,
    base64_converter,
    url_encoder,
    regex_tester,
    markdown_converter,
    color_palette,
    robots_generator
)
from utils.common import add_footer

# Configure page
st.set_page_config(
    page_title="DevTools Hub - Free Developer Utilities",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Sidebar title
    st.sidebar.title("🔧 Developer Tools")
    st.sidebar.markdown("---")

    # Define tools menu
    tools_menu = {
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

    # Sidebar selectbox
    selected = st.sidebar.selectbox("Choose a tool:", list(tools_menu.keys()))
    tool_key = tools_menu[selected]

    # Route to the selected tool
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

    # Footer on all pages
    add_footer()

if __name__ == "__main__":
    main()
