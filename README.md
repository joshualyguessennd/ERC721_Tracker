ERC721_CHECKER is a tool build to detect newly ERC721 created addresses inside a EVM block

The ```checker.py``` loop into an array of standards ERC721' function encode in keccack 256 that match with new creating contract in the identified block

```
# list of standard function for ERC721 token encode in keccak2563
ERC721_KeyWord = [
    "70a08231",  # balanceOf(uint256)
    "6352211e",  # ownerOf(uint256)
    "42842e0",  # safeTransferFrom(address,address,uint256)
    "b88d4fde",  # safeTransferFrom(address,address,uint256,bytes)
    "23b872dd",  # transferFrom(address,address,uint256)
    "095ea7b3",  # approve(address,uint256)
    "081812fc",  # getApprove(uint256)
    "a22cb465",  # setApprovalForAll(address,bool)
    "e985e9c5",  # isApprovedForAll(address,address)
    "ddf252ad",  # Transfer(address,address,uint256)
    "8c5be1e5",  # Approval(address,address,uint256)
    "17307eab",  # ApprovalForAll(address,address,bool)
    "c87b56dd",  # tokenURI(uint256)
    "2f745c59",  # tokenOfOwnerByIndex(address,uint256)
]
```

# Installation

ensure that ```eth-brownie``` package is installed

```
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
python3 -m pip install eth-brownie
```

# USAGE

```
python3 checker.py --block 13821429
```
output

```
fetching for block 13821429
list of ERC721 is ['0xD16bdCCAe06DFD701a59103446A17e22e9ca0eF0']
['0xD16bdCCAe06DFD701a59103446A17e22e9ca0eF0']
```


