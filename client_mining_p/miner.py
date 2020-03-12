import hashlib
import requests

import sys
import json
from time import time


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    proof = 0
    json_block = json.dumps(block,sort_keys=True)
    while valid_proof(json_block,proof) is False:
        proof +=1
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    block_string_proof = f'{block_string}{proof}'.encode()
    hash_block = hashlib.sha256(block_string_proof).hexdigest()
    #print("hasbloc",hash_block)
    if hash_block[:6]=="000000":
        #print(block_string)
        return True
    else:
        return False


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    start_time = time()
    # Run forever until interrupted
    coins = 0
   
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
            
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        # new_proof = ???
        new_proof = proof_of_work(data["last_block"])
        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        try:
            data = r.json()
            print(data)
            # TODO: If the server responds with a 'message' 'New Block Forged'
            # add 1 to the number of coins mined and print it.  Otherwise,
            # print the message from the server.
            # print(r["message"])
            if data['message']=="New Block Forged":
                find_time = time()
                coins +=1
                print("Time from last block",find_time-start_time)
                start_time = find_time
                print("Coins mined:",coins)
                print("")
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            
            
        