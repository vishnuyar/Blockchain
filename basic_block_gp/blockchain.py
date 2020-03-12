import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block# TODO

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index':len(self.chain),
            'timestamp':time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_Block_Hash':previous_hash or self.hash(self.last_block)
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        block_string = json.dumps(block,sort_keys=True).encode()

        # TODO: Hash this string using sha256
        sha_block = hashlib.sha256(block_string)
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return sha_block.hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     proof = 0
    #     json_block = json.dumps(block,sort_keys=True)
    #     while self.valid_proof(json_block,proof) is False:
    #         proof +=1
    #     print(proof)
    #     return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
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
        #print(block_string)
        if hash_block[:6]=="000000":
            #print(hash_block)
            return True
        else:
            return False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    recd_data = request.get_json()
    block_id = recd_data['id']
    block_proof = recd_data['proof']

      
    #check block_id and block_proof should be present
    if (block_id is not None) & (block_proof is not None):
        #create a new block with this proof
        previous_hash = blockchain.hash(blockchain.last_block)
        prev_block = blockchain.last_block
        string_block = json.dumps(prev_block,sort_keys=True)
        if blockchain.valid_proof(string_block,block_proof):
            blockchain.new_block(block_proof,previous_hash)
            response = {
                "message":"New Block Forged"
            }            
        else:
            response = {"message":"Proof failed"}
    else:
        response = {
            "message":"Both Id and Proof should be present"
            }
    return jsonify(response),200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def send_last_block():
    response = {
        'last_block':blockchain.chain[-1],
        
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
