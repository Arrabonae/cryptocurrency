# Cryptocurrency
The follow code has 4 miners which can be run from the same computer using different ports and they can interact with other.

The demo code has the following functionalities:

## /get_chain
Creates the genesis block and/or returns the chain, including each block and the lenght of the chain.

## /mine_block 
Calling this, the miner will mine the current block and includes the currently available transactions from the memory. 

## /add_transaction 
Adds a transaction to the memory, which will be mined whem the '/mine_block' called

## /force_consensus
This function compares the chains in the network and copies the longest chaain to all miner's local chain. In addition it will also save the deleted chain's transactions which were not present in the longest chain, this ensures that no transaction will be lost. These transactions will be added to the chain next time a block is mined. 

## /is_valid
Validates if the chain is valid or not, that is check if there was no tempering with the chain. 

### Contributing
This project is based on the code fromt he following repository: https://github.com/deividroger/course-blockchain-a-z