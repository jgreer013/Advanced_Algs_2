Create a Transaction class, which is a class that has two inner classes: Transaction.Output and Transaction.Input. A transaction output consists of a coin value and a public key to which it is being paid. A transaction input consists of a hash-pointer to the transaction that contains the funding of the corresponding output, the index of this funding output in that transaction, and a digital signature signed by the public key associated with the transaction input.

For a transaction to be validated by the system, signatures must be verified. A transaction must contain a valid signature using the public key in the funding transaction. Create a structure, say using string type, representing raw transaction data, which will be signed using the associated public key. To sign and verify a signature, you will use the functions defined from Part 1.

A transaction consists of a list of inputs, a list of outputs, and a unique ID. The class should contain methods to add and remove input items, add and remove output items, compute raw digests to be signed, add a signature to an input, and compute and store the hash-pointer of the entire transaction once all inputs/outputs/signatures have been added.

There is example starter code for a UTXO class that represents an unspent transaction output. A UTXO contains the hash of the transaction from which it originates as well as its index within that transaction. In this class there should be methods for testing equals, compute hashCode, and compareTo functions that allows for the testing of equality and comparison between two UTXOs based on their indices and the contents of their txHash arrays.

There is also starter code for the UTXOpool class that represents the current set of outstanding UTXOs. This pool contains a dictionary map from each UTXO to its corresponding transaction output. This class contains constructors to create a new empty UTXOPool or a copy of a given UTXOPool, and methods to add and remove UTXOs from a pool, get the output corresponding to a given UTXO, check if a UTXO is in the pool, and get a list of all UTXOs in the pool.

You will be responsible for creating a module that contains an API called txHandler that validates transactions using UTXOpool and updates the pool based on processing a set of non-conflicting tranactions contained in the pool. Your code should be stored in file (for example, txHandler.py or TxHandler.java). that contains code to implement and test the following:


def isValidTx (Transaction tx):

* Returns true if
* (1) all outputs claimed by tx are in the current UTXO pool,
* (2) the signatures on each input of tx are valid,
* (3) no UTXO is claimed multiple times by tx,
* (4) all of tx’s output values are non-negative, and
* (5) the sum of tx’s input values is greater than or equal to the sum of its output values; and false otherwise.


def handleTxs (possibleTxs)   # Transaction[] --> Transaction[]

* Handles each epoch by receiving a set of proposed
* transactions, checking each transaction for correctness using isValidTx(),
* returning a mutually valid array of accepted transactions.
* handleTxs() should return a mutually valid transaction set of maximal size ---
* one that can’t be enlarged simply by adding more transactions.

Based on the transactions it has chosen to accept, handleTxs should also update its internal view of UTXOPool to reflect the current set of unspent transaction outputs, so that future calls to handleTxs() and isValidTx() are able to correctly process/validate transactions that claimn outputs from transactions that were accepted in a previous call to handleTxs().

Extra Credit:  Improve the handleTxs() method so that it finds a set of transactions with maximum total transaction fees -- i.e. maximize the sum over all transactions in the set of (sum of input values - sum of output values)).