# Complete Developer Tools Website Implementation Guide

## 🚀 Project Overview
Building a professional-grade, free developer tools website using Python + Streamlit with zero budget.

## 📁 Project Structure
```
dev-tools-hub/
├── app.py                 # Main application file
├── tools/                 # Individual tool modules
│   ├── __init__.py
│   ├── jwt_decoder.py
│   ├── json_formatter.py
│   ├── timestamp_converter.py
│   ├── uuid_generator.py
│   ├── base64_converter.py
│   ├── url_encoder.py
│   ├── regex_tester.py
│   ├── markdown_converter.py
│   ├── color_palette.py
│   └── robots_generator.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── common.py
├── requirements.txt       # Dependencies
├── README.md             # Documentation
└── .streamlit/           # Streamlit config
    └── config.toml
```

## 🔧 Step 1: Environment Setup

### 1.1 Install Python & Dependencies
```bash
# Create project directory
mkdir dev-tools-hub
cd dev-tools-hub

# Install required packages
pip install streamlit pandas pillow requests regex markdown2 jwt

# Create requirements.txt
echo "streamlit>=1.28.0
pandas>=1.5.0
pillow>=9.0.0
requests>=2.28.0
regex>=2022.10.31
markdown2>=2.4.0
PyJWT>=2.8.0" > requirements.txt
```

### 1.2 Create Basic Structure
```bash
mkdir tools utils .streamlit
touch app.py tools/__init__.py utils/__init__.py utils/common.py
touch tools/jwt_decoder.py tools/json_formatter.py tools/timestamp_converter.py
touch tools/uuid_generator.py tools/base64_converter.py tools/url_encoder.py
touch tools/regex_tester.py tools/markdown_converter.py tools/color_palette.py
touch tools/robots_generator.py
```

## 🎨 Step 2: Streamlit Configuration

### 2.1 Create .streamlit/config.toml
```toml
[theme]
primaryColor = "#00d4aa"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
font = "monospace"

[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

## 🏗️ Step 3: Core Implementation

### 3.1 Main Application (app.py)
```python
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from tools import (
    jwt_decoder, json_formatter, timestamp_converter, 
    uuid_generator, base64_converter, url_encoder,
    regex_tester, markdown_converter, color_palette, 
    robots_generator
)
from utils.common import setup_page, add_footer, track_usage

