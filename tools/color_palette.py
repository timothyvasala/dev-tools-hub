import streamlit as st
import random
from utils.common import setup_page, show_result, add_footer
from typing import List

# ── Cache heavy color operations ───────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def generate_random_palette(count: int, seed: int = None) -> List[str]:
    """Generate a list of random hex colors with optional seed for reproducibility"""
    if seed:
        random.seed(seed)
    return [f"#{random.randint(0, 0xFFFFFF):06X}" for _ in range(count)]

@st.cache_data(show_spinner=False)
def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """Calculate WCAG contrast ratio between two hex colors"""
    def luminance(hex_color):
        r, g, b = tuple(int(hex_color[i:i+2], 16)/255 for i in (1, 3, 5))
        for v in (r, g, b):
            v = v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
        return 0.2126*r + 0.7152*g + 0.0722*b

    l1, l2 = luminance(color1), luminance(color2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Header
    setup_page(
        "🎨 Color Palette Generator",
        "Generate random HEX colors or check contrast compliance."
    )

    # 2. Mode
    mode = st.radio("Mode:", ["Random Palette", "Contrast Checker"])

    if mode == "Random Palette":
        col1, col2 = st.columns([2, 1])
        with col1:
            count = st.number_input("How many colors?", min_value=1, max_value=10, value=5)
        with col2:
            use_seed = st.checkbox("Use seed for reproducible colors")
            seed = st.number_input("Seed:", value=42) if use_seed else None

        if st.button("🎲 Generate"):
            palette = generate_random_palette(count, seed)

            # Display colors visually
            cols = st.columns(min(count, 5))  # Max 5 columns per row
            for i, color in enumerate(palette):
                with cols[i % 5]:
                    st.markdown(
                        f'<div style="background:{color};height:80px;border-radius:8px;'
                        f'border:2px solid #444;margin:4px 0;"></div>',
                        unsafe_allow_html=True
                    )
                    st.code(color, language="css")

            # Show result as text
            result = "\n".join(palette)
            show_result(result)

            st.download_button(
                label="📥 Download Palette",
                data=result,
                file_name="color_palette.txt",
                mime="text/plain"
            )

    else:
        st.subheader("WCAG Contrast Checker")
        col1, col2 = st.columns(2)

        with col1:
            c1 = st.color_picker("Foreground Color", "#000000")
            st.markdown(
                f'<div style="background:{c1};height:60px;border-radius:8px;'
                f'border:2px solid #666;"></div>',
                unsafe_allow_html=True
            )

        with col2:
            c2 = st.color_picker("Background Color", "#FFFFFF")
            st.markdown(
                f'<div style="background:{c2};height:60px;border-radius:8px;'
                f'border:2px solid #666;"></div>',
                unsafe_allow_html=True
            )

        if st.button("✔️ Check Contrast"):
            ratio = calculate_contrast_ratio(c1, c2)

            # Display preview
            st.markdown("**Preview:**")
            st.markdown(
                f'<div style="background:{c2};color:{c1};padding:20px;'
                f'border-radius:8px;border:2px solid #666;text-align:center;">'
                f'<h3>Sample Text</h3>'
                f'<p>This is how your text will look with these colors.</p>'
                f'</div>',
                unsafe_allow_html=True
            )

            show_result(f"Contrast Ratio: {ratio:.2f}:1")

            # WCAG compliance check
            if ratio >= 7.0:
                st.success("✅ AAA Compliant - Excellent contrast!")
            elif ratio >= 4.5:
                st.success("✅ AA Compliant - Good contrast for normal text")
            elif ratio >= 3.0:
                st.warning("⚠️ AA Compliant for large text only")
            else:
                st.error("❌ Does not meet WCAG guidelines")

            st.info("📊 **WCAG Requirements:**\n"
                   "- AA Normal text: ≥4.5:1\n"
                   "- AA Large text: ≥3:1\n"
                   "- AAA Normal text: ≥7:1\n"
                   "- AAA Large text: ≥4.5:1")

    # Footer
    # add_footer()
