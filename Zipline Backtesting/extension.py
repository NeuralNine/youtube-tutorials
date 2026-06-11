# ~/.zipline/extension.py

# First download with script 7
# Then extension
# Then: zipline ingest -b yfinance-csvdir-bundle

import pandas as pd

from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

start_session = pd.Timestamp('2014-01-02')
end_session = pd.Timestamp('2025-12-31')

register(
    'yfinance-csvdir-bundle',
    csvdir_equities(
        ['daily'],
        '/home/neuralnine/Documents/Programming/NeuralNine/youtube-preparation/ZiplineTutorial/scratch/zipline_csvs',
    ),
    calendar_name='NYSE',
    start_session=start_session,
    end_session=end_session
)

