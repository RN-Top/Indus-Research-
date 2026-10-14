"""Smoke test: execute every Streamlit page against a stub `streamlit` module
and a synthetic corpus, so page logic runs end to end without a browser or
network. Run:  python tests/smoke_pages.py
(The real UI is still best checked with `streamlit run app.py`.)"""

import runpy
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from test_core import synthetic_csv  # noqa: E402


class Stop(Exception):
    pass


class State(dict):
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        self[k] = v


class Ctx:
    def __getattr__(self, name):
        return getattr(st, name)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


st = types.ModuleType("streamlit")
st.session_state = State()
CALLS = []


def _noop(*a, **k):
    return None


def _val(key, default):
    if key and key in st.session_state:
        return st.session_state[key]
    if key:
        st.session_state[key] = default
    return default


def radio(label, options, index=0, key=None, **k):
    return _val(key, list(options)[index])


def selectbox(label, options, index=0, key=None, **k):
    options = list(options)
    return _val(key, options[index] if options else None)


def checkbox(label, value=False, key=None, **k):
    return _val(key, value)


def slider(label, min_value=None, max_value=None, value=None, step=None, key=None, **k):
    return _val(key, value if value is not None else min_value)


def select_slider(label, options, value=None, key=None, **k):
    return _val(key, value if value is not None else options[0])


def number_input(label, min_value=None, max_value=None, value=None, step=None, key=None, **k):
    return _val(key, value)


def text_input(label, value="", key=None, **k):
    return _val(key, value)


def columns(spec, **k):
    n = spec if isinstance(spec, int) else len(spec)
    return [Ctx() for _ in range(n)]


def tabs(labels):
    return [Ctx() for _ in labels]


def stop():
    raise Stop()


def cache_data(func=None, **k):
    return func if func else (lambda f: f)


for name in ["title", "header", "subheader", "markdown", "caption", "write", "info", "warning",
             "error", "success", "metric", "dataframe", "json", "bar_chart", "line_chart",
             "download_button", "set_page_config", "progress"]:
    setattr(st, name, _noop)
st.progress = lambda *a, **k: types.SimpleNamespace(progress=_noop)
st.radio, st.selectbox, st.checkbox, st.toggle = radio, selectbox, checkbox, checkbox
st.slider, st.select_slider, st.number_input = slider, select_slider, number_input
st.text_input, st.text_area = text_input, text_input
st.multiselect = lambda label, options, key=None, **k: _val(key, [])
st.file_uploader = lambda *a, **k: None
st.button = lambda *a, **k: True
st.columns, st.tabs, st.stop = columns, tabs, stop
st.expander = st.spinner = lambda *a, **k: Ctx()
st.sidebar = Ctx()
st.cache_data = cache_data
sys.modules["streamlit"] = st

import json  # noqa: E402
import tempfile  # noqa: E402

from indus_workbench import data, hypotheses, ui  # noqa: E402

import os  # noqa: E402

RAW = synthetic_csv()
if not os.environ.get("REAL"):  # REAL=1 runs the pages on the bundled real data instead
    data.load_raw = lambda key: (RAW, "synthetic test corpus")

# A registered hypothesis in a temporary folder, plus a tampered one that must be refused.
tmp = Path(tempfile.mkdtemp())
good = hypotheses.freeze(hypotheses.new_hypothesis("precedes", {"a": "A", "b": "B"}, "x", n_perm=200))
bad = hypotheses.freeze(hypotheses.new_hypothesis("position", {"a": "Z", "where": "end"}, "y", n_perm=200))
bad["params"]["where"] = "start"
(tmp / "good.json").write_text(json.dumps(good))
(tmp / "tampered.json").write_text(json.dumps(bad))
ui.HYPOTHESIS_DIR = tmp

# Pre-fill the Hypothesis Lab form so explore/register run.
st.session_state.update({"x_a": "A", "x_b": "B", "x_stmt": "A precedes B (synthetic test)",
                         "author": "smoke"})

pages = [ROOT / "app.py"] + sorted((ROOT / "pages").glob("*.py"))
failed = 0
for p in pages:
    try:
        runpy.run_path(str(p), run_name="__main__")
        status = "ok"
    except Stop:
        status = "ok (stopped)"
    except Exception as e:  # noqa: BLE001
        status = f"FAIL: {type(e).__name__}: {e}"
        failed += 1
        import traceback
        traceback.print_exc()
    print(f"{p.name:30s} {status}")

print("report sections:", sorted(st.session_state.get("report", {})))
sys.exit(1 if failed else 0)
