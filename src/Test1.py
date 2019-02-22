import unittest
import hashlib
import random
from Transaction import Transaction
from UTXOPool import UTXOPool
from UTXO import UTXO
from keys import genkeys, sign, verify, n, g, p

#Maximal set for handle txs
#When do you have a maximal set of transactions, as long as no double spent, you should be able to add it. keep adding untill you see double spending that violates mutual validity ( create a container add txs to untill no further adds )
#EC:::: create one that has a maxium size hard problem because you end uo enumerating all subsets (knapsack)


class TestMethods(unittest.TestCase):
 
    def test_strings(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
 
    def test_keysigs(self):
        m = hashlib.sha256()
        m.update(b"Nobody respects")
        m.update(b" the spammish repetition")
        skx, pkx = genkeys(n,p,g)
        hm=int(m.hexdigest(),16)
        sig= sign(skx,hm,p,g)
        self.assertTrue(verify(pkx,sig,hm,p,g))
        self.assertFalse(verify(pkx,sig,hm+1,p,g))

    def test_1(self):
        print("Test 1: test isValidTx() with valid transactions")
        nPeople = 10
        people = [] #new List DigSigKeyPair
        #Generate 10 public and secret keys
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
              print("Index",rIndex); print(people[rIndex])
              addr = people[rIndex][1]  #(sk,pk)
              value = random.random() * maxValue
              tx.addOutput(value , addr) #Addr is the public key
              keyPairAtIndex[j] = people[rIndex]
           tx.finalize() #adds the hash
         # add all num tx outputs to utxo pool
           for j in range(num):
              ut = UTXO(tx.getHash(), j)
              utxoPool.addUTXO(ut, tx.getOutput(j))
              utxoToKeyPair[ut] = keyPairAtIndex[j]

        utxoSet = utxoPool.getAllUTXO()
        print("Len of utxoSet", len(utxoSet))
        print(utxoSet)
        maxValidInput = min(maxInput, len(utxoSet))

        nTxPerTest= 11
        maxValidInput = 2
        maxOutput = 3
        passes = True

        for i in range(nTxPerTest):         
           tx = Transaction()
           utxoAtIndex = {}
           nInput = random.randint(1,maxValidInput+ 1)
           inputValue = 0.0
           for j in range(nInput):
              utxo = random.sample(utxoSet,1)[0]
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
         
           for j in range(nInput):
             m=hashlib.sha256()
             m.update(str.encode(tx.getRawDataToSign(j)))
             hm = int(m.hexdigest(),16)
             tx.addSignature(sign(utxoToKeyPair[utxoAtIndex[j]][0], hm,p,g), j)
         
           tx.finalize()
           if (not txHandler.isValidTx(tx)):
             passes = False
        self.assertTrue(passes)


        
if __name__ == '__main__':
    unittest.main()
