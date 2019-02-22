import unittest
import hashlib
import random
from Transaction import Transaction
from UTXOPool import UTXOPool
from UTXO import UTXO
from keys import genkeys, sign, verify, n, g, p
from txHandler import txHandler

class TestMethods(unittest.TestCase):
 
    def test_2(self):
        print("Test 2: test isValidTx() with some invalid transactions")
        nPeople = 10
        people = [] #new list of KeyPair
        for i in range(nPeople):
           sk,pk = genkeys(n,p,g)
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
              tx.addOutput(value, addr);
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

           uncorrupted = True
           utxoAtIndex = {}
           nInput = random.randint(1,maxValidInput+ 1)
           inputValue = 0.0
           for j in range(nInput):
              utxo = random.sample(utxoSet, 1)[0]
              while ((utxo.getTxHash(), utxo.getIndex()) in usedInputs):
                  utxo = random.sample(utxoSet, 1)[0]
              usedInputs.add((utxo.getTxHash(), utxo.getIndex()))
              tx.addInput(utxo.getTxHash(), utxo.getIndex())
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

           pCorrupt = 0.5
           for j in range(nInput):
                 m=hashlib.sha256()
                 m.update(str.encode(tx.getRawDataToSign(j)))
                 hm = int(m.hexdigest(),16)
                 if (random.random() < pCorrupt):
                     hm += 1
                     uncorrupted = False
                 keyPair = utxoToKeyPair[utxoAtIndex[j]]
                 tx.addSignature(sign(keyPair[0], hm), j)
                 print("Test output")
                 print(j)
                 print("sk", utxoToKeyPair[utxoAtIndex[j]][0])
                 print("pk", utxoToKeyPair[utxoAtIndex[j]][1])
                 print("hm", hm)
                 print("sig", tx.getInput(j).signature)
                 pks.append(utxoToKeyPair[utxoAtIndex[j]][1])
           tx.finalize()
           if (txHandler.isValidTx(tx,utxoPool,pks) != uncorrupted):
               passes = False
               print("Failed")
               #txHandler.isValidTx(tx, utxoPool,pks)
               break
           else:
               print("Passed")
        self.assertTrue(passes)


        
if __name__ == '__main__':
    unittest.main()