# Page config
st.set_page_config(
    page_title="DevTools Hub - Free Developer Utilities",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Custom CSS for professional look
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #00d4aa;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #fafafa;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .tool-card {
        background: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #00d4aa;
    }
    .sidebar .sidebar-content {
        background: #0e1117;
    }
    .stAlert {
        background-color: #262730;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🛠️ DevTools Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional-grade developer utilities, completely free</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🔧 Developer Tools")
    st.sidebar.markdown("---")
    
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
    
    selected_tool = st.sidebar.selectbox(
        "Choose a tool:",
        options=list(tools_menu.keys()),
        index=0
    )
    
    tool_key = tools_menu[selected_tool]
    
    # Tool routing
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
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Statistics")
    st.sidebar.info("🔥 All tools are free & unlimited")
    st.sidebar.success("🚀 No registration required")
    st.sidebar.warning("⭐ Open source on GitHub")
    
    # Footer
    add_footer()

if __name__ == "__main__":
    main()
```

### 3.2 Common Utilities (utils/common.py)
```python
import streamlit as st
import time
import json
from datetime import datetime

def setup_page(title, description=""):
    """Setup page with consistent header and description"""
    st.markdown(f"""
    <div class="tool-card">
        <h2 style="color: #00d4aa; margin-bottom: 0.5rem;">{title}</h2>
        <p style="color: #b0b0b0; margin-bottom: 1rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def add_copy_button(content, label="Copy Result"):
    """Add a copy-to-clipboard button"""
    if st.button(label):
        # Using JavaScript to copy to clipboard
        st.markdown(f"""
        <script>
        navigator.clipboard.writeText(`{content}`);
        </script>
        """, unsafe_allow_html=True)
        st.success("✅ Copied to clipboard!")

def show_result(result, result_type="text"):
    """Display result with proper formatting"""
    if result_type == "json":
        st.code(result, language="json")
    elif result_type == "html":
        st.code(result, language="html")
    elif result_type == "css":
        st.code(result, language="css")
    else:
        st.code(result)

def handle_file_upload(file_types=None, max_size_mb=5):
    """Handle file upload with size and type validation"""
    if file_types is None:
        file_types = ["txt", "json", "csv", "md"]
    
    uploaded_file = st.file_uploader(
        "Or upload a file:",
        type=file_types,
        help=f"Maximum file size: {max_size_mb}MB"
    )
    
    if uploaded_file is not None:
        # Check file size
        if uploaded_file.size > max_size_mb * 1024 * 1024:
            st.error(f"File too large! Maximum size: {max_size_mb}MB")
            return None
        
        try:
            content = uploaded_file.read().decode('utf-8')
            return content
        except UnicodeDecodeError:
            st.error("Unable to decode file. Please ensure it's a valid text file.")
            return None
    
    return None

def validate_input(input_text, min_length=1, max_length=1000000):
    """Validate input text"""
    if not input_text:
        return False, "Input cannot be empty"
    
    if len(input_text) < min_length:
        return False, f"Input too short (minimum {min_length} characters)"
    
    if len(input_text) > max_length:
        return False, f"Input too long (maximum {max_length:,} characters)"
    
    return True, "Valid"

def add_footer():
    """Add consistent footer to all pages"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>Made with ❤️ for developers | 
        <a href="https://github.com/your-username/dev-tools-hub" target="_blank">⭐ Star on GitHub</a> | 
        Free Forever</p>
    </div>
    """, unsafe_allow_html=True)

def track_usage(tool_name):
    """Simple usage tracking (optional)"""
    # You can implement analytics here later
    pass
```

## 🔧 Step 4: Individual Tool Implementation

### 4.1 JWT Decoder (tools/jwt_decoder.py)
```python
import streamlit as st
import jwt
import json
import base64
from utils.common import setup_page, show_result, handle_file_upload, validate_input

def render():
    setup_page(
        "🔑 JWT Decoder & Debugger", 
        "Decode and inspect JSON Web Tokens without verification"
    )
    
    # Input methods
    input_method = st.radio(
        "Input method:",
        ["Paste Token", "Upload File", "Bulk Processing"]
    )
    
    jwt_tokens = []
    
    if input_method == "Paste Token":
        token_input = st.text_area(
            "Paste your JWT token:",
            placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            height=100
        )
        if token_input.strip():
            jwt_tokens = [token_input.strip()]
    
    elif input_method == "Upload File":
        file_content = handle_file_upload(["txt", "json"], max_size_mb=2)
        if file_content:
            # Try to parse as JSON array or newline-separated tokens
            try:
                tokens = json.loads(file_content)
                if isinstance(tokens, list):
                    jwt_tokens = tokens
                else:
                    jwt_tokens = [str(tokens)]
            except:
                jwt_tokens = [line.strip() for line in file_content.split('\n') if line.strip()]
    
    elif input_method == "Bulk Processing":
        bulk_input = st.text_area(
            "Enter multiple tokens (one per line):",
            height=150
        )
        if bulk_input.strip():
            jwt_tokens = [line.strip() for line in bulk_input.split('\n') if line.strip()]
    
    # Processing
    if jwt_tokens:
        if st.button("🔓 Decode JWT(s)", type="primary"):
            results = []
            
            for i, token in enumerate(jwt_tokens):
                try:
                    # Validate token format
                    parts = token.split('.')
                    if len(parts) != 3:
                        results.append({
                            "token_index": i + 1,
                            "error": "Invalid JWT format (should have 3 parts separated by dots)"
                        })
                        continue
                    
                    # Decode without verification
                    decoded_payload = jwt.decode(
                        token, 
                        options={"verify_signature": False}
                    )
                    
                    # Decode header
                    header_encoded = parts[0] + '=' * (-len(parts[0]) % 4)
                    header = json.loads(base64.urlsafe_b64decode(header_encoded))
                    
                    results.append({
                        "token_index": i + 1,
                        "header": header,
                        "payload": decoded_payload,
                        "raw_token": token[:50] + "..." if len(token) > 50 else token
                    })
                    
                except Exception as e:
                    results.append({
                        "token_index": i + 1,
                        "error": str(e),
                        "raw_token": token[:50] + "..." if len(token) > 50 else token
                    })
            
            # Display results
            for result in results:
                if "error" in result:
                    st.error(f"❌ Token #{result['token_index']}: {result['error']}")
                    if 'raw_token' in result:
                        st.code(result['raw_token'])
                else:
                    st.success(f"✅ Token #{result['token_index']} decoded successfully")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Header")
                        st.json(result['header'])
                    
                    with col2:
                        st.subheader("📄 Payload")  
                        st.json(result['payload'])
                
                st.markdown("---")
            
            # Export option for bulk processing
            if len(results) > 1:
                if st.button("📥 Download Results as JSON"):
                    json_output = json.dumps(results, indent=2)
                    st.download_button(
                        label="💾 Download JSON",
                        data=json_output,
                        file_name=f"jwt_decoded_results_{len(results)}_tokens.json",
                        mime="application/json"
                    )
    
    # Additional features
    with st.expander("ℹ️ About JWT"):
        st.markdown("""
        **JSON Web Tokens (JWT)** are a compact way to securely transmit information between parties.
        
        **Structure:**
        - **Header**: Token type and signing algorithm
        - **Payload**: Claims (user data, expiration, etc.)
        - **Signature**: Used to verify the token hasn't been tampered with
        
        **⚠️ Security Note:** This tool decodes tokens without signature verification. 
        Never paste sensitive tokens on untrusted websites.
        """)
```

### 4.2 JSON Formatter (tools/json_formatter.py)
```python
import streamlit as st
import json
from utils.common import setup_page, show_result, handle_file_upload, validate_input

def render():
    setup_page(
        "📝 JSON Formatter & Validator",
        "Format, validate, and beautify JSON data with error detection"
    )
    
    # Input options
    col1, col2 = st.columns([3, 1])
    
    with col2:
        indent_size = st.selectbox("Indentation:", [2, 4, 8], index=0)
        sort_keys = st.checkbox("Sort keys alphabetically")
        ensure_ascii = st.checkbox("Ensure ASCII", value=False)
    
    # Input methods
    input_method = st.radio(
        "Input method:",
        ["Paste JSON", "Upload File"]
    )
    
    json_input = ""
    
    if input_method == "Paste JSON":
        json_input = st.text_area(
            "Paste your JSON:",
            placeholder='{"name": "John", "age": 30, "city": "New York"}',
            height=200
        )
    else:
        file_content = handle_file_upload(["json", "txt"], max_size_mb=10)
        if file_content:
            json_input = file_content
    
    # Processing
    if json_input.strip():
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✨ Format & Validate", type="primary"):
                try:
                    # Parse JSON
                    parsed_json = json.loads(json_input)
                    
                    # Format with options
                    formatted_json = json.dumps(
                        parsed_json,
                        indent=indent_size,
                        sort_keys=sort_keys,
                        ensure_ascii=ensure_ascii,
                        separators=(',', ': ')
                    )
                    
                    st.success("✅ Valid JSON!")
                    
                    # Statistics
                    stats = analyze_json(parsed_json)
                    with st.expander("📊 JSON Statistics"):
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Total Keys", stats['total_keys'])
                        with col_b:
                            st.metric("Max Depth", stats['max_depth'])
                        with col_c:
                            st.metric("Size (bytes)", len(formatted_json))
                    
                    # Output
                    st.subheader("📄 Formatted JSON:")
                    st.code(formatted_json, language="json")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Formatted JSON",
                        data=formatted_json,
                        file_name="formatted.json",
                        mime="application/json"
                    )
                    
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON: {str(e)}")
                    
                    # Try to highlight error location
                    lines = json_input.split('\n')
                    if hasattr(e, 'lineno') and e.lineno <= len(lines):
                        st.code(f"Line {e.lineno}: {lines[e.lineno-1]}", language="json")
                        st.info(f"💡 Error at line {e.lineno}, column {e.colno}")
                
                except Exception as e:
                    st.error(f"❌ Error processing JSON: {str(e)}")
        
        with col2:
            if st.button("🗜️ Minify JSON"):
                try:
                    parsed_json = json.loads(json_input)
                    minified = json.dumps(parsed_json, separators=(',', ':'))
                    
                    reduction = round((1 - len(minified)/len(json_input)) * 100, 1)
                    st.success(f"✅ Reduced by {reduction}%")
                    
                    st.subheader("🗜️ Minified JSON:")
                    st.code(minified, language="json")
                    
                    st.download_button(
                        label="📥 Download Minified",
                        data=minified,
                        file_name="minified.json",
                        mime="application/json"
                    )
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # JSON Tools
    with st.expander("🔧 Additional JSON Tools"):
        st.markdown("""
        **Common JSON Issues:**
        - Missing quotes around keys
        - Trailing commas
        - Single quotes instead of double quotes
        - Unescaped special characters
        
        **Pro Tips:**
        - Use proper indentation for readability
        - Validate JSON before using in APIs
        - Minify for production to reduce size
        """)

def analyze_json(obj, depth=0):
    """Analyze JSON structure and return statistics"""
    stats = {
        'total_keys': 0,
        'max_depth': depth,
        'arrays': 0,
        'objects': 0
    }
    
    if isinstance(obj, dict):
        stats['objects'] += 1
        stats['total_keys'] += len(obj)
        for value in obj.values():
            sub_stats = analyze_json(value, depth + 1)
            stats['total_keys'] += sub_stats['total_keys']
            stats['max_depth'] = max(stats['max_depth'], sub_stats['max_depth'])
            stats['arrays'] += sub_stats['arrays']
            stats['objects'] += sub_stats['objects']
    
    elif isinstance(obj, list):
        stats['arrays'] += 1
        for item in obj:
            sub_stats = analyze_json(item, depth + 1)
            stats['total_keys'] += sub_stats['total_keys']
            stats['max_depth'] = max(stats['max_depth'], sub_stats['max_depth'])
            stats['arrays'] += sub_stats['arrays']
            stats['objects'] += sub_stats['objects']
    
    return stats
```

### 4.3 Unix Timestamp Converter (tools/timestamp_converter.py)
```python
import streamlit as st
from datetime import datetime, timezone
import time
import re
from utils.common import setup_page, show_result

def render():
    setup_page(
        "⏰ Unix Timestamp Converter",
        "Convert between Unix timestamps and human-readable dates"
    )
    
    # Conversion direction
    conversion_type = st.radio(
        "Conversion type:",
        ["Timestamp → Date", "Date → Timestamp", "Bulk Conversion"]
    )
    
    if conversion_type == "Timestamp → Date":
        timestamp_to_date()
    elif conversion_type == "Date → Timestamp":
        date_to_timestamp()
    else:
        bulk_conversion()
    
    # Current timestamp
    with st.sidebar:
        st.markdown("### 🕐 Current Time")
        current_ts = int(time.time())
        current_dt = datetime.fromtimestamp(current_ts, tz=timezone.utc)
        
        st.code(f"Timestamp: {current_ts}")
        st.code(f"UTC: {current_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if st.button("📋 Copy Current Timestamp"):
            st.code(str(current_ts))

def timestamp_to_date():
    """Convert Unix timestamp to human-readable date"""
    
    timestamp_input = st.text_input(
        "Enter Unix timestamp:",
        placeholder="1609459200",
        help="Unix timestamp (seconds since January 1, 1970)"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        timezone_option = st.selectbox(
            "Timezone:",
            ["UTC", "Local", "Custom"],
            index=1
        )
    
    with col2:
        format_option = st.selectbox(
            "Date format:",
            [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%d/%m/%Y %H:%M:%S", 
                "%B %d, %Y %H:%M:%S",
                "ISO 8601"
            ]
        )
    
    if timestamp_input:
        try:
            # Handle different timestamp formats
            timestamp = float(timestamp_input)
            
            # Auto-detect milliseconds vs seconds
            if timestamp > 1e12:  # Likely milliseconds
                timestamp = timestamp / 1000
                st.info("💡 Detected milliseconds, converted to seconds")
            
            # Convert timestamp
            if timezone_option == "UTC":
                dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            else:
                dt = datetime.fromtimestamp(timestamp)
            
            # Format output
            if format_option == "ISO 8601":
                formatted_date = dt.isoformat()
            else:
                formatted_date = dt.strftime(format_option)
            
            # Display results
            st.success("✅ Conversion successful!")
            
            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                st.subheader("📅 Formatted Date")
                st.code(formatted_date, language=None)
            
            with result_col2:
                st.subheader("📋 Additional Formats")
                st.text(f"ISO 8601: {dt.isoformat()}")
                st.text(f"RFC 2822: {dt.strftime('%a, %d %b %Y %H:%M:%S %z')}")
                st.text(f"Weekday: {dt.strftime('%A')}")
                st.text(f"Week: {dt.isocalendar().week}")
            
            # Relative time
            time_diff = datetime.now(timezone.utc) - dt.replace(tzinfo=timezone.utc)
            relative_time = format_relative_time(time_diff.total_seconds())
            st.info(f"🕒 Relative time: {relative_time}")
            
        except ValueError:
            st.error("❌ Invalid timestamp format")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def date_to_timestamp():
    """Convert date to Unix timestamp"""
    
    input_method = st.radio(
        "Input method:",
        ["Date Picker", "Text Input"]
    )
    
    if input_method == "Date Picker":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_input = st.date_input("Date:")
        with col2:
            time_input = st.time_input("Time:")
        with col3:
            include_time = st.checkbox("Include time", value=True)
        
        if date_input:
            if include_time:
                dt = datetime.combine(date_input, time_input)
            else:
                dt = datetime.combine(date_input, datetime.min.time())
    
    else:
        date_string = st.text_input(
            "Enter date string:",
            placeholder="2024-01-01 12:00:00",
            help="Formats: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, MM/DD/YYYY"
        )
        
        dt = None
        if date_string:
            dt = parse_date_string(date_string)
    
    if 'dt' in locals() and dt:
        timezone_option = st.selectbox(
            "Interpret as:",
            ["Local time", "UTC", "Custom timezone"]
        )
        
        if st.button("🔢 Convert to Timestamp", type="primary"):
            try:
                if timezone_option == "UTC":
                    dt = dt.replace(tzinfo=timezone.utc)
                elif timezone_option == "Local time":
                    dt = dt.astimezone()
                
                timestamp = int(dt.timestamp())
                
                st.success("✅ Conversion successful!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🔢 Unix Timestamp")
                    st.code(str(timestamp))
                    st.code(f"{timestamp}000  # Milliseconds")
                
                with col2:
                    st.subheader("✅ Verification")
                    verification = datetime.fromtimestamp(timestamp)
                    st.text(f"Converts back to:")
                    st.text(verification.strftime("%Y-%m-%d %H:%M:%S"))
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

def bulk_conversion():
    """Bulk convert timestamps or dates"""
    
    st.subheader("📊 Bulk Conversion")
    
    conversion_direction = st.radio(
        "Direction:",
        ["Timestamps → Dates", "Dates → Timestamps"]
    )
    
    input_text = st.text_area(
        "Enter values (one per line):",
        placeholder="1609459200\n1640995200\n1672531200" if conversion_direction == "Timestamps → Dates" else "2021-01-01\n2022-01-01\n2023-01-01",
        height=150
    )
    
    if input_text and st.button("🔄 Convert All", type="primary"):
        lines = [line.strip() for line in input_text.split('\n') if line.strip()]
        
        results = []
        errors = []
        
        for i, line in enumerate(lines, 1):
            try:
                if conversion_direction == "Timestamps → Dates":
                    timestamp = float(line)
                    if timestamp > 1e12:
                        timestamp = timestamp / 1000
                    
                    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                    result = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                    results.append(f"{line} → {result}")
                
                else:  # Dates → Timestamps
                    dt = parse_date_string(line)
                    if dt:
                        timestamp = int(dt.timestamp())
                        results.append(f"{line} → {timestamp}")
                    else:
                        errors.append(f"Line {i}: Invalid date format")
            
            except Exception as e:
                errors.append(f"Line {i}: {str(e)}")
        
        # Display results
        if results:
            st.success(f"✅ Converted {len(results)} items")
            result_text = '\n'.join(results)
            st.code(result_text)
            
            st.download_button(
                label="📥 Download Results",
                data=result_text,
                file_name=f"timestamp_conversion_{len(results)}_items.txt",
                mime="text/plain"
            )
        
        if errors:
            st.error("❌ Errors:")
            for error in errors:
                st.text(error)

def parse_date_string(date_str):
    """Parse various date string formats"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S", 
        "%Y/%m/%d",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

def format_relative_time(seconds):
    """Format seconds into relative time string"""
    abs_seconds = abs(seconds)
    
    if abs_seconds < 60:
        return f"{int(abs_seconds)} seconds ago" if seconds > 0 else f"in {int(abs_seconds)} seconds"
    elif abs_seconds < 3600:
        minutes = int(abs_seconds / 60)
        return f"{minutes} minutes ago" if seconds > 0 else f"in {minutes} minutes"
    elif abs_seconds < 86400:
        hours = int(abs_seconds / 3600)
        return f"{hours} hours ago" if seconds > 0 else f"in {hours} hours"
    else:
        days = int(abs_seconds / 86400)
        return f"{days} days ago" if seconds > 0 else f"in {days} days"
```

## 📱 Step 5: Deployment Guide

### 5.1 GitHub Setup
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: DevTools Hub"

# Create GitHub repository (go to github.com)
# Then connect local repo to GitHub
git remote add origin https://github.com/YOUR_USERNAME/dev-tools-hub.git
git push -u origin main
```

### 5.2 Streamlit Community Cloud Deployment
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Set main file path: `app.py`
5. Click "Deploy"

### 5.3 Custom Domain (Optional, Free)
- Use Cloudflare for free DNS management
- Add CNAME record pointing to your Streamlit app
- Enable SSL through Cloudflare

## 🎯 Step 6: Professional Features

### 6.1 SEO Optimization
Add to each tool file:
```python
# Add to beginning of render() function
st.markdown(f"""
<meta name="description" content="{tool_description}">
<meta name="keywords" content="{relevant_keywords}">
<meta property="og:title" content="{tool_name} - DevTools Hub">
<meta property="og:description" content="{tool_description}">
""", unsafe_allow_html=True)
```

### 6.2 Analytics (Optional)
Add Google Analytics code to main app.py:
```python
# Add to main() function
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

### 6.3 API Endpoints (Advanced)
Create `api.py` for programmatic access:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DevTools Hub API")

@app.get("/api/jwt/decode")
async def decode_jwt(token: str):
    # Implementation here
    pass

@app.get("/api/json/format") 
async def format_json(data: str, indent: int = 2):
    # Implementation here
    pass
```

## 🔧 Step 7: Testing & Quality Assurance

### 7.1 Test Each Tool Thoroughly
```python
# Create test_tools.py
import pytest
from tools import jwt_decoder, json_formatter

def test_jwt_decoder():
    # Test valid JWT
    # Test invalid JWT
    # Test edge cases
    pass

def test_json_formatter():
    # Test valid JSON
    # Test invalid JSON
    # Test large files
    pass
```

### 7.2 Performance Optimization
- Enable caching with `@st.cache_data`
- Optimize file upload sizes
- Add loading indicators for slow operations

### 7.3 Error Handling
- Comprehensive try-catch blocks
- User-friendly error messages
- Graceful degradation

## 🚀 Step 8: Launch Strategy

### 8.1 Pre-launch Checklist
- [ ] All tools working correctly
- [ ] Mobile responsive design
- [ ] Fast loading times
- [ ] SEO metadata added
- [ ] Error handling implemented
- [ ] Professional styling applied

### 8.2 Marketing & Promotion
1. **Developer Communities:**
   - Reddit: r/webdev, r/programming, r/Python
   - DEV.to: Write tutorials using your tools
   - Stack Overflow: Answer questions, mention tools when relevant

2. **Content Marketing:**
   - Blog posts: "10 Essential Developer Tools You Need"
   - YouTube demos of each tool
   - GitHub README with comprehensive documentation

3. **Product Hunt Launch:**
   - Submit to Product Hunt
   - Prepare marketing materials
   - Engage with the community

### 8.3 Growth Strategy
1. **Week 1-2:** Soft launch to developer friends
2. **Week 3-4:** Social media promotion
3. **Month 2:** Content marketing and SEO
4. **Month 3+:** Feature additions based on user feedback

## 🔧 Ongoing Maintenance

### 8.1 User Feedback Integration
- Add feedback forms to each tool
- Monitor user behavior with analytics
- Regular feature updates based on usage patterns

### 8.2 Performance Monitoring
- Monitor app performance with Streamlit Cloud metrics
- Optimize slow-loading tools
- Scale if needed (upgrade to paid hosting)

### 8.3 Feature Roadmap
- API access for power users
- Additional developer tools based on demand
- Premium features (bulk processing, history, etc.)

---

## 🎯 Success Metrics to Track

1. **Traffic Metrics:**
   - Monthly active users
   - Page views per tool
   - Time on site
   - Bounce rate

2. **User Engagement:**
   - Tool usage frequency
   - Feature adoption
   - User feedback scores

3. **Technical Metrics:**
   - App performance
   - Error rates
   - Uptime percentage

---

This comprehensive guide provides everything needed to build, deploy, and grow a professional developer tools website with zero upfront cost. Focus on quality, user experience, and consistent value delivery to build trust in the developer community.