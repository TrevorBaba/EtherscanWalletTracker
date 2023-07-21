import datetime
import pytz
import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Insert your Telegram bot token and Etherscan API key here
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')

wallet_hash = {}


# Define a function to get the latest transaction for a given Ethereum wallet address


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
        return latest_tx


def poll_wallet(context):
    for wallet_address in wallet_hash.keys():
        tx = get_latest_transaction(wallet_address)
        if tx['hash'] != wallet_hash[wallet_address]:
            wallet_hash[wallet_address] = tx['hash']
            message = format_message(tx, wallet_address)
            context.bot.send_message(chat_id=context.job.context, text=message)
        # else:
        #     context.bot.send_message(chat_id=context.job.context, text="hello world")
    


# Define a function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! I'm a bot that can track Ethereum wallets and their transactions on Etherscan. To get started, send me a wallet address.")
    context.job_queue.run_repeating(
        poll_wallet, interval=5, first=1, context=update.effective_chat.id)
    

# Define a function to handle text messages
def echo(update, context):
    wallet_address = update.message.text
    latest_tx = get_latest_transaction(wallet_address)
    if wallet_address not in wallet_hash:
        wallet_hash[wallet_address] = latest_tx['hash']
    message = format_message(latest_tx, wallet_address)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def format_message(latest_tx, wallet_address):
    timestamp = int(latest_tx['timeStamp'])
    utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
    pst_timezone = pytz.timezone('America/Los_Angeles')
    # Convert the datetime to PST
    pst_datetime = utc_datetime.astimezone(pst_timezone)
    date_string = pst_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Check if it is a buy or sell
    recipient = latest_tx['to']
    if wallet_address.lower() == recipient.lower():
        type = "BUY"
    else:
        type = "SELL"
    message = f"""
Latest transaction by {wallet_address}
{type}
Token Name: {latest_tx['tokenName']} ({latest_tx['tokenSymbol']})
Amount in {latest_tx['tokenName']}: {latest_tx['value']}
Time: {date_string}
Contract Address: {latest_tx['contractAddress']}"""
    return message

# Create a Telegram bot and add handlers
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, echo))

# Start the bot
updater.start_polling()
updater.idle()
