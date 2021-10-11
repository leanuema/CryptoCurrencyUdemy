import datetime
import json
import pprint
from time import time

from Block import Block
from Transaction import Transaction


class Blockchain:
    def __init__(self):
        self.chain = [self.genesisBlock()]
        self.difficulty = 5
        self.pendingTransaction = []
        self.reward = 10

    # funcion que genera el bloque 0 con la fecha actual
    def genesisBlock(self):
        gblock = Block(str(datetime.datetime.now()), "block 0 from blockchain")
        return gblock

    # se obtiene el ultimo bloque de la cadena
    def getLastBlock(self):
        return self.chain[-1]

    # se recorre la lista de transacciones y se buscan los bloques a minar
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

    def isValidChain(self):
        for x in range(1, len(self.chain)):
            currentBlock = self.chain[x]
            previousBlock = self.chain[x - 1]

            if (currentBlock.previousBlock != previousBlock.hash):
                print("Invalid chain")

        print("Valid chain and secure")

    # funcion que crea una nueva transaccion y la almacena en la lista
    def createTransaction(self, transaction):
        self.pendingTransaction.append(transaction)

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

my_crypto = Blockchain()

print("Leandro, begun to mine")

my_crypto.createTransaction(Transaction("Macia", "JB", 0.01))
my_crypto.createTransaction(Transaction("Leandro", "Seba", 0.1))
my_crypto.createTransaction(Transaction("Luis", "Migue", 1))

init_time = time()
my_crypto.minePendingTransaction("Leandro")
to_time = time()
print(f"Time spent {init_time-to_time} secs")

print("Gaby, begun to mine")

my_crypto.createTransaction(Transaction("Macia", "JB", 0.01))
my_crypto.createTransaction(Transaction("Leandro", "Seba", 0.1))
my_crypto.createTransaction(Transaction("Luis", "Migue", 1))

init_time = time()
my_crypto.minePendingTransaction("Gaby")
to_time = time()
print(f"Time spent {init_time-to_time} secs")

print("Maca, begun to mine")

my_crypto.createTransaction(Transaction("Macia", "JB", 0.01))
my_crypto.createTransaction(Transaction("Leandro", "Seba", 0.1))
my_crypto.createTransaction(Transaction("Luis", "Migue", 1))

init_time = time()
my_crypto.minePendingTransaction("Maca")
to_time = time()
print(f"Time spent {init_time-to_time} secs")

print("Leandro has " + str(my_crypto.getBalance("Leandro")) + " LeanCoins in his wallet")
print("Gaby has " + str(my_crypto.getBalance("Leandro")) + " LeanCoins in his wallet")
print("Maca has " + str(my_crypto.getBalance("Leandro")) + " LeanCoins in his wallet")
print('-'*20)

for x in range(len(my_crypto.chain)):
    print(f"Block hash {x}: {my_crypto.chain[x].hash}")
print(my_crypto.isValidChain())