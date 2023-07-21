import os
import requests
import datetime

# Insert your Telegram bot token and Etherscan API key here
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')


# Define a function to get the latest transaction for a given Ethereum wallet address

# https://api.etherscan.io/api
#    ?module=account
#    &action=tokentx
#    &address=0x88AAd0cB142c15cC46A342a9950F4089cfC07f81&startblock=17737312
#    &sort=desc
#    &apikey=A34XM7W2TWG41J92HHMNTVSNIBAU3K7QJY

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


result = get_latest_transaction('0x1fB8DD0Ab9608Bd5f9E709B6B85c0EEc96997066')
print(result)
