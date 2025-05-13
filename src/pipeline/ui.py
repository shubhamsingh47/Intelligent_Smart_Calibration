import streamlit as st
from streamlit_option_menu import option_menu
from src.pipeline.calibration import run_calibration, setup_session_state, show_results


def render_ui():
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

    # Navigation Menu
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

        #### 📜 Upload your Excel, CSV or TSV  file, define reference and deviated devices, and let our intelligent system handle the rest.  

        #### **💡 Key Features:**  
        - **Automated Calibration** powered by advanced ML models  
        - **Visual Calibration Analysis** through intuitive sensor plots  
        - **Instant Data Correction** with downloadable refined datasets  

        **🔍 Navigate using the menu to get started and transform your sensor data with precision!**
        """)

    elif selected == "Calibrate":
        st.title("Calibrate Device Readings")

        uploaded_file = st.file_uploader("Upload Your File", type=["xlsx", "csv", "tsv", "xls"], key="file")
        target_col = st.text_input("Target Column (e.g., Output Feature )", key="target")
        ref_val = st.text_input("Reference Value (e.g., True Values)", key="ref")
        dev_val = st.text_input("Deviated Value (e.g., Drifted Values)", key="dev")

        setup_session_state()

        if st.session_state.get("trigger_reset", True):
            st.session_state.calibrated_done = False

        if st.button("Run Calibration"):
            if uploaded_file and target_col and ref_val and dev_val:
                st.session_state.trigger_reset = False
                run_calibration(uploaded_file, target_col, ref_val, dev_val)
            else:
                st.warning("Please fill in all inputs and upload a valid Excel file.")

        if st.session_state.calibrated_done:
            show_results()

        if uploaded_file != st.session_state.get("prev_file") or \
                target_col != st.session_state.get("prev_target") or \
                ref_val != st.session_state.get("prev_ref") or \
                dev_val != st.session_state.get("prev_dev"):
            st.session_state.trigger_reset = True
            st.session_state.prev_file = uploaded_file
            st.session_state.prev_target = target_col
            st.session_state.prev_ref = ref_val
            st.session_state.prev_dev = dev_val
