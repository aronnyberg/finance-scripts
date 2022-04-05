import pandas as pd
import boto3
import json
from decimal import Decimal

chunk = pd.read_csv(
    'https://www.cryptodatadownload.com/cdd/gemini_BTCUSD_2021_1min.csv',
    chunksize=100000, header=1)
pd_df = pd.concat(chunk)

print(pd_df.head())

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('btc')

with table.batch_writer() as batch:
    for index, row in pd_df.head().iterrows():
        batch.put_item(json.loads(row.to_json(), parse_float=Decimal))