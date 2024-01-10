from pathlib import Path
import os

import streamlit as st
import streamlit.components.v1 as stc

import pandas as pd # installed with sequana
from sequana.iem import IEM

st.set_page_config(
    page_title="Sample Sheet Validator",
    page_icon="imgs/logo_256x256.png",
    layout="wide",
)

def main():
    st.sidebar.write("Provided by the [Sequana teams](https://github.com/sequana/sequana)")
    st.sidebar.image("imgs/logo_256x256.png")
    st.title("Sample Sheet validator")

    menu = ["Sample Sheet Validation (Illumina)","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Sample Sheet Validation (Illumina)":
        st.subheader("Illumina case")
        data_file = st.file_uploader("Upload CSV",type=['csv'])

        st.markdown("""
        This validator checks for
        - presence of ; at the end of lines indicated an edition with excel that
              wrongly transformed the data into a pure CSV file
        - inconsistent numbers of columns in the [DATA] section, which must be
              CSV-like section
        - Extra lines at the end are ignored
        - special characters are forbidden except - and _
        - for Sample_ID column uniqueness
        - for index uniqueness (if single index)
        - for combo of dual indices uniqueness
        - that sample names are unique
        """)

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
                    st.write("An error was found :sob: See message below")
                    st.write(err)
                else:
                    st.write(":champagne: Sample Sheet looks correct.")
                finally:
                    st.write("The data section looks like:")
                    st.write(iem.df)
    else:
        st.subheader("About")
        st.info("Built with Streamlit")
        st.info("Thomas Cokelaer")
        st.text("Institut Pasteur, Paris, France")


if __name__ == '__main__':
    main()
