from lib.Fetcher import Fetcher as F

fetcher = F()
label = input("Enter a label, e.g. 'NDA-FI.HE': ") or "NDA-FI.HE"
if not fetcher.isStored(label):
    fetcher.fetch(label)
    fetcher.store()

fetcher.viewStored(input("View stored records by shortName, e.g. 'Nordea Bank Abp': "))