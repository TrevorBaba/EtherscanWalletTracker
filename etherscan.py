import os
import requests
import datetime

# Insert your Telegram bot token and Etherscan API key here
TELEGRAM_TOKEN = '6342306829:AAFZqztXdu3wPbpVuiR6xG58Ci2KtJWIfFc'
ETHERSCAN_API_KEY = 'IDQD5ANRJT6JYIQCHZSD842YP4EDWEUJ8U'


# Define a function to get the latest transaction for a given Ethereum wallet address

# https://api.etherscan.io/api
#    ?module=account
#    &action=tokentx
#    &address=0x12b6e121Cf45E03f100C296A4Ee2E12C2D53df72&startblock=17737312
#    &sort=desc
#    &apikey=IDQD5ANRJT6JYIQCHZSD842YP4EDWEUJ8U

def get_latest_transaction(wallet_address):
    url = f"""https://api.etherscan.io/api?module=account&action=tokentx&address={wallet_address}&startblock=17737000&sort=desc&apikey={ETHERSCAN_API_KEY}"""

    response = requests.get(url)
    data = response.json()
    if data['status'] == '0':
        return 'Error: ' + data['message']
    elif len(data['result']) == 0:
        return 'No transactions found for this address'
    else:
        latest_tx = data['result'][0]
        timestamp = int(latest_tx['timeStamp'])
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        date_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        eth = int(latest_tx['value']) / 10**18
        return f"""
        Latest transaction\n
        Token Name: {latest_tx['tokenName']} ({latest_tx['tokenSymbol']})\n
        Amount in {latest_tx['tokenName']}: {eth}\n
        Time: {date_string}"""


result = get_latest_transaction('0x12b6e121Cf45E03f100C296A4Ee2E12C2D53df72')
print(result)
