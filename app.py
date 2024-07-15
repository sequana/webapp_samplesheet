import os
import tempfile
import time
from collections import defaultdict
from pathlib import Path

import pandas as pd  # installed with sequana
import requests
import streamlit as st
from sequana.iem import IEM
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Illumina Sample Sheet Validator",
    page_icon="imgs/logo_256x256.png",
    layout="wide",
    menu_items={"Report a bug": "https://github.com/sequana/webapp_samplesheet/issues/new/choose"},
)


def print_checks(checks):

    msgs = defaultdict(list)
    emoji = {"Error": ":x:", 
            "Succcess": ":white_check_mark:", # a temporary hack
            "Success": ":white_check_mark:", 
            "Warning": ":warning:"}

    bar = st.progress(0)
    for i, check in enumerate(checks):
        status = check["status"]
        msg = check["msg"]

        msgs[status].append(f"{status} {emoji[status]}. {msg}\n\n")
        bar.progress((i + 1) / len(checks))
        time.sleep(0.2)

    for error in msgs["Error"]:
        st.error(error)
    for warning in msgs["Warning"]:
        st.warning(warning)
    for success in msgs["Success"]:
        st.success(success)
    return msgs


def main():
    st.sidebar.write("Provided by the [Sequana teams](https://github.com/sequana/sequana)")
    st.sidebar.image("imgs/logo_256x256.png")
    st.title("Sample Sheet and Design Validator")

    menu = ["Sample Sheet Validation (Illumina)", "Examples", "About"]

    # 1. as sidebar menu
    with st.sidebar:
        choice = option_menu(
            "Main Menu", menu, icons=["gear", "gear", "cloud-upload", ""], menu_icon="cast", default_index=0
        )

    if choice == "Sample Sheet Validation (Illumina)":
        st.markdown(
            "Please select a validator from the left hand side menu (default is Illumina Sample Sheet). Valid examples are available [here](https://github.com/sequana/st_sample_sheet/)"
        )
        st.subheader("Illumina case", divider="blue")

        data_file = st.file_uploader(
            "Drop a sample sheet here below and press the **Process** button. ", type=["csv", "txt"]
        )

        if st.button("Process"):

            samplesheet = data_file.read().decode()
            try:
                process_sample_sheet(data_file, samplesheet)
            except Exception as err:
                import urllib.parse
                base_url = f"https://github.com/sequana/webapp_samplesheet/issues/new"

                samplesheet = "\n".join(["    "+x for x in samplesheet.split("\n")])
                params = {
                    'title': "Automatic error from the check-my-sample-sheet website",
                    'body': f"Dear developer(s),\n\nI encountered an expected error using the following samplesheet \n\n{samplesheet}\n\n Here is the full error message\n\n     {err}. Please tell us what you think might be the reason for the error"
                }
                url = f"{base_url}?{urllib.parse.urlencode(params)}"
                st.markdown(f'<div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;"> Sorry but and unknown error occurred. Please create an issue <a href="{url}">here</a> to report it. A page will open; you will need to clik on the "Submit new issue" button </div>', unsafe_allow_html=True)

                raise Exception(err)

    elif choice == "Examples":
        st.subheader("1 - Illumina")
        url = "https://raw.githubusercontent.com/sequana/webapp_samplesheet/main/examples/sample_sheet.csv"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode()
        st.write(
            """Here below is a simple Illumina Sample Sheet. We can see sections in square brackets.
There are 4 of them. The [Header], [Reads], and [Settings] are optional (here [Settings] is missing.
The  [Data] section is compulsary. The [Data] section should be a valid comma separated column section."""
        )
        st.code(data, language="bash")


    else:
        st.subheader("About")
        st.markdown(
            "This application is part of the [Sequana Project](https://github.com/sequana), which is dedicated to NGS analysis. Please see the [online documentation](https://sequana.readthdocs.io) as well as https://sequana.github.io for more information; the code used in this application is based on the [IEM module](https://github.com/sequana/sequana) of the Sequana Python library"
        )
        st.info("Application Author: Thomas Cokelaer")
        #st.info("Application Reviewer/Contributors: Laure Lemée, Etienne Kornobis, Rania Ouazahrou")


def process_sample_sheet(data_file, samplesheet):
    if data_file is not None:
        file_details = {"Filename": data_file.name, "FileType": data_file.type, "FileSize": data_file.size}

        # read to save locally
        #samplesheet = data_file.read().decode()

        with tempfile.NamedTemporaryFile(delete=False, mode="w") as fout:
            fout.write(samplesheet)
            fout.close()
            iem = IEM(fout.name)

        try:
            # st.write(f"This sample sheet contains {len(iem.df)} samples")
            iem.validate()
        except SystemExit as err:
            st.header("Validation Results", divider="blue")
            msg = "Error(s) found. :sob: See message below from Sequana"
            st.error(msg)
            st.info(err)
        else:
            st.header("Validation Results", divider="blue")
            # emoji within div do not seem to work
            msg = ":champagne: Sample Sheet looks correct. :champagne:"
            st.success(msg)
        # =============================================================== validation
        st.subheader(" Details about the checks", divider="blue")
        checks = iem.checker()
        msgs = print_checks(checks)

        # =============================================================== original file
        st.subheader("Original file", divider="blue")
        st.code(samplesheet)

        # =============================================================== corrected file
        if len(msgs["Error"]):
            st.subheader("Corrected file", divider="blue")
            st.caption(
                "Quick fix here below gets rid of extra trailing ; . Other types of errors are difficult to correct automatically. You will need to correct the file manually. We strongly recommend you to use IEM software (from Illumina) for that. Otherwise, to quickly edit the file, do not use Excel because the sample sheet is not a CSV file despite the fact that the extension is usually .csv   "
                )
            with tempfile.NamedTemporaryFile(delete=False, mode="w") as fout:
                iem.quick_fix(fout.name)
                fout.close()
                with open(fout.name, "r") as fin:

                    st.download_button(
                        label="Download data as CSV",
                        data=fin.read(),
                        file_name="sample.csv",
                        mime="text/csv",
                    )

        # =============================================================== data section
        st.subheader("Data section", divider="blue")
        st.caption(
            "For convenience, we show the data section here below as a CSV file. It should be coherent (e.g. index on a single column"
        )
        df = iem.df.copy()
        st.write(df)


if __name__ == "__main__":
    main()
