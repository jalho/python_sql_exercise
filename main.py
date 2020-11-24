"""Financial ratios fetcher

Fetch financial information or use local copy of previously fetched data.
"""

import json, pickle, yfinance
from pathlib import Path

def fetchNDA(pickleBinary=False):
    """Fetch NDA data from Yahoo! Finance and store it as JSON or pickled object binary
    unless local copy of the data already exists."""

    if Path("nda.json").is_file() or Path("nda").is_file():
        print("Data already exists. Not fetching again.")
        return

    print("Fetching data.")
    data = yfinance.Ticker("NDA-FI.HE").info

    if pickleBinary:
        with open("nda", "wb") as f:
            pickle.dump(data, f)
    else:
        with open("nda.json", "w") as f:
            f.write(json.dumps(data, indent=4, sort_keys=True))

fetchNDA()
# Do something with the fetched data...