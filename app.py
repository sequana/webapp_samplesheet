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
"""Root entry point kept for Streamlit Community Cloud.

The application lives in :mod:`check_my_sample_sheet.app`. Streamlit Cloud is
configured to run ``app.py`` from the repository root, so this thin shim just
imports and runs the packaged app. Prefer ``streamlit run
check_my_sample_sheet/app.py`` or the ``check-my-sample-sheet`` console script.
"""

from check_my_sample_sheet.app import main

main()
