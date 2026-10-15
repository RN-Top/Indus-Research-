"""Geographic and linguistic context: follow the water.

This page is CONTEXT AND HYPOTHESIS, not decipherment. Nothing here was
pre-registered or tested on the holdout, and none of it is evidence about what
the signs say. It is kept separate from the statistical results on purpose.
"""

import pandas as pd
import streamlit as st

from indus_workbench import ui

st.set_page_config(page_title="Geographic Context", layout="wide")
st.title("Geographic & Linguistic Context")
st.warning(
    "**Context and hypothesis, not decipherment.** This page gathers published evidence about where "
    "the Indus people lived, the river that dried up, and words that may have survived in later "
    "languages. None of it has been tested against the signs, and none of it is part of the "
    "pre-registered results on the other pages.")

ui.init_settings()
corpus = ui.load_corpus("indus_website")
ui.sidebar_status(corpus)

sites = pd.read_csv(ui.ROOT / "data" / "site_coordinates.csv")
river = pd.read_csv(ui.ROOT / "data" / "ghaggar_hakra_schematic.csv").sort_values("order")
counts = corpus.df["site"].value_counts() if corpus is not None else pd.Series(dtype=int)
sites["inscriptions"] = sites["site"].map(counts).fillna(0).astype(int)
sites["on_river"] = sites["on_ghaggar_hakra"].str.startswith("yes")

# --- 1. Map -------------------------------------------------------------------
st.header("1. Where the inscriptions come from, and the river that dried up")
st.markdown(
    "Dots are sites with inscriptions in this app's corpus, sized by how many inscriptions each has. "
    "**Red** dots sit on the Ghaggar-Hakra; **brown** dots elsewhere. The **blue line** follows the "
    "Ghaggar-Hakra's course through places documented as lying on it.")

try:
    import pydeck as pdk

    sites["radius"] = 6000 + 400 * sites["inscriptions"].clip(upper=1200) ** 0.5 * 10
    sites["color"] = sites["on_river"].map(lambda r: [164, 68, 42, 220] if r else [140, 110, 70, 200])
    path = [{"name": "Ghaggar-Hakra (schematic)",
             "path": [[r.lon, r.lat] for r in river.itertuples()]}]
    deck = pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(latitude=27.5, longitude=71.5, zoom=4.3),
        layers=[
            pdk.Layer("PathLayer", path, get_path="path", get_color=[47, 74, 122, 230],
                      width_min_pixels=4, pickable=True),
            pdk.Layer("ScatterplotLayer", sites, get_position=["lon", "lat"], get_radius="radius",
                      get_fill_color="color", pickable=True, stroked=True, get_line_color=[46, 33, 24],
                      line_width_min_pixels=1),
            pdk.Layer("TextLayer", sites, get_position=["lon", "lat"], get_text="site", get_size=13,
                      get_color=[46, 33, 24], get_pixel_offset=[0, -16]),
        ],
        tooltip={"text": "{site}\n{inscriptions} inscriptions in this corpus\n{on_ghaggar_hakra}"},
    )
    st.pydeck_chart(deck)
except ImportError:
    st.map(sites.rename(columns={"lon": "longitude", "lat": "latitude"}))
    st.caption("Interactive map unavailable here; showing sites only.")

st.caption(
    "**The blue line is schematic**: straight segments through seven places documented as on the river's "
    "course (Bhirrana, Banawali, Sirsa, Hanumangarh, Kalibangan, Fort Abbas, Derawar). It is not traced "
    "from satellite or survey data, and it omits the course upstream and the terminal lakes. Sites whose "
    "sources give no coordinates (Chanhu-daro, Nausharo, Ganweriwala and smaller sites) are not plotted.")

with st.expander("Site coordinates and sources"):
    st.dataframe(sites[["site", "lat", "lon", "inscriptions", "on_ghaggar_hakra", "source"]],
                 hide_index=True, use_container_width=True)
    st.dataframe(river[["order", "place", "lat", "lon", "why_on_course", "source"]],
                 hide_index=True, use_container_width=True)

