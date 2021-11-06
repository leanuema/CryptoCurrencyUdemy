import datetime
import hashlib
import json
import pprint

import Flask as Flask
import requests
from urllib.parse import urlparse
from uuid import uuid4

from flask import jsonify

from Block import Block
from Transaction import Transaction


class Blockchain:

    def __init__(self):
        self.chain = [self.genesisBlock()]
        self.difficulty = 5
        self.pendingTransaction = []
        self.reward = 10
        self.nodes = set()
        self.create_block(proof=1, previous_hash='0')
        self.transactions = []

    def genesisBlock(self):
        gblock = Block(str(datetime.datetime.now()), "block 0 from blockchain")
        return gblock

    # funcion que genera el bloque 0 con la fecha actual
    def getLastBlock(self):
        return self.chain[-1]

    # se obtiene el ultimo bloque de la cadena
    def minePendingTransaction(self, minerRewardAddress):
        newBlock = Block(str(datetime.datetime.now()), self.pendingTransaction)
        newBlock.mineBlock(self.difficulty)
        newBlock.previousBlock = self.getLastBlock().hash

        print(f"Previous block hash {newBlock.previousBlock}")
        testChain = []
        for trans in newBlock.transaction:
            temp = json.dumps(trans.__dict__, indent=5, separators=(',', ':'))
            testChain.append(temp)
        pprint.pprint(testChain)
        self.chain.append(newBlock)
        print(f"Hash from actual block {newBlock.hash}")

        rewardTrans = Transaction("System", minerRewardAddress, self.reward)
        self.pendingTransaction.append(rewardTrans)
        self.pendingTransaction = []

    # se recorre la lista de transacciones y se buscan los bloques a minar
    def isValidChainToMine(self):
        for x in range(1, len(self.chain)):
            currentBlock = self.chain[x]
            previousBlock = self.chain[x - 1]

            if (currentBlock.previousBlock != previousBlock.hash):
                print("Invalid chain")

        print("Valid chain and secure")

    def add_transaction(self, sender, receiber, amount):
        self.transactions.append({'sender': sender,
                                  'receiber': receiber,
                                  'amount': amount
                                  })
        previous_block = self.print_previous_block()
        return previous_block['index'] + 1

    # funcion que crea una nueva transaccion y la almacena en la lista
    def getBalance(self, walletAddress):
        balance = 0
        for block in self.chain:
            if block.previousBlock == "":
                continue
            for transaction in block.transaction:
                if transaction.fromWallet == walletAddress:
                    balance -= transaction.amount
                if transaction.toWallet == walletAddress:
                    balance += transaction.amount
        return balance

    # Funcion para aniadir bloques a la cadena
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'time-stamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous-hash': previous_hash,
            'transaction': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

        # Devuelve el ultimo bloque de la cadena

    def print_previous_block(self):
        return self.chain[-1]

    # Funcion de prueba de trabajo
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()

    def chain_validator(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous-hash'] != self.hash(previous_block):
                return False
            previous_block = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_block ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_node(self, address):
        parser_url = urlparse(address)
        self.nodes.add(parser_url.netloc)

    # funcion que reemplaza cadena por la mas larga
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get('https://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['lenght']
                chain = response.json()['chain']
                if length > max_length and self.chain_validator(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# my_crypto = Blockchain()
#
# print("Leandro, begun to mine")
#
# my_crypto.add_transaction(Transaction("Macia", "JB", 0.01))
# my_crypto.add_transaction(Transaction("Leandro", "Seba", 0.1))
# my_crypto.add_transaction(Transaction("Luis", "Migue", 1))
#
# init_time = datetime.time()
# my_crypto.minePendingTransaction("Leandro")
# to_time = datetime.time()
# print(f"Time spent {init_time - to_time} secs")
#
# print("Gaby, begun to mine")
#
# my_crypto.add_transaction(Transaction("Macia", "JB", 0.01))
# my_crypto.add_transaction(Transaction("Leandro", "Seba", 0.1))
# my_crypto.add_transaction(Transaction("Luis", "Migue", 1))
#
# init_time = datetime.time()
# my_crypto.minePendingTransaction("Gaby")
# to_time = datetime.time()
# print(f"Time spent {init_time - to_time} secs")
#
# print("Maca, begun to mine")
#
# my_crypto.add_transaction(Transaction("Macia", "JB", 0.01))
# my_crypto.add_transaction(Transaction("Leandro", "Seba", 0.1))
# my_crypto.add_transaction(Transaction("Luis", "Migue", 1))
#
# init_time = datetime.time()
# my_crypto.minePendingTransaction("Maca")
# to_time = datetime.time()
# print(f"Time spent {init_time - to_time} secs")
#
# print("Leandro has " + str(my_crypto.getBalance("Leandro")) + " LeanCoins in his wallet")
# print("Gaby has " + str(my_crypto.getBalance("Leandro")) + " LeanCoins in his wallet")
# print("Maca has " + str(my_crypto.getBalance("Leandro")) + " LeanCoins in his wallet")
# print('-' * 20)
#
# for x in range(len(my_crypto.chain)):
#     print(f"Block hash {x}: {my_crypto.chain[x].hash}")
# print(my_crypto.isValidChain())

# Creacion de la web app usando flask
app = Flask(__name__)

# Crear objeto blockchain
blockchain = Blockchain()
# Creacion de la direccioin del nodo en el puerto 5000
node_address = str(uuid4()).replace("-", "")


# Minar nuevo bloque
@app.route('/mine-block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiber="Leandro", amount=10)
    block = blockchain.create_block(proof, previous_hash)
    actual_hash = blockchain.hash(block)
    response = {'message': 'New block mining',
                'index': block['index'],
                'time-stamp': block['time-stamp'],
                'proof': block['proof'],
                'previous-hash': block['previous-hash'],
                'hash': actual_hash,
                'transactions': block['transactions']}
    return jsonify(response), 200


# Funcion para obtener la cadena
@app.route('/get-chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Validacion de la blockchain
@app.route('/valid', methods=['GET'])
def validate_blockchain():
    valid = blockchain.chain_validator(blockchain.chain)
    if valid:
        response = {'messege': 'La blockchain funciona'}
    else:
        response = {'messege': 'La blockchain no funciona'}
    return jsonify(response), 200


# Agregar nueva transaccion a la cadena
@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    json = requests.get_json()
    transaction_keys = ['sender', 'receiver', 'v']
    if not all(key in json for key in transaction_keys):
        return "Transaction incomplete", 400
    index = blockchain.add_transaction(sender=json['sender'], receiber=json['receiver'], amount=json['amount'])
    response = {'messege': f'The transaction has been added to block correctly {index}'}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
