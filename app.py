#
#  This file is part of Sequana software
#
#  Copyright (c) 2023-2024 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/webapp_samplesheet
#  documentation: http://github.com/sequana/webapp_samplesheet/
#
##############################################################################

import tempfile
import time
from collections import defaultdict

import requests
import streamlit as st
from sequana.iem import SampleSheet
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Illumina Sample Sheet Validator",
    page_icon="imgs/logo_256x256.png",
    layout="wide",
    menu_items={"Report a bug": "https://github.com/sequana/webapp_samplesheet/issues/new/choose"},
)

version = "1.0.0"


def print_checks(checks):
    """
    This function processes a list of checks and displays them in a Streamlit application.
    Each check is represented as a dictionary with 'status' and 'msg' keys. The function
    updates a color-coded progress bar based on the number of errors, warnings, and successes.
    It also prints the messages associated with each check in the appropriate Streamlit function
    (st.error, st.warning, st.success).

    Parameters:
    checks (list): A list of dictionaries, where each dictionary represents a check.
                   The dictionary should have 'status' and 'msg' keys.

    Returns:
    dict: A dictionary containing the messages associated with each status (Error, Warning, Success).
    """

    # func to update colorbar
    def colored_bar(success, warning, error, completed=0):
        return f"""
        <div style="display: flex; width: {completed}%; height: 30px; border: 1px solid black;">
            <div style="width: {success}%; background-color: green;"></div>
            <div style="width: {warning}%; background-color: yellow;"></div>
            <div style="width: {error}%; background-color: red;"></div>
        </div>
        """

    def add_legend(success, warning, error):
        # finally add the legend
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; width: 50%;">
                 <div style="display: flex; align-items: center;">
                     <div style="width: 20px; height: 20px; background-color: green; margin-right: 5px;"></div>
                    <span>Success ({success})</span>
                </div>
                <div style="display: flex; align-items: center;">
                     <div style="width: 20px; height: 20px; background-color: yellow; margin-right: 5px;"></div>
                    <span>Warning ({warning})</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; background-color: red; margin-right: 5px;"></div>
                    <span>Error ({error})</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    msgs = defaultdict(list)
    emoji = {"Error": ":x:", "Success": ":white_check_mark:", "Warning": ":warning:"}

    # Placeholder for the colored bar
    bar_placeholder = st.empty()
    bar_placeholder.markdown(colored_bar(0, 0, 0, 0), unsafe_allow_html=True)
    # add_legend(0,0,0)

    counter = {"Error": 0, "Warning": 0, "Success": 0}

    N = len(checks)  # Number of checks
    for i, check in enumerate(checks):
        status = check["status"]
        msg = check["msg"]

        msgs[status].append(f"{status} {emoji[status]}. {msg}\n\n")
        time.sleep(0.15)

        counter[status] += 1

        S = sum(counter.values())
        success = counter["Success"] / S * 100
        warning = counter["Warning"] / S * 100
        error = counter["Error"] / S * 100

        completed = min(round(100 * (S / float(N))), 100)
        bar_placeholder.markdown(colored_bar(success, warning, error, completed), unsafe_allow_html=True)

    # finally add the legend
    _, col2, _ = st.columns([1, 4, 1])
    with col2:
        add_legend(counter["Success"], counter["Warning"], counter["Error"])

    # prints all message
    for error in msgs["Error"]:
        st.error(error)
    for warning in msgs["Warning"]:
        st.warning(warning)
    for success in msgs["Success"]:
        st.success(success)
    return dict(msgs)


