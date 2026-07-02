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
from pathlib import Path

import requests
import streamlit as st
from sequana.iem import SampleSheetFactory, get_sample_sheet_version
from streamlit_option_menu import option_menu

# directory holding this module, used to resolve packaged assets (imgs, examples)
# regardless of the current working directory.
HERE = Path(__file__).resolve().parent
LOGO = str(HERE / "imgs" / "logo_256x256.png")

st.set_page_config(
    page_title="Check My Sample Sheet",
    page_icon=LOGO,
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


if "code_input" not in st.session_state:
    st.session_state.code_input = ""

# used to reset the file_uploader when an example is loaded: bumping this counter
# changes the widget key, which forces Streamlit to drop any previously uploaded file.
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


def load_example(filename):
    """Load example file from examples directory."""
    examples_dir = Path(__file__).parent / "examples"
    with open(examples_dir / filename, "r") as f:
        return f.read()


def set_example(filename):
    """Callback to load example into the textarea session state.

    Also resets the file_uploader (by bumping its key) so a previously uploaded
    file does not silently take precedence over the loaded example.
    """
    st.session_state.code_input = load_example(filename)
    st.session_state.uploader_key += 1


def main():
    st.sidebar.write("Provided by the [Sequana team](https://github.com/sequana/sequana)")
    st.sidebar.image(LOGO)
    st.title(f"Check My Sample Sheet (v{version})")

    menu = ["Sample Sheet Validation (Illumina)", "Examples", "About", "How to cite"]

    # 1. as sidebar menu
    with st.sidebar:
        choice = option_menu(
            "Main Menu", menu, icons=["gear", "gear", "cloud-upload", ""], menu_icon="cast", default_index=0
        )
        st.markdown(
            "**Resources:**\n\n"
            "- [Source code](https://github.com/sequana/webapp_samplesheet)\n"
            "- [Report a bug](https://github.com/sequana/webapp_samplesheet/issues/new/choose)\n"
            "- [Sequana documentation](https://sequana.readthedocs.io)"
        )

    if choice == "Sample Sheet Validation (Illumina)":

        st.markdown(
            "This tool validates Illumina sample sheets. Both the **v1** format (bcl2fastq v2.20) and the "
            "**v2** format (BCL Convert) are supported; the version is detected automatically. "
            "It checks the structure, mandatory sections, sample identifiers, indexes, and more. "
            "Provide a sample sheet below for validation, or load one of the examples to try the tool. "
            "More examples are available in the **Examples** section of the menu."
        )
        st.subheader("Input Sample Sheet", divider="blue")

        # create a 3-column layout
        col1, col2, col3 = st.columns([4, 1, 4])
        with col1:
            data_file = st.file_uploader(
                "Drop a sample sheet below and press the **Process** button. ",
                type=["csv", "txt"],
                key=f"uploader_{st.session_state.uploader_key}",
            )
        with col2:
            # Centered "OR" text
            st.markdown("<div style='text-align: center;'><br><br>OR</div>", unsafe_allow_html=True)

        with col3:
            code = st.text_area(
                "Paste your sample sheet content here and press the **Process** button.", key="code_input"
            )

        st.subheader("Load an Example", divider="blue")
        st.caption(
            "Click a button to load a sample sheet into the text area above. "
            "Examples 1, 2 and 4 are valid sheets; Example 3 is invalid and demonstrates how errors are reported. "
            "Example 4 is a v2 (BCL Convert) sheet, the others are v1 (bcl2fastq)."
        )
        example_col1, example_col2, example_col3, example_col4 = st.columns(4)
        with example_col1:
            st.button("Example 1: Dual indexing (v1)", on_click=set_example, args=("sample_sheet.csv",))
        with example_col2:
            st.button("Example 2: Single index + Settings (v1)", on_click=set_example, args=("sample_sheet_settings_index.csv",))
        with example_col3:
            st.button("Example 3: Invalid (bad sample ID)", on_click=set_example, args=("Bad_SampleSheet_alphanum.csv",))
        with example_col4:
            st.button("Example 4: BCL Convert (v2)", on_click=set_example, args=("sample_sheet_v2_bclconvert.csv",))

        if st.button(":gear: Process :gear:"):

            try:
                samplesheet = data_file.read().decode()
                # st.experimental_rerun()
            except:
                samplesheet = code  # if there is no drag/drop data, we use the pasted code (if any)
                data_file = None

            try:
                process_sample_sheet(data_file, samplesheet)
            except Exception as err:
                import urllib.parse

                base_url = f"https://github.com/sequana/webapp_samplesheet/issues/new"

                samplesheet = "\n".join(["    " + x for x in samplesheet.split("\n")])
                params = {
                    "title": "Automatic error from the check-my-sample-sheet website",
                    "body": f"Dear developer(s),\n\nI encountered an unexpected error using the following sample sheet:\n\n{samplesheet}\n\nHere is the full error message:\n\n     {err}\n\nPlease let us know what you think might be the reason for the error.",
                }
                url = f"{base_url}?{urllib.parse.urlencode(params)}"
                st.markdown(
                    f'<div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;"> Sorry, an unknown error occurred. Please create an issue <a href="{url}">here</a> to report it. A page will open; you will need to click on the "Submit new issue" button. </div>',
                    unsafe_allow_html=True,
                )

                raise Exception(err)

    elif choice == "Examples":
        st.write("Below are several sample sheet examples, both valid and invalid, to illustrate the expected format.")
        st.subheader("1 - Minimalist Example (only [Data] section)")
        st.write(
            "In this example, the sample sheet is simplified to keep only the [Data] section and the mandatory columns "
            "(index and Sample_ID). Note that 'Sample_ID' is not strictly mandatory in bcl2fastq, but we make it "
            "mandatory in this application as a design choice for better traceability."
        )
        st.code(
            """[Data]
Sample_ID,index
ID1,TGACCA
ID2,CATTTT"""
        )

        st.subheader("2 - [Data] section with dual indexing and no [Settings] section")
        url = "https://raw.githubusercontent.com/sequana/webapp_samplesheet/main/examples/sample_sheet.csv"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode()
        st.write(
            "A more common example is shown below. The Illumina sample sheet uses sections enclosed in square brackets. "
            "Up to four sections may appear: [Header], [Reads], [Settings] and [Data]. This example shows the [Header], "
            "[Reads] and [Data] sections (the [Settings] section is missing). According to the Illumina specification, "
            "all sections are optional, including [Data]. However, when [Data] is missing, all reads are stored as "
            "undetermined, which is rarely useful. For this reason, we require the [Data] section in this application."
        )
        st.code(data, language="bash")

        st.subheader("3 - [Data] section with single index and a [Settings] section")
        url = (
            "https://raw.githubusercontent.com/sequana/webapp_samplesheet/main/examples/sample_sheet_settings_index.csv"
        )
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode()
        st.code(data, language="bash")

        st.subheader("4 - Example of an erroneous sample sheet (invalid sample ID name)")
        url = "https://raw.githubusercontent.com/sequana/webapp_samplesheet/main/examples/Bad_SampleSheet_alphanum.csv"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode()
        st.code(data, language="bash")

        st.subheader("5 - Example of an erroneous sample sheet (extra trailing semicolons)")
        url = "https://raw.githubusercontent.com/sequana/webapp_samplesheet/main/examples/Bad_SampleSheet_extra_semicolons.csv"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode()
        st.code(data, language="bash")

    elif choice == "About":
        st.subheader("About")
        st.markdown(
            "This application is part of the [Sequana Project](https://github.com/sequana), which is dedicated to NGS analysis. "
            "Please see the [online documentation](https://sequana.readthedocs.io) as well as https://sequana.github.io for more information. "
            "The code used in this application is based on the [IEM module](https://github.com/sequana/sequana) of the Sequana Python library. "
            "It was developed based on the bcl2fastq documentation (v2.20) and is intended for users who want to demultiplex their data properly. "
            "The source code for this web application is available on [GitHub](https://github.com/sequana/webapp_samplesheet)."
            "\n\nThe different checks performed are described in this preprint: [Research Square](https://www.researchsquare.com/article/rs-5268893/v1)."
        )
        st.info(
            "Application Author: Thomas Cokelaer\n\nIEM module provided by The Sequana Team\n\nOriginal beta testing: Laure Lemée, Etienne Kornobis, Rania Ouazahrou"
        )
    else:
        st.subheader("How to cite?")
        st.info("Check My Sample Sheet application (this website):\n\nLemée L. et al, [Research Square](https://www.researchsquare.com/article/rs-5268893/v1)")

        st.info(
            "The Sequana framework used to check the sample sheet:\n\nCokelaer T. et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI [doi:10.21105/joss.00352](https://joss.theoj.org/papers/10.21105/joss.00352)"
        )


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
            version = get_sample_sheet_version(fout.name)
            iem = SampleSheetFactory(fout.name)

        if version == "v2":
            st.info(":information_source: Detected an Illumina **v2** sample sheet: validating against the **BCL Convert** specification.")
        else:
            st.info(":information_source: Detected an Illumina **v1** sample sheet: validating against the **bcl2fastq v2.20** specification.")

        try:
            # st.write(f"This sample sheet contains {len(iem.df)} samples")
            iem.validate()
        except SystemExit as err:
            st.header("Validation Results", divider="blue")
            msg = "Error(s) found. :sob: See the message below from Sequana for details."
            st.error(msg)
            st.info(err)
        else:
            st.header("Validation Results", divider="blue")
            # emoji within div do not seem to work
            msg = ":champagne: Your sample sheet looks correct. :champagne:"
            st.success(msg)
        # =============================================================== validation
        st.subheader("Details about the checks", divider="blue")
        checks = iem.checker()

        msgs = print_checks(checks)

        # =============================================================== original file
        st.subheader("Original file", divider="blue")
        st.code(samplesheet)

        # =============================================================== corrected file
        if len(msgs["Error"]):
            st.subheader("Corrected file", divider="blue")
            st.caption(
                "The quick fix below removes extra trailing semicolons. Other types of errors are difficult to correct "
                "automatically, so you will need to fix the file manually. We strongly recommend using the IEM software "
                "from Illumina for that purpose. If you need to edit the file quickly, do not use Excel: although the "
                "extension is usually .csv, an Illumina sample sheet is not a standard CSV file and Excel may corrupt it."
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
            "For convenience, the [Data] section is shown below as a parsed table. "
            "Check that the values are consistent with your expectations (for example, that each index appears in a single column)."
        )
        df = iem.df.copy()
        st.write(df)


if __name__ == "__main__":
    main()
