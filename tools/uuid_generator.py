import streamlit as st
import uuid
from utils.common import setup_page, show_result

def render():
    # 1. Header
    setup_page(
        "🆔 UUID Generator",
        "Generate version 4 UUIDs for unique identifiers."
    )

    # 2. Input: number of UUIDs to generate
    count = st.number_input(
        "How many UUIDs to generate?",
        min_value=1, max_value=1000, value=1, step=1
    )

    # 3. Generate button
    if st.button("🔢 Generate"):
        uuids = [str(uuid.uuid4()) for _ in range(count)]
        result = "\n".join(uuids)
        show_result(result)
        st.download_button(
            label="📥 Download as TXT",
            data=result,
            file_name=f"{count}_uuids.txt",
            mime="text/plain"
        )

    # 4. Footer
    from utils.common import add_footer
    add_footer()
