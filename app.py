import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
from PIL import Image 
import os
from pathlib import Path

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

                if os.path.exists(data_file.name) is False:
                    filename = f"/mount/src/st_sample_sheet/{data_file.name}"
                else:
                    filename = data_file.name
                
                from sequana.iem import IEM
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
