from pathlib import Path
import os

import streamlit as st
import streamlit.components.v1 as stc

import pandas as pd # installed with sequana
from sequana.iem import IEM

st.set_page_config(
    page_title="Sample Sheet Validator",
    page_icon="imgs/logo_2566x256.png",
    layout="wide",
    #initial_sidebar_state="expanded",
    #menu_items={
    #    "Get help": "https://github.com/",
    #    "Report a bug": "https://github.com/",
    #    "About": """
    #        ## Streamly Streamlit Assistant
    #        
    #        **GitHub**: https://github.com/sequana/st_sample_sheet
    #
    #    """
    #}
)

def main():
    st.title("Sample Sheet validator")

    menu = ["Sample Sheet Validation (Illumina)","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Sample Sheet Validation (Illumina)":
        st.subheader("Illumina case")
        data_file = st.file_uploader("Upload CSV",type=['csv'])
        if st.button("Process"):
            if data_file is not None:
                file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
                st.write(file_details)

                # read to save locally
                data = data_file.read().decode()
                filename = "temp.csv"
                with open(filename, "w") as fout:
                    fout.write(data)
                iem = IEM(filename)
                try:
                    st.write(f"This sample sheet contains {len(iem.df)} samples")
                    iem.validate()
                except SystemExit as err:
                    st.write(err)
                else:
                    st.write("OK")
    else:
        st.subheader("About")
        st.info("Built with Streamlit")
        st.info("Thomas Cokelaer")
        st.text("Institut Pasteur, Paris, France")



if __name__ == '__main__':
    main()
