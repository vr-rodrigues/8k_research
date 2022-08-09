import pandas as pd
from sec_edgar_downloader import Downloader

# Initialize a downloader instance. If no argument is passed
# to the constructor, the package will download filings to
# the current working directory.
dl = Downloader("baixados")


df = pd.read_excel('doc.xlsx')
list_8k = df['lista_8k'].tolist()

for filling in list_8k:
    print(filling)
    try:
        dl.get("8-K", filling, after="2010-01-01")
    except:
        pass
