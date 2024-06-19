from web3 import Web3
import mysql.connector
from mysql.connector import Error
import json
import time

# Connect to the blockchain using Infura
infura_url = "https://polygon-mainnet.infura.io/v3/8d82201ca34e42aa8ab2cac9201a0f89"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',
    database='blockchain',
    user='user',
    password='password'
)

def store_event(event):
    cursor = connection.cursor()
    add_event = ("INSERT INTO user_operations "
                 "(userOpHash, sender, paymaster, nonce, success, actualGasCost, actualGasUsed) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data_event = (event['userOpHash'], event['sender'], event['paymaster'], event['nonce'], event['success'], event['actualGasCost'], event['actualGasUsed'])
    cursor.execute(add_event, data_event)
    connection.commit()
    cursor.close()

# Read the ABI from the file
with open('abi.json', 'r') as abi_file:
    abi = json.load(abi_file)

# Convert the contract address to checksum format
contract_address = "0x5ff137d4b0fdcd49dca30c7cf57e578a026d2789"
checksum_address = web3.to_checksum_address(contract_address)

# Define the contract and event
contract = web3.eth.contract(address=checksum_address, abi=abi)
event_signature_hash = web3.keccak(text="UserOperationEvent(bytes32,address,address,uint256,bool,uint256,uint256)").hex()

# Fetch logs using eth_getLogs
def fetch_logs():
    latest_block = web3.eth.block_number
    logs = web3.eth.get_logs({
        'fromBlock': latest_block - 1000,  # Adjust the range as needed
        'toBlock': 'latest',
        'address': checksum_address,
        'topics': [event_signature_hash]
    })
    for log in logs:
        try:
            userOpHash = log['topics'][1].hex()
            sender = web3.to_checksum_address(log['topics'][2].hex()[-40:])
            paymaster = web3.to_checksum_address(log['topics'][3].hex()[-40:])

            data = log['data']  # Keep as bytes

            # Detailed debugging information
            print(f"Raw log data: {log}")
            print(f"Processed data (hex): {data.hex()}")
            print(f"Sender: {sender}, Paymaster: {paymaster}")

            nonce = int.from_bytes(data[0:32], byteorder='big')
            success = bool(int.from_bytes(data[32:64], byteorder='big'))
            actualGasCost = int.from_bytes(data[64:96], byteorder='big')
            actualGasUsed = int.from_bytes(data[96:128], byteorder='big')

            event_data = {
                'userOpHash': userOpHash,
                'sender': sender,
                'paymaster': paymaster,
                'nonce': nonce,
                'success': success,
                'actualGasCost': actualGasCost,
                'actualGasUsed': actualGasUsed
            }
            store_event(event_data)
        except ValueError as ve:
            print(f"ValueError: {ve}")
            print(f"Data causing error: {data}")
        except Exception as e:
            print(f"Error processing log: {e}")
            print(f"Log data: {log}")

while True:
    fetch_logs()
    time.sleep(100)  # Sleep for a while before fetching new logs

