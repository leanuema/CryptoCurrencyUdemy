import hashlib


class Block:
    def __init__(self, timeStamp, transaction, previousBlock=''):
        self.timeStamp = timeStamp
        self.transaction = transaction
        self.previousBlock = previousBlock
        self.difficultyIncrement = 0
        self.hash = self.calculateHash(transaction, timeStamp, self.difficultyIncrement)

    # funcion para calcular hash
    def calculateHash(self, transaction, time_stamp, difficultIncrement):
        data = str(transaction) + str(time_stamp) + str(difficultIncrement)
        dataEncoded = data.encode()
        hash = hashlib.sha256(dataEncoded)
        return hash.hexdigest()

    # funcion para realizar el minado de bloques
    def mineBlock(self, difficulty):
        difficultyCheck = "0" * difficulty
        # valido que el numero de ceros que contiene la variable difficulty sea distinto del difficultyCheck
        # en caso de que sean iguales finaliza el bucle y se obtiene el minado
        while self.hash[:difficulty] != difficultyCheck:
            self.hash = self.calculateHash(self.transaction, self.timeStamp, self.difficultyIncrement)
            self.difficultyIncrement += 1
