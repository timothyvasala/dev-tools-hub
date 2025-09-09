import streamlit as st
from utils.common import setup_page, show_result, add_footer

# ── Cache robots.txt generation ───────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def generate_robots(agents: list[str], disallow_paths: list[str], allow_paths: list[str], crawl_delay: str) -> str:
    """
    Generate robots.txt content based on user-agents, disallow/allow paths, and optional crawl-delay.
    """
    lines = []
    for ua in agents:
        lines.append(f"User-agent: {ua}")
        for path in disallow_paths:
            lines.append(f"Disallow: {path}")
        for path in allow_paths:
            lines.append(f"Allow: {path}")
        if crawl_delay.isdigit():
            lines.append(f"Crawl-delay: {crawl_delay}")
        lines.append("")  # blank line between agents
    return "\n".join(lines).strip()
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Header
    setup_page(
        "🤖 Robots.txt Generator",
        "Create a robots.txt to control crawler access."
    )

    # 2. Settings
    user_agents_input = st.text_area(
        "User-agent(s) (one per line):", height=100,
        placeholder="*\nGooglebot"
    )
    disallow_input = st.text_area(
        "Disallow paths (one per line):", height=100,
        placeholder="/admin\n/private"
    )
    allow_input = st.text_area(
        "Allow paths (one per line):", height=100,
        placeholder="/public"
    )
    crawl_delay = st.text_input("Crawl-delay (seconds):", "")

    # Parse inputs
    agents = [ua.strip() for ua in user_agents_input.split("\n") if ua.strip()]
    disallow_paths = [p.strip() for p in disallow_input.split("\n") if p.strip()]
    allow_paths = [p.strip() for p in allow_input.split("\n") if p.strip()]

    # 3. Generate
    if st.button("⚙️ Generate robots.txt"):
        txt = generate_robots(agents, disallow_paths, allow_paths, crawl_delay)
        show_result(txt)
        st.download_button(
            "📥 Download robots.txt",
            txt,
            "robots.txt",
            "text/plain"
        )

    # 4. Footer
    add_footer()
