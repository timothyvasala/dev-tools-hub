import streamlit as st
from utils.common import setup_page, show_result

def render():
    # 1. Header
    setup_page(
        "🤖 Robots.txt Generator",
        "Create a robots.txt to control crawler access."
    )

    # 2. Settings
    user_agents = st.text_area(
        "User-agent(s) (one per line):", height=100,
        placeholder="*\nGooglebot"
    )
    disallow = st.text_area(
        "Disallow paths (one per line):", height=100,
        placeholder="/admin\n/private"
    )
    allow = st.text_area(
        "Allow paths (one per line):", height=100,
        placeholder="/public"
    )
    crawl_delay = st.text_input("Crawl-delay (seconds):", "")

    # 3. Generate
    if st.button("⚙️ Generate robots.txt"):
        lines = []
        agents = [ua.strip() for ua in user_agents.split("\n") if ua.strip()]
        for ua in agents:
            lines.append(f"User-agent: {ua}")
            for path in [p.strip() for p in disallow.split("\n") if p.strip()]:
                lines.append(f"Disallow: {path}")
            for path in [p.strip() for p in allow.split("\n") if p.strip()]:
                lines.append(f"Allow: {path}")
            if crawl_delay.strip().isdigit():
                lines.append(f"Crawl-delay: {crawl_delay.strip()}")
            lines.append("")  # blank line between agents
        txt = "\n".join(lines).strip()
        show_result(txt)
        st.download_button("📥 Download robots.txt", txt, "robots.txt", "text/plain")

    # Footer
    from utils.common import add_footer
    add_footer()
