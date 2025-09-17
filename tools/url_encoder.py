import streamlit as st
import urllib.parse
from utils.common import setup_page, show_result, validate_input, add_footer

# ── Cache URL operations ───────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def encode_url(text: str) -> str:
    return urllib.parse.quote(text, safe='')

@st.cache_data(show_spinner=False)
def decode_url(text: str) -> str:
    return urllib.parse.unquote(text)

@st.cache_data(show_spinner=False)
def bulk_process(lines: list[str], direction: str) -> list[str]:
    results = []
    for line in lines:
        if direction == "Encode":
            results.append(f"{line} → {urllib.parse.quote(line, safe='')}")
        else:
            results.append(f"{line} → {urllib.parse.unquote(line)}")
    return results
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Header
    setup_page(
        "🔗 URL Encoder / Decoder",
        "Encode special characters for URLs or decode URL-encoded strings."
    )

    # 2. Mode selection
    mode = st.radio("Mode:", ["Encode URL", "Decode URL", "Bulk Processing"])

    if mode == "Encode URL":
        text = st.text_area("Enter text/URL to encode:", height=150,
                            placeholder="Hello World! Special chars: @#$%")
        if st.button("🔒 Encode URL"):
            valid, msg = validate_input(text)
            if not valid:
                st.error(f"❌ {msg}")
            else:
                encoded = encode_url(text)
                show_result(encoded)
                st.download_button("📥 Download", encoded, "encoded_url.txt", "text/plain")

    elif mode == "Decode URL":
        encoded_text = st.text_area("Enter URL-encoded text to decode:", height=150,
                                    placeholder="Hello%20World%21%20Special%20chars%3A%20%40%23%24%25")
        if st.button("🔓 Decode URL"):
            valid, msg = validate_input(encoded_text)
            if not valid:
                st.error(f"❌ {msg}")
            else:
                try:
                    decoded = decode_url(encoded_text)
                    show_result(decoded)
                    st.download_button("📥 Download", decoded, "decoded_url.txt", "text/plain")
                except Exception as e:
                    st.error(f"❌ Decoding error: {e}")

    else:  # Bulk Processing
        direction = st.selectbox("Direction:", ["Encode", "Decode"])
        bulk_text = st.text_area("Enter URLs/text (one per line):", height=200)

        if st.button("🔄 Process All"):
            if not bulk_text:
                st.error("❌ Please enter some text")
            else:
                lines = [line.strip() for line in bulk_text.split('\n') if line.strip()]
                results = bulk_process(lines, direction)

                if results:
                    st.success(f"✅ Processed {len(results)} items")
                    show_result('\n'.join(results))
                    st.download_button(
                        "📥 Download Results",
                        '\n'.join(results),
                        f"bulk_url_{direction.lower()}.txt",
                        "text/plain"
                    )

    # 6. Info box
    with st.expander("ℹ️ About URL Encoding"):
        st.markdown("""
        **URL Encoding** (percent-encoding) converts special characters to a transmit-safe format.

        **Common encodings:**
        - Space ` ` → `%20`
        - `!` → `%21`
        - `@` → `%40`
        - `#` → `%23`
        - `$` → `%24`
        - `%` → `%25`

        **Use cases:**
        - Query parameters
        - Form submissions
        - API request encoding
        """)

    # 7. Footer
    # add_footer()
