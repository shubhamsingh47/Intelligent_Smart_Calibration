import io
from src.pipeline.train_pipeline import TrainPipeline
import streamlit as st


def run_calibration(uploaded_file, target_col, ref_val, dev_val):
    pipeline = TrainPipeline(
        uploaded_file=uploaded_file,
        target_column=target_col,
        reference_value=ref_val,
        deviated_value=dev_val
    )
    output_df, model_used, figures = pipeline.run_pipeline()

    st.session_state.output_df = output_df
    st.session_state.model_used = model_used
    st.session_state.figures = figures
    st.session_state.calibrated_done = True
    st.success(f"✅ Calibration completed")


def setup_session_state():
    if "calibrated_done" not in st.session_state:
        st.session_state.calibrated_done = False
    if "figures" not in st.session_state:
        st.session_state.figures = []
    if "output_df" not in st.session_state:
        st.session_state.output_df = None
    if "model_used" not in st.session_state:
        st.session_state.model_used = ""


def show_results():
    st.subheader("📥 Download or View Results")

    button_col1, button_col2 = st.columns(2)

    with button_col1:
        excel_buffer = io.BytesIO()
        st.session_state.output_df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
        excel_buffer.seek(0)
        st.download_button("Download Calibrated Excel",
                           excel_buffer,
                           file_name="calibrated_output.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           icon=":material/download:"
                           )

    with button_col2:
        show_graphs = st.button("📊 Show Calibration Graphs")

    if show_graphs:
        st.subheader("📉 Sensor Distribution Comparisons")
        for fig in st.session_state.figures:
            st.pyplot(fig)
