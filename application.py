import streamlit as st
from streamlit_option_menu import option_menu
from src.pipeline.train_pipeline import TrainPipeline
import io

# Page Config
st.set_page_config(page_title="Intelligent Calibration", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
        .main {background-color: #F4F6F9;}
        .stButton > button {
            background-color: #014132;
            color: white;
            border-radius: 5px;
            padding: 0.4em 1em;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #028C6A;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- Navigation Menu ---
selected = option_menu(
    menu_title=None,
    options=["Home", "Calibrate"],
    icons=["house", "sliders"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#014132"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "margin": "0px",
            "color": "white",
            "--hover-color": "#028C6A",
        },
        "nav-link-selected": {"background-color": "#028C6A"},
    }
)

if selected == "Home":
    st.title("Intelligent Calibration System")
    st.markdown("""
    ## Welcome to the **Intelligent Calibration Engine** 
    ### Precision Calibration for Medical & Industrial Sensors  

    #### 📜 Upload your Excel file, define reference and deviated devices, and let our intelligent system handle the rest.  

    #### **💡 Key Features:**  
    - **Automated Calibration** powered by advanced ML models  
    - **Visual Calibration Analysis** through intuitive sensor plots  
    - **Instant Data Correction** with downloadable refined datasets  

    **🔍 Navigate using the menu to get started and transform your sensor data with precision!**
    """)

elif selected == "Calibrate":
    st.title("🧠 Calibrate Device Readings")

    uploaded_file = st.file_uploader("📁 Upload Excel File", type=["xlsx"])
    target_col = st.text_input("🎯 Target Column (e.g., Device)")
    ref_val = st.text_input("✅ Reference Value (e.g., D6)")
    dev_val = st.text_input("⚠️ Deviated Value (e.g., D5)")

    if "calibrated_done" not in st.session_state:
        st.session_state.calibrated_done = False
    if "figures" not in st.session_state:
        st.session_state.figures = []
    if "output_df" not in st.session_state:
        st.session_state.output_df = None
    if "model_used" not in st.session_state:
        st.session_state.model_used = ""

    if st.button("🚀 Run Calibration"):
        if uploaded_file and target_col and ref_val and dev_val:
            with open("temp.xlsx", "wb") as f:
                f.write(uploaded_file.getbuffer())

            pipeline = TrainPipeline("temp.xlsx", target_col, ref_val, dev_val)
            output_df, model_used, figures = pipeline.run_pipeline()

            st.session_state.output_df = output_df
            st.session_state.model_used = model_used
            st.session_state.figures = figures
            st.session_state.calibrated_done = True
            st.success(f"✅ Calibration complete using **{model_used}** model.")
        else:
            st.warning("⚠️ Please fill in all inputs and upload a valid Excel file.")

    if st.session_state.calibrated_done:
        st.subheader("📥 Download or View Results")

        # Buttons and UI layout
        # Top row with buttons only
        button_col1, button_col2 = st.columns(2)

        with button_col1:
            excel_buffer = io.BytesIO()
            st.session_state.output_df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
            excel_buffer.seek(0)
            st.download_button("📥 Download Calibrated Excel",
                               excel_buffer,
                               file_name="calibrated_output.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                               )

        with button_col2:
            show_graphs = st.button("📊 Show Calibration Graphs")

        # Render graphs below — full-width, separate from buttons
        if show_graphs:
            st.subheader("📉 Sensor Distribution Comparisons")
            for fig in st.session_state.figures:
                st.pyplot(fig)
