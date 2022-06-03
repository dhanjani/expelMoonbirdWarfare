# expelMoonbirdWarfare
Renest your expelled Moonbird. Play gas warfare with the MoonBird admin with the EXPULSION_ROLE.

The MoonBirds contract allows admins with the EXPULSION_ROLE to expel your nested moonbird in cases where you have nested
it and also put it up for sale.

Problem is, the expel mechanism doesn't have a timeout and backoff period, like for example your mobile phone does 
when you incorrectly input the wrong passcode.

You can use this code in many different ways. Here's one way using blocknative.com:

1. Get ngkrok. Start ngrok: ngrok http 127.0.0.1:5000. Note down the forwarding address.
2. Set the values of $PRIVATE_KEY, $ACCOUNT_ADDR, $PROVIDER, $MB_CONTRACT. Note the $ACCOUNT_ADDR and $PRIVATE_KEY
    correspond to the wallet that owns your bird. CAREFUL.
3. Set the value of tokenId in expelMoonbirdWarfare.py to that of your bird's tokenid.
4. Run on commandline where you have python and flask (figure out the other dependencies):
    FLASK_APP=expelMoonbirdWarfare.py pipenv run flask run
4. Sign up for a free account on https://www.blocknative.com
5. Setup a new subscription on blocknative with the MoonBirds contract 0x23581767a106ae21c074b2276d25e5c3e136a68b.
6. Configure the following filters:
      { "contractCall.methodName": "expelFromNest" }
      { "contractCall.params.tokenId": "1" }
      { "status": "pending" }
      
7. Configure your blocknative subcription's webhook to be the address you noted down in 1. and append "/expel" to it.

Should be good to go. 

PS: Make sure your wallet has enough ETH to pay for gas. After all, the strategy is a gas war.
    
