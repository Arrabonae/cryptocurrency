# Blockchain based coin with Python
The follow code has 4 miners which can be run from the same computer using different ports and they can interact with other.

The demo code has the following functionalities:

## /get_chain
Creates the genesis block and/or returns the chain, including each block and the length of the chain.

## /mine_block 
Calling this, the miner will mine the current block and includes the currently available transactions from the memory. 
### The following mining parameters are embedded into the code: 
* The block will consist the of the following information:
    * index, transaction, previous hash, timestamp, nonce, difficulty target.
* The difficulty target is set to be static, 4 zeros at the beginning of the hash of the block.

## /add_transaction 
Adds a transaction to the memory, which will be mined when the '/mine_block' called

## /force_consensus
This function compares the chains in the network and copies the longest chain to all miner's local chain. In addition it will also save the deleted chain's transactions which were not present in the longest chain, this ensures that no transaction will be lost. These transactions will be added to the chain next time a block is mined. 

## /is_valid
Validates if the chain is valid or not, that is check if there was no tampering with the chain. 

### Contributing
This project is based on the code from the following repository: https://github.com/deividroger/course-blockchain-a-z