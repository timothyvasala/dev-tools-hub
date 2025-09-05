import streamlit as st
from datetime import datetime, timezone
import time
from utils.common import setup_page, show_result

def render():
    # 1. Header
    setup_page(
        "⏰ Unix Timestamp Converter",
        "Convert between Unix timestamps and human-readable dates."
    )

    # 2. Select mode
    mode = st.radio("Conversion type:", ["Timestamp → Date", "Date → Timestamp", "Bulk Conversion"])

    if mode == "Timestamp → Date":
        # Single timestamp to date
        ts = st.text_input("Enter Unix timestamp (seconds or ms):", "")
        fmt = st.selectbox("Output format:", ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "ISO 8601"])
        tz = st.selectbox("Timezone:", ["Local", "UTC"])

        if st.button("🔄 Convert"):
            try:
                t = float(ts)
                # Detect ms vs s
                if t > 1e12:
                    t = t / 1000
                dt = datetime.fromtimestamp(t, tz=timezone.utc if tz=="UTC" else None)
                out = dt.isoformat() if fmt=="ISO 8601" else dt.strftime(fmt)
                show_result(out)
            except Exception as e:
                st.error(f"❌ Error: {e}")

    elif mode == "Date → Timestamp":
        # Single date to timestamp
        date_str = st.text_input("Enter date/time string:", "2025-01-01 12:00:00")
        tz = st.selectbox("Interpret as:", ["Local", "UTC"])
        if st.button("🔄 Convert"):
            try:
                dt = datetime.fromisoformat(date_str) if "T" in date_str else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if tz == "UTC":
                    dt = dt.replace(tzinfo=timezone.utc)
                ts = int(dt.timestamp())
                show_result(str(ts))
            except Exception as e:
                st.error(f"❌ Error: {e}")

    else:
        # Bulk conversion
        text = st.text_area("Enter values, one per line:", "")
        direction = st.selectbox("Direction:", ["→ Date", "→ Timestamp"])
        if st.button("🔄 Bulk Convert"):
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            results, errors = [], []
            for i, line in enumerate(lines, 1):
                try:
                    if direction == "→ Date":
                        t = float(line)
                        if t > 1e12: t /= 1000
                        dt = datetime.fromtimestamp(t, tz=timezone.utc)
                        results.append(f"{line} → {dt.isoformat()}")
                    else:
                        dt = datetime.fromisoformat(line)
                        results.append(f"{line} → {int(dt.timestamp())}")
                except Exception as e:
                    errors.append(f"Line {i}: {e}")
            if results:
                show_result("\n".join(results))
            if errors:
                for err in errors:
                    st.error(err)

    # 3. Sidebar: show current timestamp
    with st.sidebar.expander("🕒 Current Time"):
        now_ts = int(time.time())
        now_dt = datetime.fromtimestamp(now_ts, tz=timezone.utc)
        st.text(f"Timestamp: {now_ts}")
        st.text(f"UTC: {now_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        if st.button("📋 Copy Now"):
            st.write(now_ts)

    # 4. Footer
    from utils.common import add_footer
    add_footer()
