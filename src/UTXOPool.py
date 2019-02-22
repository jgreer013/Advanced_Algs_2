from UTXO import UTXO

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

	def search(self,txHash,index):
		for ut in self.H.keys():
			if ut.equals(txHash,index):
				return self.H[ut]
		return None