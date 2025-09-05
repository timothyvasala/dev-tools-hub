import streamlit as st
import random
from utils.common import setup_page, show_result

def render():
    # 1. Header
    setup_page(
        "🎨 Color Palette Generator",
        "Generate random HEX colors or check contrast compliance."
    )

    # 2. Mode
    mode = st.radio("Mode:", ["Random Palette", "Contrast Checker"])

    if mode == "Random Palette":
        count = st.number_input("How many colors?", min_value=1, max_value=10, value=5)
        if st.button("🎲 Generate"):
            palette = [f"#{random.randint(0, 0xFFFFFF):06X}" for _ in range(count)]
            result = "\n".join(palette)
            for c in palette:
                st.markdown(f"<div style='display:inline-block;width:50px;height:50px;background:{c};margin:2px;border:1px solid #fff;'></div>", unsafe_allow_html=True)
            show_result(result)

    else:
        c1 = st.color_picker("Color 1", "#FFFFFF")
        c2 = st.color_picker("Color 2", "#000000")
        if st.button("✔️ Check Contrast"):
            # Simple luminance contrast ratio
            def lum(hexc):
                r, g, b = tuple(int(hexc[i:i+2], 16)/255 for i in (1,3,5))
                for v in (r, g, b):
                    v = v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
                return 0.2126*r + 0.7152*g + 0.0722*b
            l1, l2 = lum(c1), lum(c2)
            ratio = (max(l1,l2)+0.05)/(min(l1,l2)+0.05)
            show_result(f"Contrast ratio: {ratio:.2f}")
            st.info("WCAG AA requires ≥4.5:1 for normal text, ≥3:1 for large text.")

    # Footer
    from utils.common import add_footer
    add_footer()
