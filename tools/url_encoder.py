import streamlit as st
import urllib.parse
from utils.common import setup_page, show_result, validate_input

def render():
    # 1. Header
    setup_page(
        "🔗 URL Encoder / Decoder",
        "Encode special characters for URLs or decode URL-encoded strings."
    )

    # 2. Mode selection
    mode = st.radio("Mode:", ["Encode URL", "Decode URL", "Bulk Processing"])

    # 3. Encode URL
    if mode == "Encode URL":
        text = st.text_area("Enter text/URL to encode:", height=150,
                           placeholder="Hello World! Special chars: @#$%")
        if st.button("🔒 Encode URL"):
            valid, msg = validate_input(text)
            if not valid:
                st.error(f"❌ {msg}")
            else:
                encoded = urllib.parse.quote(text, safe='')
                show_result(encoded)
                st.download_button("📥 Download", encoded, "encoded_url.txt", "text/plain")

    # 4. Decode URL
    elif mode == "Decode URL":
        encoded_text = st.text_area("Enter URL-encoded text to decode:", height=150,
                                   placeholder="Hello%20World%21%20Special%20chars%3A%20%40%23%24%25")
        if st.button("🔓 Decode URL"):
            valid, msg = validate_input(encoded_text)
            if not valid:
                st.error(f"❌ {msg}")
            else:
                try:
                    decoded = urllib.parse.unquote(encoded_text)
                    show_result(decoded)
                    st.download_button("📥 Download", decoded, "decoded_url.txt", "text/plain")
                except Exception as e:
                    st.error(f"❌ Decoding error: {e}")

    # 5. Bulk Processing
    else:  # mode == "Bulk Processing"
        direction = st.selectbox("Direction:", ["Encode", "Decode"])
        bulk_text = st.text_area("Enter URLs/text (one per line):", height=200)

        if st.button("🔄 Process All"):
            if not bulk_text:
                st.error("❌ Please enter some text")
            else:
                lines = [line.strip() for line in bulk_text.split('\n') if line.strip()]
                results = []
                errors = []

                for i, line in enumerate(lines, 1):
                    try:
                        if direction == "Encode":
                            result = urllib.parse.quote(line, safe='')
                            results.append(f"{line} → {result}")
                        else:  # Decode
                            result = urllib.parse.unquote(line)
                            results.append(f"{line} → {result}")
                    except Exception as e:
                        errors.append(f"Line {i}: {e}")

                if results:
                    st.success(f"✅ Processed {len(results)} URLs")
                    show_result('\n'.join(results))
                    st.download_button("📥 Download Results", '\n'.join(results),
                                     f"bulk_url_{direction.lower()}.txt", "text/plain")

                if errors:
                    for error in errors:
                        st.error(error)

    # 6. Info box
    with st.expander("ℹ️ About URL Encoding"):
        st.markdown("""
        **URL Encoding** (also called percent-encoding) converts special characters to a format that can be transmitted over the Internet.

        **Common encodings:**
        - Space ` ` → `%20`
        - `!` → `%21`
        - `@` → `%40`
        - `#` → `%23`
        - `$` → `%24`
        - `%` → `%25`

        **Use cases:**
        - Query parameters in URLs
        - Form data submission
        - API requests with special characters
        """)

    # 7. Footer
    from utils.common import add_footer
    add_footer()
