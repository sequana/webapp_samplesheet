# Check My Sample Sheet

This is a streamlit application that uses Sequana (github.com/sequana/sequana) **iem** modules to check Sample Sheet from Illumina sequencers.

Running demo is here: https://check-my-sample-sheet.streamlit.app/

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fcheck-my-sample-sheet.streamlit.app%2F&countColor=%23263759)


# General Information

If you want to contribute to this web application, please provide PR here. Note, however, that the core of the application is within the Sequana project on https://github.com/sequana/sequana/, more specifically in the iem.py module.

The sanity checks implemented are based on experience and the bcl2fastq documentation v2.20

# Local instance

    git clone https://github.com/sequana/webapp_samplesheet check_my_sample_sheet
    cd check_my_sample_sheet

    # You will need to install requirements (sequana and streamlit)
    pip install --file requirements.txt

    # and should ne ready to test the appliction locally in your browser 
    streamlit run app.py


