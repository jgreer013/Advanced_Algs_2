
class UTXOPool():

    H = {}

    def __init__(self):
        self.H = {} #UTXO, Transaction.Output
 
    def addUTXO(self, utxo, txOut):
        self.H[utxo] = txOut

    def put(self, utxo, txOut):
        self.H[utxo] = txOut
    
    def remove(self, utxo):
         self.H.remove(utxo)

    def getTxOutput(self, ut):
        return self.H.get(ut);
    
    def contains(self, utxo):
        return utxo in self.H
    
    def getAllUTXO(self):
        setUTXO = self.H.keys()
        allUTXO = []
        for ut in setUTXO:
            allUTXO.append(ut)
        return allUTXO