def main():
    st.sidebar.write("Provided by the [Sequana teams](https://github.com/sequana/sequana)")
    st.sidebar.image("imgs/logo_256x256.png")
    st.title(f"Sample Sheet and Design Validator (v{version})")
    if "code" not in st.session_state:
        st.session_state.code = ""

    menu = ["Sample Sheet Validation (Illumina)", "Examples", "About"]

    # 1. as sidebar menu
    with st.sidebar:
        choice = option_menu(
            "Main Menu", menu, icons=["gear", "gear", "cloud-upload", ""], menu_icon="cast", default_index=0
        )

    if choice == "Sample Sheet Validation (Illumina)":
        st.markdown(
            "Please provide a Sample Sheet file to validate here below. Valid examples are available [here](https://github.com/sequana/st_sample_sheet/ and in the Example section.)"
        )
        st.subheader("Input SampleSheet file", divider="blue")

        # create a 3-column layout
        col1, col2, col3 = st.columns([4, 1, 4])
        with col1:
            data_file = st.file_uploader(
                "Drop a sample sheet here below and press the **Process** button. ", type=["csv", "txt"]
            )
        with col2:
            # Centered "OR" text
            st.markdown("<div style='text-align: center;'><br><br>OR</div>", unsafe_allow_html=True)

        with col3:
            code = st.text_area(
                "Paste your code here and press the **Process** button", value=st.session_state.code, key="code_area"
            )

        if st.button("Process"):

            try:
                samplesheet = data_file.read().decode()
                # st.experimental_rerun()
            except:
                samplesheet = code
                data_file = None

            try:
                process_sample_sheet(data_file, samplesheet)
            except Exception as err:
                import urllib.parse

                base_url = f"https://github.com/sequana/webapp_samplesheet/issues/new"

                samplesheet = "\n".join(["    " + x for x in samplesheet.split("\n")])
                params = {
                    "title": "Automatic error from the check-my-sample-sheet website",
                    "body": f"Dear developer(s),\n\nI encountered an expected error using the following samplesheet \n\n{samplesheet}\n\n Here is the full error message\n\n     {err} \n\n Please tell us what you think might be the reason for the error",
                }
                url = f"{base_url}?{urllib.parse.urlencode(params)}"
                st.markdown(
                    f'<div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;"> Sorry but and unknown error occurred. Please create an issue <a href="{url}">here</a> to report it. A page will open; you will need to clik on the "Submit new issue" button </div>',
                    unsafe_allow_html=True,
                )

                raise Exception(err)

    elif choice == "Examples":
        st.write("Here are some valid sample sheets examples.")
        st.subheader("1 - Illumina Minimalist Example")
        st.write(
            """In this example, we simplify the sample sheet to keep only the [DATA] section and mandatory columns(index and Sample_ID).
                 Note that the 'Sample_ID' is not mandatory with bcl2fastq but we made it mandatory in this application (design choice)"""
        )
        st.code(
            """[Data]
Sample_ID,index
ID1,TGACCA
ID2,CATTTT"""
        )

        st.subheader("2 - Illumina With two indices")
        url = "https://raw.githubusercontent.com/sequana/webapp_samplesheet/main/examples/sample_sheet.csv"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode()
        st.write(
            """A more common example is shown here below. We can see several sections in square brackets.
There should be 4 of them. Here, we show the [Header], [Reads] and [Data] sections. The [Settings] is missing here.
According to the Illumina specs, all sections are optional including the [Data] section. However,  in such case, all
called reads are stored as undetermined. Not very useful. We make the [Data] section mandatory."""
        )
        st.code(data, language="bash")

        st.subheader("3 - Illumina one index and settings section")
        url = "https://raw.githubusercontent.com/sequana/webapp_samplesheet/main/examples/sample_sheet_settings_single_index.csv"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode()
        st.code(data, language="bash")

        st.subheader("4 - Illumina example of a wrong sample sheet")
        url = "https://raw.githubusercontent.com/sequana/webapp_samplesheet/main/examples/Bad_SampleSheet_alphanum.csv"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode()

    else:
        st.subheader("About")
        st.markdown(
            "This application is part of the [Sequana Project](https://github.com/sequana), which is dedicated to NGS analysis. "
            "Please see the [online documentation](https://sequana.readthdocs.io) as well as https://sequana.github.io for more information."
            "The code used in this application is based on the [IEM module](https://github.com/sequana/sequana) of the Sequana Python library."
            "It was created based on the bcl2fastq documentation v2.20 and should users to demultiplex their data properly."
        )
        st.info("Application Author: Thomas Cokelaer")
        # st.info("Application Reviewer/Contributors: Laure Lemée, Etienne Kornobis, Rania Ouazahrou")


def process_sample_sheet(data_file, samplesheet):
    """
    This function processes an uploaded sample sheet file and performs validation checks.
    It saves the file locally, creates a SampleSheet object using the Sequana library,
    and then validates the sample sheet. If errors are found, they are displayed in the
    Streamlit application. The function also provides options to download the corrected
    sample sheet file and view the data section as a CSV file.

    Parameters:
    data_file (FileIO): The uploaded sample sheet file.
    samplesheet (str): The content of the sample sheet file.

    Returns:
    None
    """
    st.write("header")
    if data_file is not None:
        file_details = {"Filename": data_file.name, "FileType": data_file.type, "FileSize": data_file.size}
    else:
        pass

    if 1 == 1:

        # read to save locally
        # samplesheet = data_file.read().decode()

        with tempfile.NamedTemporaryFile(delete=False, mode="w") as fout:
            fout.write(samplesheet)
            fout.close()
            iem = SampleSheet(fout.name)

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
