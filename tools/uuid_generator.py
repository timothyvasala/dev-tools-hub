import streamlit as st
import uuid
from utils.common import setup_page, show_result, add_footer

# ── Cache UUID generation when using a seed ────────────────────────────────────
@st.cache_data(show_spinner=False)
def generate_uuids(count: int, seed: int | None = None) -> list[str]:
    """
    Generate a list of version 4 UUIDs.
    If seed is provided, uses it to seed the RNG for reproducible results.
    """
    if seed is not None:
        import random
        random.seed(seed)
    return [str(uuid.uuid4()) for _ in range(count)]
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Header
    setup_page(
        "🆔 UUID Generator",
        "Generate version 4 UUIDs for unique identifiers."
    )

    # 2. Inputs
    col1, col2 = st.columns([2, 1])
    with col1:
        count = st.number_input(
            "How many UUIDs to generate?",
            min_value=1, max_value=1000, value=1, step=1
        )
    with col2:
        use_seed = st.checkbox("Use seed for reproducible UUIDs")
        seed = st.number_input("Seed value:", value=0) if use_seed else None

    # 3. Generate button
    if st.button("🔢 Generate"):
        uuids = generate_uuids(count, seed)
        result = "\n".join(uuids)
        show_result(result)
        st.download_button(
            label="📥 Download as TXT",
            data=result,
            file_name=f"{count}_uuids.txt",
            mime="text/plain"
        )

    # 4. Footer
    # add_footer()
