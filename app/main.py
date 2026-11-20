"""Streamlit entry point: `streamlit run app/main.py`"""
import json
from pathlib import Path

import streamlit as st

from app.core import milestone_1, milestone_3

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "results" / "evaluation.json"


@st.cache_resource(show_spinner=False)
def _merged_model():
    from app.core import milestone_2, milestone_5

    trained = milestone_2(steps=40)
    return milestone_5(trained)


def _load_report():
    if not REPORT_PATH.exists():
        return None
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


st.set_page_config(page_title="Product Description Enhancer", layout="wide")
st.title("Product Description Enhancer")
st.write(
    "Turn a short product spec into a longer description. "
    "The preview below is a template. The recorded table is GPT-2 after a short LoRA fine-tune, merged back into the base weights."
)

info = milestone_1()
report = _load_report()
count, spec_words, desc_words = st.columns(3)
count.metric("Training pairs", info["num_examples"])
spec_words.metric("Average spec length (words)", info["avg_spec_length"])
desc_words.metric("Average description length (words)", info["avg_desc_length"])

st.subheader("Generate")
spec = st.text_area(
    "Product spec",
    height=100,
    placeholder="Stainless steel water bottle, 750ml, double-wall insulated, leak-proof lid",
)
generator = st.radio(
    "Generator",
    ["Template preview", "Merged LoRA model"],
    horizontal=True,
)
if st.button("Generate", type="primary"):
    cleaned = spec.strip()
    if not cleaned:
        st.warning("Enter a product spec first.")
    elif generator == "Template preview":
        st.write(milestone_3(cleaned))
    else:
        with st.spinner("Training the LoRA adapter and merging it. The first run takes several minutes."):
            bundle = _merged_model()
        st.write(milestone_3(cleaned, bundle["model"], bundle["tokenizer"]))

st.subheader("Recorded evaluation")
if report is None:
    st.info("No recorded run is saved yet. From the project folder run: python -m app.record")
else:
    lora = report["lora"]
    averages = report["averages"]
    loss_col, final_col, overlap_col = st.columns(3)
    loss_col.metric("Loss before LoRA steps", lora["baseline_loss"])
    final_col.metric("Loss after LoRA steps", lora.get("final_eval_loss", lora["final_loss"]))
    overlap_col.metric(
        "Keyword overlap after LoRA",
        averages["lora_keyword_overlap"],
        delta=round(averages["lora_keyword_overlap"] - averages["untouched_keyword_overlap"], 2),
    )
    st.caption(report["data_source"])
    st.dataframe(
        [
            {
                "method": row["method"],
                "keyword overlap": row["keyword_overlap"],
                "composite": row["composite_score"],
                "spec": row["spec"],
                "generated": row["generated"],
            }
            for row in report["samples"]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.subheader("Baseline and limits")
    for limit in report["limits"]:
        st.markdown(f"- {limit}")
