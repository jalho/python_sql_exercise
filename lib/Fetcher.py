import yfinance, sqlite3, datetime
from pathlib import Path

def initSql():
  connection = sqlite3.connect("data.db")
  cursor = connection.cursor()
  with connection:
    cursor.execute("""
      CREATE TABLE firms (
        symbol text,
        shortName text,
        bookValue integer,
        bookValueDate text,
        fullTimeEmployees integer
      )
    """)

class Fetcher:
  """Fetch data from Yahoo! Finance and store it in SQLite database."""
  def __init__(self):
    self.data = None
  
  def fetch(self, label):
    """Fetch data from Yahoo! Finance without storing."""
    try:
      self.data = yfinance.Ticker(label).info
      print("Data fetched.")
    except:
      self.data = None
      raise Exception(
        "No data fetched. Check the label argument '{}'.".format(label)
        ) from None

  def store(self):
    """Store previously fetched data."""
    if not self.data:
      raise Exception("No data has been fetched to be stored!")
    # store data in the specified format ("sql" mode by default)
    else:
      if not Path("data.db").is_file():
        initSql()
      connection = sqlite3.connect("data.db")
      cursor = connection.cursor()
      # check duplicate
      cursor.execute("SELECT * FROM firms WHERE shortName=:shortName", {"shortName": self.data["shortName"]})
      if len(cursor.fetchall()):
        print("Record with the same shortName is already stored. Not storing again.")
        return
      with connection:
        cursor.execute(
            "INSERT INTO firms VALUES (:symbol, :shortName, :bookValue, :bookValueDate, :fullTimeEmployees)",
            {
              "symbol": self.data["symbol"],
              "shortName": self.data["shortName"],
              "bookValue": self.data["bookValue"],
              "bookValueDate": datetime.datetime.now().strftime("%c"),
              "fullTimeEmployees": self.data["fullTimeEmployees"]
            }
          )
        print("Data stored.")

  def viewStored(self, shortName=None):
    """View firms stored in data.db. Defaults to view all."""
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    if not shortName:
      print("All records:")
      cursor.execute("SELECT * FROM firms")
      print(cursor.fetchall())
    else:
      print("Stored records:")
      cursor.execute("SELECT * FROM firms WHERE shortName=:shortName", {"shortName": shortName})
      print(cursor.fetchall())
  
  def isStored(self, label):
    if not Path("data.db").is_file():
      return False
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM firms WHERE symbol=:symbol", {"symbol": label})
    results = cursor.fetchall()
    if results:
      print("'{}' is already stored, not fetching again.".format(label))
    return results