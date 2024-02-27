# Check My Sample Sheet

This is a streamlit application that uses Sequana (github.com/sequana/sequana) modules to check Sample Sheet from Illumina sequencers.

Running demo is here: https://check-my-sample-sheet.streamlit.app/

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fcheck-my-sample-sheet.streamlit.app%2F&countColor=%23263759)


# General Information

Note that there is a V2 version of the Illumina Sample Sheet to be used with BCL convert. In this application we focus on the V1 (to be used with bcl2fastq). 
Some differences are :

- section **[Data]** is **[BCLConvert_Data]**  [doc](https://support-docs.illumina.com/APP/AppBCLConvert_v1_3/Content/APP/DataSection_swBCL_swBS_appBCL.htm)

According to the bcl2fastq documentation, for project and sample names, the space is not allowed. These characters are not allowed  either: ? ( ) [ ] / \ = + < > : ; " ' , * ^ | & .

v4.0 of bclconvert: https://support-docs.illumina.com/SW/BCL_Convert_v4.0/Content/SW/BCLConvert/BCLConvert.htm
