import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse


class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(nonce = 0, previous_hash = '0')
        self.miners = set()
    
    def create_block(self, nonce, previous_hash):
        """
        A function that creates a new block in the blockchain
        """
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'difficulty target': '0000', #static difficulty target
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}

        if previous_hash == '0': # only for genesis block
            self.transactions = []
            self.chain.append(block)
        return block

    def get_last_block(self):
        """
        A function that returns the previous block for use of creating a new block (previous block's hash)
        """
        return self.chain[-1]

    def proof_of_work(self, previous_hash):
        """
        This is the proof of work algorithm with static dificulty level
        """
        nonce = 0
        valid = False
        
        while valid is False:
            block_candidate = self.create_block(nonce, previous_hash)
            hash_operation = hashlib.sha256(json.dumps(block_candidate, sort_keys =True).encode()).hexdigest()
            if hash_operation[:4] == block_candidate['difficulty target']:
                self.transactions = [] # clear the transaction after finding the nonce
                self.chain.append(block_candidate) # add the block to the chain
                valid = True
            else:
                nonce += 1
        return True
    
    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys =True).encode()).hexdigest()
    
    def is_chain_valid(self, chain):
        """
        A function that validates the blockchain from the beginning
        """
        previous_block = chain[0] # start with genesis block
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount, comment = ""):
        """
        A function that adds a transaction to the list of transactions
        """
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'comment': comment, 
                                  'amount': amount})
        previous_block = self.get_last_block()
        return previous_block['index'] + 1
    
    def add_miner(self, address):
        """
        A function that adds a node to the list of nodes. The nodes are the miners that will mine the blocks
        """
        parsed_url = urlparse(address)
        self.miners.add(parsed_url.netloc)

    def save_transactions(self, chain_to_delete, longest_chain):
        """
        A function that saves the transactions from the overwritten chain to the transaction's memory
        """
        index = 0
        if chain_to_delete == None:
            return True
        while index < len(chain_to_delete):
            transactions_to_delete = chain_to_delete[index]['transactions']
            transactions = longest_chain[index]['transactions']

            if not (transactions_to_delete == transactions):
                [self.transactions.append(i) for i in transactions_to_delete if i not in transactions]
            
            index += 1

        return True
    
    def force_consensus(self):
        """
        A function that replaces the local chain of each miner with the longest chain. 
        """
        network = self.miners
        longest_chain = requests.get(f"http://localhost:{port}/get_chain").json()['blockchain']
        max_length = len(self.chain)
        for m in network:
            response = requests.get(f"http://{m}/get_chain")
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['blockchain']
                if length > max_length and self.is_chain_valid(chain):
                    self.save_transactions(longest_chain, chain)
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False



app = Flask(__name__) 
blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_last_block()
    prev_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(prev_hash)
    if not proof:
        return 'No valid Nonce found! Please, restart the mining process', 400
    ind = previous_block['index'] + 1
    blockchain.add_transaction(sender = 'The Network', receiver = str(port), amount = 1, comment = 'Mining Reward for mining block {}'. format(ind)) #created from thin air, this is the miner fee. This will show up in the next block
    block = blockchain.get_last_block()
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'nonce': block['nonce'],
                'difficulty_target': block['difficulty target'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'blockchain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount', 'comment', 'comment']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    _ = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'], json['comment'])
    response = {'message': f'Transaction awaits confirmation. If valid, will be added to the blockchain.'}
    return jsonify(response), 201


@app.route('/connect_miner', methods = ['POST'])
def connect_miner():
    json = request.get_json()
    miners = json.get('miners')
    if miners is None:
        return "No miners", 400
    for miner in miners:
        blockchain.add_miner(miner)
    response = {'message': 'All the miners are now connected. The Cryptocurrency Blockchain now contains the following miners:',
                'total_miners': list(blockchain.miners)}
    return jsonify(response), 201

@app.route('/force_consensus', methods = ['GET'])
def force_consensus():
    is_chain_replaced = blockchain.force_consensus()
    if is_chain_replaced:
        response = {'message': 'The miners had different chains so the chain was replaced by the longest one.',
                    'in_force_chain': blockchain.chain,
                    'transactions pending': blockchain.transactions}
    else:
        response = {'message': 'All good. The current chain is the largest one.',
                    'in_force_chain': blockchain.chain}
    return jsonify(response), 200


port = 5003
app.run(host = '0.0.0.0', port = port)