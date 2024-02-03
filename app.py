from pathlib import Path
import os
import time
from collections import defaultdict

import streamlit as st
import streamlit.components.v1 as stc


import pandas as pd # installed with sequana
from sequana.iem import IEM
from sequana.rnadiff import RNADesign

st.set_page_config(
    page_title="Sample Sheet Validator",
    page_icon="imgs/logo_256x256.png",
    layout="wide",
)


def main():
    st.sidebar.write("Provided by the [Sequana teams](https://github.com/sequana/sequana)")
    st.sidebar.image("imgs/logo_256x256.png")
    st.title("Sample Sheet validator")

    menu = ["Sample Sheet Validation (Illumina)", "RNAdiff Design File (Sequana)", "About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Sample Sheet Validation (Illumina)":
        st.subheader("Illumina case", divider="blue")

        data_file = st.file_uploader(
            ("Drop a valid sample sheet here below and press the **Process** button. "
            'Valid examples are available [here](https://github.com/sequana/st_sample_sheet/)'),
            type=['csv', 'txt'])


        if st.button("Process"):
            if data_file is not None:
                file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
                #st.write(file_details)

                # read to save locally
                data = data_file.read().decode()
                filename = "temp.csv"
                with open(filename, "w") as fout:
                    fout.write(data)
                iem = IEM(filename)

                try:
                    #st.write(f"This sample sheet contains {len(iem.df)} samples")
                    iem.validate()
                except SystemExit as err:
                    st.header("Validation Results", divider='blue')
                    msg = "Error(s) found. :sob: See message below from Sequana"
                    st.error(msg)
                    st.info(err)
                else:
                    st.header("Validation Results", divider='blue')
                    # emoji within div do not seem to work
                    msg = ":champagne: Sample Sheet looks correct. :champagne:"
                    st.success(msg)
                # =============================================================== validation
                st.subheader(" Details about the checks", divider="blue")
                checks = iem.checker()

                msgs = defaultdict(list)
                emoji = {
                    "Error": ":x:",
                    "Success": ":white_check_mark:",
                    "Warning": ":warning:"
                }

                bar = st.progress(0)
                for i,check in enumerate(checks):

                    status = check['status']
                    msg = check['msg']

                    msgs[status].append(f"{status} {emoji[status]}. {msg}\n\n")
                    bar.progress((i + 1) / len(checks) )
                    time.sleep(0.2)

                for error in msgs["Error"]:
                    st.error(error)
                for warning in msgs["Warning"]:
                    st.warning(warning)
                for success in msgs['Success']:
                    st.success(success)

                # =============================================================== original file
                st.subheader("Original file", divider="blue")

                st.code(open(filename).read())

                # =============================================================== corrected file
                if len(msgs['Error']):
                    st.subheader("Corrected file", divider="blue")
                    st.caption("Quick fix here below gets rid of extra trailing ; . Other types of errors are difficult to correct automatically. You will need to correct the file manually. We strongly recommend you to use IEM software (from Illumina) for that. Otherwise, to quickly edit the file, do not use Excel because the sample sheet is not a CSV file despite the fact that the extension is usually .csv   ")

                    iem.quick_fix("test.txt")
                    data = open("test.txt", "r").read()
                    st.download_button(
                        label="Download data as CSV",
                        data=data,
                        file_name='sample.csv',
                        mime='text/csv',
                    )
                    #st.code(open(filename).read())

                # =============================================================== data section
                st.subheader("Data section", divider="blue")
                st.caption("For convenience, we show the data section here below as a CSV file. ")
                df = iem.df.copy()
                st.write(df)
    elif choice == "RNAdiff Design File (Sequana)":
        st.subheader("Sequana RNAdiff design file", divider="blue")

        data_file = st.file_uploader(
            ("Drop a RNAdiff design file here below and press the **Process** button. "
            'Valid examples are available [here](https://github.com/sequana/st_sample_sheet/)'),
            type=['csv', 'txt'])


        if st.button("Process"):
            if data_file is not None:
                file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}

                # read to save locally
                data = data_file.read().decode()
                filename = "temp.csv"
                with open(filename, "w") as fout:
                    fout.write(data)
                try:
                    design = RNADesign(filename)
                    st.write("ok")
                except SystemExit as err:
                    st.header("Validation Results", divider='blue')
                    msg = "Error(s) found. :sob: See message below from Sequana"
                    st.error(msg)
                    st.error(err)


    else:
        st.subheader("About")
        st.info("Built with Streamlit")
        st.info("Thomas Cokelaer")
        st.text("Institut Pasteur, Paris, France")


if __name__ == '__main__':
    main()
