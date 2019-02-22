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
            if txOutValue is None and not utxoPool.contains(txOutValue) and txOutValue < 0:
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
                return False
            if (txIn.prevTxHash,txIn.signature) in inputTracker:
                return False
            else:
                inputTracker.add((txIn.prevTxHash,txIn.signature))
            verifyTransaction.addInput(txIn.prevTxHash,txIn.outputIndex)

            m = hashlib.sha256()
            m.update(str.encode(verifyTransaction.getRawDataToSign(txInputInd)))
            hm = int(m.hexdigest(), 16)
            #HM is same, pk is correct as it is passed in so signatures should match
            if not verify(pks[txInputInd],txIn.signature,hm):
                return False

            if prevTxOut.value is None or prevTxOut.value < 0:
                return False
            else:
                txInSum += prevTxOut.value
        return (txInSum >= txOutSum)
    @staticmethod
    # * Handles each epoch by receiving a set of proposed
    # * transactions, checking each transaction for correctness using isValidTx(),
    # * returning a mutually valid array of accepted transactions.
    # * handleTxs() should return a mutually valid transaction set of maximal size ---
    # * one that can’t be enlarged simply by adding more transactions.
    @staticmethod
    def handleTxs(possibleTxs, utxoPool, pksList):  # Transaction[] --> Transaction[]
        validTransactions = []
        inputTracker = set()
        for txInd in possibleTxs:
            transactionInputTracker = set()  # Seperate in case the transaction is invalid
            if txHandler.isValidTx(possibleTxs[txInd], utxoPool, pksList[txInd]):
                invalidInputFound = False
                for txInputInd in range(0, possibleTxs[txInputInd].getInputLen()):
                    txIn = possibleTxs[txInputInd].getInput(txInputInd)
                    prevTxOut = utxoPool.search(txIn.prevTxHash, txIn.outputIndex)
                    if prevTxOut is None:
                        invalidInputFound = True
                        break
                    if (txIn.prevTxHash, txIn.signature) in inputTracker:
                        invalidInputFound = True
                        break
                    else:
                        transactionInputTracker.add((txIn.prevTxHash, txIn.signature))
            if not invalidInputFound:
                inputTracker = inputTracker.union(transactionInputTracker)
                validTransactions.append(possibleTxs[txInd])
        return validTransactions