import solcx
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json


class operation:
    def __init__(self, address, filepath, filename, url, contrectname):
        self.address = address
        self.filepath = filepath
        self.filename = filename
        self.url = url
        self.chain_id = 1337
        self.contrectname = contrectname

    def getspec(self):
        return {
            "language": "Solidity",
            "sources": {
                self.filename: {
                    "urls": [
                        self.filepath
                    ]
                }
            },
            "settings": {
                "optimizer": {
                    "enabled": True
                },
                "outputSelection": {
                    "*": {
                        "*": [
                            "metadata", "evm.bytecode", "abi"
                        ]
                    }
                }
            }
        }

    def deploy(self):
        out = solcx.compile_standard(self.getspec(), allow_paths=".")
        abi = out['contracts'][self.filename][self.contrectname]['abi']
        bytecode = out['contracts'][self.filename][self.contrectname]['evm']['bytecode']['object']
        web3 = Web3(Web3.HTTPProvider(self.url))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        nonce = web3.eth.getTransactionCount(self.address)
        temp = web3.eth.contract(bytecode=bytecode, abi=abi)
        txn = temp.constructor().buildTransaction(
            {
                "chainId": self.chain_id,
                "gasPrice": web3.eth.gas_price,
                "from": self.address,
                "nonce": nonce,
            }
        )
        txn_hash = web3.eth.send_transaction(txn)
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        address = txn_receipt['contractAddress']
        return address

    def getPropertyDetail(self, contrectaddress,id):

        with open('contractfile/abi.json', 'r') as openfile:
            abi = json.load(openfile)
        web3 = Web3(Web3.HTTPProvider(self.url))
        address = web3.toChecksumAddress(contrectaddress)
        contract = web3.eth.contract(address=address, abi=abi)
        return contract.functions.propertydetail(id).call()

    def uploadProperty(self, contrectaddress, private_key,landid,ethaddress,landaddress):
        with open('contractfile/abi.json', 'r') as openfile:
            abi = json.load(openfile)
        web3 = Web3(Web3.HTTPProvider(self.url))
        address = web3.toChecksumAddress(contrectaddress)
        contract = web3.eth.contract(address=address, abi=abi)
        simple_storage = web3.eth.contract(address=address, abi=abi)
        nonce = web3.eth.getTransactionCount(self.address)
        greeting_transaction = contract.functions.uploadproperty(landid,ethaddress,landaddress).buildTransaction(
            {
                "chainId": self.chain_id,
                "gasPrice": web3.eth.gas_price,
                "from": self.address,
                "nonce": nonce,
            }
        )

        signed_greeting_txn = web3.eth.account.sign_transaction(
            greeting_transaction, private_key=private_key
        )
        tx_greeting_hash = web3.eth.send_raw_transaction(
            signed_greeting_txn.rawTransaction)
        print("Updating stored Value...")
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)
        return tx_receipt


    def transfer(self, contrectaddress, private_key,landid,newaddress):
        with open('contractfile/abi.json', 'r') as openfile:
            abi = json.load(openfile)
        web3 = Web3(Web3.HTTPProvider(self.url))
        address = web3.toChecksumAddress(contrectaddress)
        contract = web3.eth.contract(address=address, abi=abi)
        simple_storage = web3.eth.contract(address=address, abi=abi)
        nonce = web3.eth.getTransactionCount(self.address)
        greeting_transaction = contract.functions.transfer(landid,newaddress).buildTransaction(
            {
                "chainId": self.chain_id,
                "gasPrice": web3.eth.gas_price,
                "from": self.address,
                "nonce": nonce,
            }
        )

        signed_greeting_txn = web3.eth.account.sign_transaction(
            greeting_transaction, private_key=private_key
        )
        tx_greeting_hash = web3.eth.send_raw_transaction(
            signed_greeting_txn.rawTransaction)
        print("Updating stored Value...")
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)
        return tx_receipt












"""Object"""

objDep = operation("0xe286679Bb1BA6BA4AC65538e70606D68Dc15335A",
                   "contractfile/sol2.sol", "sol2.sol", "HTTP://127.0.0.1:7545", "Asset")

"""Deploy operation"""

# getaddress=objDep.deploy()
# print(getaddress)

"""GEt operation"""

# getvalue = objDep.getval("0x3abe649700c6A0dF72aaa9E4Bf457754a57E1236")
# print(getvalue)


"""Set operation"""

# getvalue = objDep.setvalue("0x3abe649700c6A0dF72aaa9E4Bf457754a57E1236","55bff9aa76e061e09e9e59d98b34067dcef298c96c66cbd9b94d2b4660af4597",67)
# print(getvalue)
