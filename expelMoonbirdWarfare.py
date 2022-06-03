from audioop import add
from base64 import encode
from lib2to3.pgen2 import token
from operator import truediv
from brownie import Contract, web3
from eth_abi import encode_single
from flask import Flask, request
from web3 import Web3, contract
from web3.middleware import geth_poa_middleware
import os
import sys
from time import sleep

#created by Nitesh Dhanjani

#This code is being provided as is. 
#No guarantee, representation or warranty is being made, express or implied, as to the safety or correctness of the code. 
#It has not been audited and as such there can be no assurance it will work as intended, and users may experience delays, failures, errors, omissions, 
#loss of transmitted information or loss of funds. Nitesh Dhanjani is not liable for any of the foregoing.
#Users should proceed with caution and use at their own risk.

#the MoonBirds contract allows admins with the EXPULSION_ROLE to expel your nested moonbird in cases where you have nested
#it and also put it up for sale
#problem is, the expel mechanism doesn't have a timeout and backoff period, like for example your mobile phone does
#when you incorrectly input the wrong passcode


#this app will prepetually re-nest your expelled bird asap
#of course, this costs you gas
#but so does the expulsion transaction, it costs the admin gas
#so anon, who will win the gas war?

#this app serves a webhook (use ngrok for example with https://explorer.blocknative.com with the following filters:
#   { "contractCall.methodName": "expelFromNest" }, { "contractCall.params.tokenId": "1" }, { "status": "pending" }

#set your MoonBird tokenId
tokenId = 1

#set your PROVIDER in .env
w3 = Web3(
    Web3.HTTPProvider(
        os.getenv("PROVIDER")
    )
)

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#set your PRIVATE_KEY and ACCOUNT_ADDR in .env
p_key = os.getenv("PRIVATE_KEY")
addr = os.getenv("ACCOUNT_ADDR")

expelMoonbirdWarfare = Flask(__name__)

with open("MB_ABI.json") as fp:
    abi = fp.read()

#set the addresss of the MoonBird contract in .env
mb_contract = w3.eth.contract(
    address=os.getenv("MB_CONTRACT"), abi=abi
)


@expelMoonbirdWarfare.route("/expel", methods=["GET", "POST"])
def receive_expel():

    isNested = mb_contract.functions.nestingPeriod(tokenId).call()

    # the expelFromNest transaction is in the mempool/pending so make sure our bird is nested
    # for the rare case that admin calls expel when our bird is not nested (expel will fail)
    # could remove this check, worst in this case would be we nest our unnested bird (which could be a problem if it's listed)
    if isNested[0] == True:

        hash = request.json["hash"]

        blocknum = w3.eth.blockNumber

        for attempt in range(60):
            try:
                expel_txn = w3.eth.getTransaction(hash)
                break
            except:
                sleep(1.25)

        if "pendingBlockNumber" in expel_txn:
            if expel_txn["pendingBlockNumber"] <= blocknum:
                sys.exit("block number mismatch")
            elif "blockNumber" in expel_txn:
                if expel_txn["blockNumber"] <= blocknum:
                    sys.exit("block number mismatch")
            else:
                sys.exit("block number mismatch")

        # check to make sure the expel transaction is for the moonbirds contract and for our tokenId
        if expel_txn["to"] == os.getenv("MB_CONTRACT"):
             if expel_txn[
                "input"
            ] == "0x39154b9e00000000000000000000000000000000000000000000000000000000000" + format(
                tokenId, "05d"
            ):

            # send transactio to re-nest bird asap
                txn = mb_contract.functions.toggleNesting([1]).buildTransaction(
                    {"nonce": w3.eth.getTransactionCount(addr)}
                    )

        signed = w3.eth.account.sign_transaction(txn, private_key=p_key)

        w3.eth.send_raw_transaction(signed.rawTransaction)

    return "ok!", 200
