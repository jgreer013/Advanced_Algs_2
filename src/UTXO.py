class UTXO():

    txHash = None
    index = None

    def __init__(self, txHash, index):
        self.txHash = txHash;
        self.index = index;
    
    def getTxHash(self):
        return self.txHash
    
    def getIndex(self):
        return self.index
    

    def equals(self,other):
        if (other == None):
            return False
        if (type(self) != type(other)):
            return False
        hash = other.txHash
        ind = other.index
        if (len(hash) != len(self.txHash) or self.index != ind):
            return False
        for i in range(len(hash)):
            if (hash[i] != self.txHash[i]):
                return False
        
        return True
    

    def compareTo(self,utxo):
        hash = utxo.txHash
        ind = utxo.index
        if (ind > self.index):
            return -1;
        elif (ind < self.index):
            return 1;
        else:
            len1 = len(self.txHash)
            len2 = len(hash)
            if (len2 > len1):
                return -1;
            elif (len2 < len1):
                return 1
            else:
                for i in range(len1):
                    if (hash[i] > self.txHash[i]):
                        return -1
                    elif (hash[i] < self.txHash[i]):
                        return 1
                
                return 0
            
        
    

   
