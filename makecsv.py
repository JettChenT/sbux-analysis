# A simple script that makes a CSV of starbucks financial data

#%%
import requests, dotenv, os
import pandas as pd
dotenv.load_dotenv()
KEY = os.getenv("FMP_KEY")
print(f"The API key is: {KEY}")

#%%
CODE = "SBUX"
r = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{CODE}", params={
    'apikey':KEY,
})
df = pd.DataFrame(data=r.json())
df.to_csv('./sbux.csv')