st.subheader("What is established, and what is argued")
st.markdown(
    "- **Many sites lie along the river.** Surveys count hundreds of settlements along the Ghaggar-Hakra: "
    "M. R. Mughal (1974–77) mapped over 400 along about 300 miles of the Hakra. Larger counts (S. P. Gupta, "
    "over 600) have been criticised as exaggerated (Sindhav 2016), and S. Ratnagar notes many are local "
    "cultures rather than fully Harappan. ([summary with sources](https://en.wikipedia.org/wiki/Ghaggar-Hakra_River))\n"
    "- **It dried up, but when is argued.** Estimates range from long before the Harappans to about 1900 BCE "
    "(Mughal 1997; Giosan et al. 2012; Chatterjee et al. 2019; Dave et al. 2019).\n"
    "- **Is it the Rigveda's Sarasvati? Debated.** Proponents include Possehl (2002), Kenoyer (1997) and "
    "McIntosh (2008); critics include Thapar (2004), who points to the Helmand, and Witzel (2001), who "
    "argues it was dry before the Vedic period. The question is politically charged; this app takes no side.\n"
    "- **Where people went.** Giosan et al. (*PNAS*, 2012) find that as monsoon rains weakened and the rivers "
    "declined, settlement shifted **east toward the Ganges basin**, from big river-fed cities to smaller "
    "farming communities ([WHOI summary](https://www.whoi.edu/press-room/news-release/climate-change-led-to-collapse-of-ancient-indus-civilization-study-finds)).")

# --- 2. Water words ------------------------------------------------------------
st.header("2. Words that may have outlived the people")
st.markdown(
    "Early Sanskrit borrowed a few hundred words from languages already spoken in the region, and some "
    "river names look older than Sanskrit. If the Indus language survives anywhere, it may be in names "
    "like these. The table lists the cases tied to **rivers and water** in the sources reviewed "
    "(full review: `results/substrate_angle.md`).")

words = pd.DataFrame([
    {"word": "Sindhu", "what": "the Indus river", "proposal":
     "Has an Indo-European etymology, but may also continue an older local word *sind-/send-, found from "
     "Hunza to Sindh and in Mesopotamian references to Meluhhan goods (sinda)", "status": "Witzel calls it preliminary",
     "source": "https://list.indology.info/pipermail/indology/1999-October/018781.html"},
    {"word": "Sutudrī", "what": "the Sutlej river", "proposal":
     "Possibly from a Munda-like root meaning 'float' or 'drift'", "status": "proposal (Witzel 1999)",
     "source": "https://www.academia.edu/713996"},
    {"word": "Vipāś", "what": "the Beas river", "proposal":
     "Linked to earlier forms such as *vibal*", "status": "proposal (Witzel 1999)",
     "source": "https://www.academia.edu/713996"},
    {"word": "Kubhā", "what": "a river (the Kabul)", "proposal":
     "Probably a loan; compared with a Munda word for 'bent'", "status": "proposal (Witzel 1999)",
     "source": "https://www.academia.edu/713996"},
    {"word": "Rigvedic river names in general", "what": "29 hydronyms analysed", "proposal":
     "About one fifth have a more or less probable pre-Indo-Aryan origin (Burushaski for 2, Dravidian possible for 4)",
     "status": "probability judgement (Blažek 2016)", "source": "https://digilib2.phil.muni.cz/en/node/27489"},
    {"word": "nīr (a sign reading)", "what": "'water', proposed for the two-wavy-lines sign", "proposal":
     "Parpola's Proto-Dravidian reading of an Indus sign; a decipherment proposal, not a loanword",
     "status": "untested here (Phase 2 paused)",
     "source": "https://www.harappa.com/sites/default/files/pdf/indusscript(2).pdf"},
])
st.dataframe(words, hide_index=True, use_container_width=True,
             column_config={"source": st.column_config.LinkColumn("source")})

st.markdown(
    "**Why none of this can be tested against the signs yet.** To find a word like *Sindhu* in the "
    "inscriptions, you would first need to know what the signs sound like, which is the decipherment "
    "itself. The loop breaks only with an outside anchor: a bilingual inscription, Meluhhan names written "
    "in cuneiform, or an independent word list scored with the Reading Tester.\n\n"
    "**A hunch worth recording:** if water was central to Indus life, as their drains and the Great Bath "
    "suggest, water and river words might be among the likeliest survivals. That is a hypothesis, not a finding.")
