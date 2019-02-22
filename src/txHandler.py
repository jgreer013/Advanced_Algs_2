from  UTXOPool import UTXOPool
from UTXO import  UTXO
import hashlib

from Transaction import Transaction
#TODO: where is utxopool initialized etc?
from keys import verify
class txHandler():

    @staticmethod
    def isValidTx(tx,utxoPool,pks):
        verifyTransaction = Transaction()
        #* Returns true if
        #* (1) all outputs claimed by tx are in the current UTXO pool,
        #* (4) all of tx’s output values are non-negative, and
        txOutSum = 0
        for txInputInd in range(0,tx.getOutputLen()):
            txOut = tx.getOutput(txInputInd)
            txOutValue = txOut.value
            print(txOutValue)
            if txOutValue is None and not utxoPool.contains(txOutValue) and txOutValue < 0:
                #print("False line 1")
                return False
            else:
                txOutSum+=txOutValue
            verifyTransaction.addOutput(txOut.value,txOut.address)
        #* (3) no UTXO is claimed multiple times by tx, meaning that an input cannot occur twice
        inputTracker = set()

        #* (2) the signatures on each input of tx are valid,
        #* (5) the sum of tx’s input values is greater than or equal to the sum of its output values; and false otherwise.
        txInSum = 0
        for txInputInd in range(0,tx.getInputLen()):
            txIn = tx.getInput(txInputInd)
            prevTxOut = utxoPool.search(txIn.prevTxHash,txIn.outputIndex)
            if prevTxOut is None:
                #print("False line 2")
                return False
            #prevTxOut = prevTx.getOutput(txIn.outputIndex)
            #TODO: Fails here on some tests but test one doesn't prevent multiple of the same input
            if (txIn.prevTxHash,txIn.signature) in inputTracker:
                #print("False line 3")
                #print("hash",txIn.prevTxHash,"outindex",txIn.outputIndex,"sig",txIn.signature)
                #print(inputTracker)
                return False
            else:
                inputTracker.add((txIn.prevTxHash,txIn.signature))
            verifyTransaction.addInput(txIn.prevTxHash,txIn.outputIndex)

            m = hashlib.sha256()
            m.update(str.encode(verifyTransaction.getRawDataToSign(txInputInd)))
            hm = int(m.hexdigest(), 16)
            #HM is same, pk is correct as it is passed in so signatures should match
            #TODO: public key matches with secret key and so does the message but cannot verify
            #print("isValid Output")
            #print(txInputInd)
            #print("pk", pks[txInputInd])
            #print("hm", hm)
            #print("printsig-nocalc", txIn.signature)
            if not verify(pks[txInputInd],txIn.signature,hm):
                #print("False line 4")
                return False


            if prevTxOut.value is None or prevTxOut.value < 0:
                #print("False line 5")
                return False
            else:
                txInSum += prevTxOut.value
        #if not (txInSum >= txOutSum):
            #print("False line 6")
            #print("in:",txInSum)
            #print("out",txOutSum)
        return (txInSum >= txOutSum)
    @staticmethod

    def handleTxs(possibleTxs):  # Transaction[] --> Transaction[]

        for tx in possibleTxs:
            if not txHandler.isValidTx(tx):
                pass #if any transactiona are invalid, just ignore them or return None

    #* Handles each epoch by receiving a set of proposed
    #* transactions, checking each transaction for correctness using isValidTx(),
    #* returning a mutually valid array of accepted transactions.
    #* handleTxs() should return a mutually valid transaction set of maximal size ---
    #* one that can’t be enlarged simply by adding more transactions.

        pass