from Node import Node
#/* MaliciousNode refers to a node that doesn't follow the rules (malicious)*/
# A malicious node can just do nothing, sooooooooo yeah.
class MaliciousNode(Node):

    def __init__(self, p_graph, p_malicious, p_txDistribution, numRounds):
         #       // IMPLEMENT THIS
         # Ignore p_malicious, p_graph, p_txDistribution, and num_rounds
        pass


    def setFollowees(self, followees):
#        // IMPLEMENT THIS
        pass

    def setPendingTransaction(self, pendingTransactions):
#        // IMPLEMENT THIS
      pass


    def sendToFollowers(self):
        return set() # Never return any (malicious)

    def receiveFromFollowees(self,candidates):
#        // IMPLEMENT THIS
        pass
