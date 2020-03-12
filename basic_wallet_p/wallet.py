import requests
import sys

def get_balance(blocks,userid):
    #Get the balance for the userid after traversing the block chain
    recd = 0
    sent = 0
    user_transactions = []
    for block in blocks:
        transactions = block['transactions']
        for transaction in transactions:
            if transaction['sender'] == userid:
                sent += float(transaction['amount'])
                user_transactions.append(transaction)
            if transaction['recipient'] == userid:
                recd += float(transaction['amount'])
                user_transactions.append(transaction)


    return (recd,sent,user_transactions)



if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    user_id = None
    if len(sys.argv) == 2:
        node = sys.argv[1]
    elif len(sys.argv) > 2:
        node = sys.argv[1]
        user_id = sys.argv[2]
        
    else:
        node = "http://localhost:5000"

    if user_id is None:
        # Load ID
        f = open("my_id.txt", "r")
        user_id = f.read()
        print("ID is", id)
        f.close()
    #Get the blockchain from the server
    r = requests.get(url=node + "/chain")
    # Handle non-json response
    try:
        data = r.json()
        blocks = data['chain']
        print(f'Number of blocks mined is {len(blocks)}')
        recd,sent,transactions = get_balance(blocks,user_id)
        print(f'The balance for the user {user_id} is {recd - sent}')
        print(f'Total Recieved:{recd}')
        print(f'Total Sent:{sent}')
        for transaction in transactions:
            print(transaction)
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
    