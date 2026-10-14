import streamlit as st

from indus_workbench import report, ui

st.set_page_config(page_title="Methods Report", layout="wide")
st.title("Methods Report")
st.markdown(
    "A record of what you ran in this session: data version and fingerprint, settings, "
    "exclusions, controls and results. Attach it to anything you share so a reviewer can "
    "repeat the work exactly."
)

ui.init_settings()
log = st.session_state.get("report", {})
if not log:
    st.info("Nothing recorded yet. Visit the Home page and run some analyses first.")
    st.stop()

md = report.render(log)
st.markdown(md)
st.download_button("Download report (Markdown)", md, file_name="methods_report.md",
                   mime="text/markdown")
