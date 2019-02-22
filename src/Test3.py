import unittest
import hashlib
import random
from Transaction import Transaction
from UTXOPool import UTXOPool
from UTXO import UTXO
from keys import genkeys, sign, verify, n, g, p
from txHandler import txHandler

class TestMethods(unittest.TestCase):
 

    def test_3(self):
        print("Test 3: test isValidTx() with transactions containing signatures using incorrect private keys")
        nPeople = 10
        people = [] #new List RSAKeyPair
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

                 keyPair = utxoToKeyPair[utxoAtIndex[j]]
                 if (random.random() < pCorrupt):
                   randomKeyPair = random.randint(0,nPeople-1)
                   while people[randomKeyPair] == keyPair:
                       randomKeyPair = random.randint(0, nPeople - 1)
                   keyPair = people[randomKeyPair]
                   uncorrupted = False
         
                 tx.addSignature(sign(keyPair[0], hm,p,g), j)
                 pks.append(utxoToKeyPair[utxoAtIndex[j]][1])
           tx.finalize()
           if (txHandler.isValidTx(tx,utxoPool,pks) != uncorrupted):
             passes = False
        self.assertTrue(passes)


        
if __name__ == '__main__':
    unittest.main()
