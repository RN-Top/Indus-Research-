"""Find-spot map: where Indus inscriptions were found, over schematic ancient waterways and routes.

Shows static/findspot_map.html, built by scripts/findspot_map.py. Geography only:
"has a closer" uses exploration texts; holdout texts are counted, never read.
"""

import streamlit as st
import streamlit.components.v1 as components

from indus_workbench import ui

st.set_page_config(page_title="Find-spot Map", layout="wide")
ui.init_settings()
st.title("Find-spot Map")
st.caption("Exploratory. Routes and old river channels are schematic reconstructions, not surveyed lines. "
           "Full analysis: `results/findspots_waterways.md`. The same map opens on its own at "
           "`static/findspot_map.html`.")

page = ui.ROOT / "static" / "findspot_map.html"
if page.exists():
    components.html(page.read_text(), height=1900, scrolling=True)
else:
    st.warning("The map has not been built yet. Run `python scripts/findspot_map.py <natural-earth-folder>`.")
