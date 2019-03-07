from Node import Node
#/* CompliantNode refers to a node that follows the rules (not malicious)*/
class CompliantNode(Node):

    def __init__(self, p_graph, p_malicious, p_txDistribution, numRounds):
         #       // IMPLEMENT THIS
         # Ignore p_malicious, p_graph, p_txDistribution, and num_rounds
         self.initial_tx = set()
         self.tx_set = set()
         self.followees = []


    def setFollowees(self, followees):
#        // IMPLEMENT THIS
        self.followees = followees

    def setPendingTransaction(self, pendingTransactions):
        self.initial_tx = pendingTransactions
        self.tx_set = pendingTransactions


    def sendToFollowers(self):
        return self.tx_set

    def receiveFromFollowees(self,candidates):
#        // IMPLEMENT THIS
        self.tx_set = self.tx_set.intersection(candidates).union(self.initial_tx)
