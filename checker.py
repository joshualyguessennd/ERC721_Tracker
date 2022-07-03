import os
import sys
from os.path import join, dirname
import argparse
from web3 import Web3
from brownie import *
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")

load_dotenv(dotenv_path)

key = os.environ.get("WEB3_INFURA_PROJECT_ID")


parser = argparse.ArgumentParser()


# checker allow to research created token in three ways
# for a specific block, from a range of block , and stream the network for new created block
# default setting stream the ethereum nainnet node

parser.add_argument("--block", type=int)
parser.add_argument("--range", type=int, nargs=2)


# list of standard function for ERC721 token encode in keccak2563
ERC721_KeyWord = [
    "70a08231",  # balanceOf(address) check
    "6352211e",  # ownerOf(uint256) check
    "42842e0",  # safeTransferFrom(address,address,uint256) check
    "b88d4fde",  # safeTransferFrom(address,address,uint256,bytes) check
    "23b872dd",  # transferFrom(address,address,uint256) check
    "095ea7b3",  # approve(address,uint256) check
    "081812fc",  # getApproved(uint256) check
    "a22cb465",  # setApprovalForAll(address,bool)  check
    "e985e9c5",  # isApprovedForAll(address,address) check
    "17307eab",  # ApprovalForAll(address,address,bool)
    "c87b56dd",  # tokenURI(uint256)
    "2f745c59",  # tokenOfOwnerByIndex(address,uint256)
]

# HTTPS provider, this project use INFURA, don't forget to add your key to .env file
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{key}"))


def tx_checker(blockData):

    array = []
    results = []
    block = w3.eth.get_block(blockData, True)
    transactions = block["transactions"]
    for transaction in transactions:
        receipt = w3.eth.get_transaction_receipt(transaction["hash"].hex())
        receipt_logs = receipt["contractAddress"]

        # check if new addresses are created inside the block
        if receipt_logs != None:
            results.append(receipt_logs)
            print(f"address {receipt_logs} has been created during block {blockData}")
    for result in results:
        checker_count = 0
        try:
            contract = Contract(result)
            bytecode = contract.bytecode
            string = str(bytecode)
            for item in ERC721_KeyWord:
                # compare the bytecode with the standards ERC721 functions bytecode
                if item in string:
                    checker_count += 1
                    if checker_count == len(ERC721_KeyWord):
                        array.append(contract.address)
                        print(f"{contract.address} is a ERC721 token")
            # print(item1.bytecode)
        except ValueError:
            # print("this contract is not verified")
            pass

    return array


def main(argv=None):
    parse = parser.parse_args(argv)
    blockNumber = parse.block
    rangeblock = parse.range
    startBlock = w3.eth.get_block_number()
    # connect to mainnet network
    network.connect("mainnet")
    blockTo = int(startBlock)
    # list of new created NFTs
    list_address = []

    if blockNumber:
        print(f"fetching for block {blockNumber}")
        list_address = tx_checker(blockNumber)
    elif rangeblock:
        blockInit = rangeblock[0]
        for x in range(rangeblock[0], rangeblock[1]):
            print(f"fetching for block {blockInit}")
            tx_checker(blockInit)
            if tx_checker(blockInit) != []:
                list_address = tx_checker(blockInit)
            blockInit += 1
    else:
        while True:
            print(f"fetching for block {blockTo}")
            list_address = tx_checker(blockTo)
            if len(list_address) > 0:
                print(f"list of ERC721 {blockTo} is {list_address}")
            blockTo += 1

    # disconnect the network
    network.disconnect()
    print(f"list of ERC721 is {list_address}")
    return list_address


if __name__ == "__main__":
    sys.exit(main())
