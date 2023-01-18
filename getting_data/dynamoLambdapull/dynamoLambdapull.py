import json
import pandas as pd
import boto3
from decimal import Decimal

def pullData():
    chunk = pd.read_csv(
        'https://www.cryptodatadownload.com/cdd/gemini_BTCUSD_2021_1min.csv',
        chunksize=100000, header=1)
    pd_df = pd.concat(chunk)
    return pd_df
    
def dynamoDump():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('btc')
    with table.batch_writer() as batch:
        for index, row in pullData().iterrows():
            batch.put_item(json.loads(row.to_json(), parse_float=Decimal))

def lambda_handler(event, context):
    dynamoDump()

lambda_handler()