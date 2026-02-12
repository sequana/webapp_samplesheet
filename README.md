# Check My Sample Sheet

This is a streamlit application that uses Sequana (github.com/sequana/sequana) **iem** modules to check Sample Sheet from Illumina sequencers.

Running demo is here: https://check-my-sample-sheet.streamlit.app/

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fcheck-my-sample-sheet.streamlit.app%2F&countColor=%23263759)


# General Information

If you want to contribute to this web application, please provide PR here. Note, however, that the core of the application is within the Sequana project on https://github.com/sequana/sequana/, more specifically in the iem.py module.

The sanity checks implemented are based on experience and the bcl2fastq documentation v2.20

# Local instance

## Using local python

If you'd like to run a local instance, you could either install streamlit and run it directly (python virtual environment is highly recommended):

```bash
git clone https://github.com/sequana/webapp_samplesheet check_my_sample_sheet
cd check_my_sample_sheet/app
pip install -r requirements.txt
python -m streamlit run app.py
```

## Using singularity

Or if you'd like to run an instance on a web server, there is a singularity definition file (requires singularity and docker to build, only singularity to run):

```bash
git clone https://github.com/sequana/webapp_samplesheet check_my_sample_sheet
singularity build --build-arg SERVER_ADDRESS=127.0.0.1 --fakeroot sample_sheet_validator_1.0.0.sif samplesheet_validator.def
```

You can change the IP address you're listening to to suit your needs, and then run an instance of the app:

```bash
singularity instance start sample_sheet_validator_1.0.0.sif samplesheet_validatord
```

Please note: if using singularity, make sure that both `/tmp` and `$HOME` are writable. You can either set `mount tmp = yes` and `mount home = yes` in `/etc/singularity/singularity.conf`, or you can set the binds manually.

By default, the app will be served on port 8501, so if you'd like to redirect http traffic through a reverse proxy, you can specify the IP address and port 8501 as the target.
