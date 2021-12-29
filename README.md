# Blockchain based coin with Python
The follow code has 3 miners which can be run from the same computer thru Flask using different ports and they can interact with other.

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


### Example result of a chain after few blocks are mine 

```json
{
    "blockchain": [
        {
            "difficulty target": "0000",
            "index": 1,
            "nonce": 0,
            "previous_hash": "0",
            "timestamp": "2021-12-28 15:24:42.523019",
            "transactions": []
        },
        {
            "difficulty target": "0000",
            "index": 2,
            "nonce": 145061,
            "previous_hash": "c9fdd74086f1d1bdb366f427f94164c2dac7763b42a98b0dfeec687b728867e8",
            "timestamp": "2021-12-28 15:26:03.479988",
            "transactions": []
        },
        {
            "difficulty target": "0000",
            "index": 3,
            "nonce": 19814,
            "previous_hash": "00008b83d3132a5c26396176805b324f7fb1aa78439d7ea708b22bc008b9e881",
            "timestamp": "2021-12-28 15:26:04.216987",
            "transactions": [
                {
                    "amount": 1,
                    "comment": "Mining Reward for mining block 2",
                    "receiver": "5001",
                    "sender": "The Network"
                }
            ]
        },
        {
            "difficulty target": "0000",
            "index": 4,
            "nonce": 68850,
            "previous_hash": "00001b2097cdddcbb33fafe662bda4bd444827a373327c097688d88d088df638",
            "timestamp": "2021-12-28 15:26:05.543427",
            "transactions": [
                {
                    "amount": 1,
                    "comment": "Mining Reward for mining block 3",
                    "receiver": "5001",
                    "sender": "The Network"
                }
            ]
        },
        {
            "difficulty target": "0000",
            "index": 5,
            "nonce": 60183,
            "previous_hash": "000074eed8f16c98479cb7ad2e31901681a707c4d541a7ffc26a849f7852482e",
            "timestamp": "2021-12-28 15:26:06.716867",
            "transactions": [
                {
                    "amount": 1,
                    "comment": "Mining Reward for mining block 4",
                    "receiver": "5001",
                    "sender": "The Network"
                }
            ]
        },
        {
            "difficulty target": "0000",
            "index": 6,
            "nonce": 4206,
            "previous_hash": "0000a75b9e0b3cf41648eca40c1d1fcfe9307ab2121a92ed477e2557be4dac51",
            "timestamp": "2021-12-28 15:26:07.243402",
            "transactions": [
                {
                    "amount": 1,
                    "comment": "Mining Reward for mining block 5",
                    "receiver": "5001",
                    "sender": "The Network"
                }
            ]
        },
        {
            "difficulty target": "0000",
            "index": 7,
            "nonce": 145128,
            "previous_hash": "000089fa82dd111c53d492b2d485ff73a2d8974a6086c6c3b3dbf99370b31999",
            "timestamp": "2021-12-28 16:11:08.345965",
            "transactions": [
                {
                    "amount": 1,
                    "comment": "Mining Reward for mining block 4",
                    "receiver": "5002",
                    "sender": "The Network"
                },
                {
                    "amount": 12,
                    "comment": "Thanks for the Coffee",
                    "receiver": "Me",
                    "sender": "You"
                },
                {
                    "amount": 1,
                    "comment": "Mining Reward for mining block 2",
                    "receiver": "5002",
                    "sender": "The Network"
                },
                {
                    "amount": 1,
                    "comment": "Mining Reward for mining block 3",
                    "receiver": "5002",
                    "sender": "The Network"
                }
            ]
        },
        {
            "difficulty target": "0000",
            "index": 8,
            "nonce": 3673,
            "previous_hash": "00009b0047b2f0ca36cc1ee0c37cbb07a1cdfc32a866e200a70381e750fa1a61",
            "timestamp": "2021-12-28 16:13:36.045229",
            "transactions": [
                {
                    "amount": 1,
                    "comment": "Mining Reward for mining block 7",
                    "receiver": "5002",
                    "sender": "The Network"
                },
                {
                    "amount": 11,
                    "comment": "Thanks for the Coffee back",
                    "receiver": "You",
                    "sender": "Me"
                }
            ]
        }
    ]
}
```