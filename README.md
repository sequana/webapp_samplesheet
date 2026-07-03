# Check My Sample Sheet

[![Tests](https://github.com/sequana/webapp_samplesheet/actions/workflows/tests.yml/badge.svg)](https://github.com/sequana/webapp_samplesheet/actions/workflows/tests.yml)
[![Release](https://img.shields.io/github/v/release/sequana/webapp_samplesheet)](https://github.com/sequana/webapp_samplesheet/releases)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit&logoColor=white)](https://check-my-sample-sheet.streamlit.app/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Last commit](https://img.shields.io/github/last-commit/sequana/webapp_samplesheet)](https://github.com/sequana/webapp_samplesheet/commits/main)
[![Issues](https://img.shields.io/github/issues/sequana/webapp_samplesheet)](https://github.com/sequana/webapp_samplesheet/issues)
[![Stars](https://img.shields.io/github/stars/sequana/webapp_samplesheet?style=flat)](https://github.com/sequana/webapp_samplesheet/stargazers)
![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fcheck-my-sample-sheet.streamlit.app%2F&countColor=%23263759)

This is a streamlit application that uses Sequana (github.com/sequana/sequana) **iem** modules to check Sample Sheets from Illumina sequencers. Both formats are supported and detected automatically:

- **v1** (bcl2fastq): `[Data]` / `[Settings]` sections
- **v2** (BCL Convert): `[BCLConvert_Data]` / `[BCLConvert_Settings]` sections

Running demo is here: https://check-my-sample-sheet.streamlit.app/


# General Information

If you want to contribute to this web application, please provide PR here. Note, however, that the core of the application is within the Sequana project on https://github.com/sequana/sequana/, more specifically in the iem.py module.

The sanity checks implemented are based on experience, the bcl2fastq documentation (v2.20) and the BCL Convert specification.

# Installation

From PyPI:

    pip install check-my-sample-sheet

Then launch the app (opens in your browser); extra arguments are forwarded to
`streamlit run` (e.g. `--server.port 8502`):

    check-my-sample-sheet

# Local instance (from source)

    git clone https://github.com/sequana/webapp_samplesheet
    cd webapp_samplesheet

    # install the dependencies (sequana, streamlit, ...)
    pip install -r requirements.txt

    # run the application locally in your browser
    streamlit run check_my_sample_sheet/app.py

# Running the tests

    pip install -r requirements-dev.txt
    pytest


