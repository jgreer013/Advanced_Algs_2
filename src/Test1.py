import unittest
import hashlib
import random
from Transaction import Transaction
from UTXOPool import UTXOPool
from UTXO import UTXO
from keys import genkeys, sign, verify
from txHandler import txHandler

class TestMethods(unittest.TestCase):
 
	def test_strings(self):
		self.assertEqual('foo'.upper(), 'FOO')
		self.assertTrue('FOO'.isupper())
		self.assertFalse('Foo'.isupper())
 
	def test_keysigs(self):
		msg = [b"4194909766994028808293623689273419362309706882612353484933795166041013714163",
			   b"81514427175971543293164191618001506196838267623329851389681647701779330840600",
			   b"17252908227080267616614312042183132638406086197574336239937230109815325852588"]
		for i in range(len(msg)):
			m = hashlib.sha256()
			m.update(msg[i])
			skx, pkx = genkeys()
			hm=int(m.hexdigest(),16)
			sig= sign(skx,hm)
			self.assertTrue(verify(pkx,sig,hm))
			self.assertFalse(verify(pkx,sig,hm+1))
		#print("PASSED KEYSIGSSS")
	def test_1(self):
		print("Test 1: test isValidTx() with valid transactions")
		nPeople = 10
		people = [] #new List DigSigKeyPair
		for i in range(nPeople):
		   sk,pk = genkeys()
		   people.append((sk,pk))

# Create a pool and an index into key pairs
		utxoPool = UTXOPool()
		utxoToKeyPair = {}
		keyPairAtIndex = {}
		nUTXOTx=10
		maxUTXOTxOutput = 5
		maxInput = 3
		maxValue = 100

		for i in range(nUTXOTx):
		   num = random.randint(1,maxUTXOTxOutput)
		   tx = Transaction()
		   # add num randonm outputs to tx
		   for j in range(num):
			  # pick a random public address
			  rIndex = random.randint(0,len(people)-1)
			  #print("Index",rIndex); print(people[rIndex])
			  addr = people[rIndex][1]  #(sk,pk)
			  value = random.random() * maxValue
			  tx.addOutput(value , addr)
			  keyPairAtIndex[j] = people[rIndex]
		   tx.finalize()
		 # add all num tx outputs to utxo pool
		   for j in range(num):
			  ut = UTXO(tx.getHash(), j)
			  utxoPool.addUTXO(ut, tx.getOutput(j))
			  utxoToKeyPair[ut] = keyPairAtIndex[j]

		utxoSet = utxoPool.getAllUTXO()
		print("Len of utxoSet", len(utxoSet))
		maxValidInput = min(maxInput, len(utxoSet))

		nTxPerTest= 1000
		maxValidInput = 2
		maxOutput = 3
		passes = True

		for i in range(nTxPerTest):
		   pks = []
		   usedInputs = set()
		   tx = Transaction()
		   utxoAtIndex = {}
		   nInput = random.randint(1,maxValidInput+ 1)
		   inputValue = 0.0

		   for j in range(nInput):
			  utxo = random.sample(utxoSet, 1)[0]
			  while ((utxo.getTxHash(),utxo.getIndex()) in usedInputs):
				utxo = random.sample(utxoSet, 1)[0]
			  tx.addInput(utxo.getTxHash(), utxo.getIndex())
			  usedInputs.add((utxo.getTxHash(),utxo.getIndex()))

			  inputValue += utxoPool.getTxOutput(utxo).value
			  utxoAtIndex[j] = utxo
		   nOutput = random.randint(1,maxOutput)
		   outputValue = 0.0
		   for j in range(nOutput):
			   value = random.random()*(maxValue)
			   if (outputValue + value > inputValue):
				  break
			   rIndex = random.randint(0,len(people)-1)
			   addr = people[rIndex][1]
			   tx.addOutput(value, addr)
			   outputValue += value

		   for j in range(nInput):
			 m=hashlib.sha256()
			 m.update(str.encode(tx.getRawDataToSign(j)))
			 #print("Message")
			 #print(str.encode(tx.getRawDataToSign(j)))
			 hm = int(m.hexdigest(),16)
			 tx.addSignature(sign(utxoToKeyPair[utxoAtIndex[j]][0], hm), j)
			 #print(j)
			 #print("sk",utxoToKeyPair[utxoAtIndex[j]][0])
			 #print("pk",utxoToKeyPair[utxoAtIndex[j]][1])
			 #print("hm",hm)
			 #print("sig",tx.getInput(j).signature)
			 pks.append(utxoToKeyPair[utxoAtIndex[j]][1])
		   tx.finalize()
		   if (not txHandler.isValidTx(tx,utxoPool,pks)):
			   passes = False
			   passes = False
			   #print("TEST NUMBERRRRRRRRRRRRRRRRRR",i,"Failed")
			   break
		   else:
			   #print("TEST NUMBERRRRRRRRRRRRRRRRRR",i,"Passed HERE")
			   pass
		   #print("\n\n\n")
		self.assertTrue(passes)



if __name__ == '__main__':

	unittest.main()
