# Check My Sample Sheet

This is a streamlit application that uses Sequana (github.com/sequana/sequana) modules to check Sample Sheet from Illumina sequencers.

Running demo is here: https://check-my-sample-sheet.streamlit.app/

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fcheck-my-sample-sheet.streamlit.app%2F&countColor=%23263759)


# General Information

If you want to contribute, the core of the application is within the Sequana project on github.com/sequana/sequana/ ,
more specifically in the iem.py module.

The sanity checks implemented are based on experience and the bcl2fastq documentation. 

Note that in project and sample names, spaces are not allowed. These characters are not allowed  either: ? ( ) [ ] / \ = + < > : ; " ' , * ^ | & .

Note also that there is a V2 version of the Illumina Sample Sheet to be used with BCL convert utility. In this application we focus on the V1 (to be used with bcl2fastq).


More information here [doc](https://support-docs.illumina.com/APP/AppBCLConvert_v1_3/Content/APP/DataSection_swBCL_swBS_appBCL.htm)
and for v4.0 of bclconvert: https://support-docs.illumina.com/SW/BCL_Convert_v4.0/Content/SW/BCLConvert/BCLConvert.htm


# Local instance

    git clone https://github.com/sequana/webapp_samplesheet check_my_sample_sheet
    cd check_my_sample_sheet
    streamlit run app.py


