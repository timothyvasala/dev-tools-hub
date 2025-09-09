import streamlit as st
from datetime import datetime, timezone
import time
from utils.common import setup_page, show_result, add_footer

# ── Cache timestamp conversions ────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def ts_to_date(ts_value: float, fmt: str, tz_str: str) -> str:
    """Convert Unix timestamp (seconds or ms) to formatted date string."""
    if ts_value > 1e12:
        ts_value /= 1000
    tz = timezone.utc if tz_str == "UTC" else None
    dt = datetime.fromtimestamp(ts_value, tz=tz)
    return dt.isoformat() if fmt == "ISO 8601" else dt.strftime(fmt)

@st.cache_data(show_spinner=False)
def date_to_ts(date_str: str, tz_str: str) -> int:
    """Convert date string to Unix timestamp (seconds)."""
    # Handle ISO vs space-separated format
    if "T" in date_str:
        dt = datetime.fromisoformat(date_str)
    else:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    if tz_str == "UTC":
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())
# ────────────────────────────────────────────────────────────────────────────────

def render():
    # 1. Header
    setup_page(
        "⏰ Unix Timestamp Converter",
        "Convert between Unix timestamps and human-readable dates."
    )

    # 2. Select mode
    mode = st.radio("Conversion type:", ["Timestamp → Date", "Date → Timestamp", "Bulk Conversion"])

    if mode == "Timestamp → Date":
        ts = st.text_input("Enter Unix timestamp (seconds or ms):", "")
        fmt = st.selectbox("Output format:", ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "ISO 8601"])
        tz = st.selectbox("Timezone:", ["Local", "UTC"])
        if st.button("🔄 Convert"):
            try:
                ts_val = float(ts)
                out = ts_to_date(ts_val, fmt, tz)
                show_result(out)
            except Exception as e:
                st.error(f"❌ Error: {e}")

    elif mode == "Date → Timestamp":
        date_str = st.text_input("Enter date/time string:", "2025-01-01 12:00:00")
        tz = st.selectbox("Interpret as:", ["Local", "UTC"])
        if st.button("🔄 Convert"):
            try:
                ts = date_to_ts(date_str, tz)
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
                        ts_val = float(line)
                        out = ts_to_date(ts_val, "ISO 8601", "UTC")
                        results.append(f"{line} → {out}")
                    else:
                        ts = date_to_ts(line, "UTC")
                        results.append(f"{line} → {ts}")
                except Exception as e:
                    errors.append(f"Line {i}: {e}")
            if results:
                show_result("\n".join(results))
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
    add_footer()
