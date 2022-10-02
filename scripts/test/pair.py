from asyncio import constants
from ..bot.Bot import Bot
from ..bot.Pair import Pair
from ..bot.Token import Token
from ..bot.Router import Router
from terra_sdk.client.lcd import LCDClient
from dotenv import load_dotenv
import os, sys, json, base64

load_dotenv() 
network = "localterra"

deployer_key = os.environ.get("MNEMONIC_KEY")
bot = Bot(network, deployer_key)
deployer = bot.get_deployer()
user2 = bot.get_lt_wallet("test2")

# deploy token0 and token1 
tk0 = Token(network, deployer_key, "TKA", [(deployer.key.acc_address, "1000"),(user2.key.acc_address, "100")], deployer.key.acc_address)
tk1 = Token(network, deployer_key, "TKB", [(deployer.key.acc_address, "1000"),(user2.key.acc_address, "0")], deployer.key.acc_address)

# deploy pair and lp token
pair01 = Pair("localterra", deployer_key, repr(tk0), repr(tk1), "50")
lp01 = Token(network, deployer_key, "LLP", [(deployer.key.acc_address, "100")], repr(pair01))
pair01.set_lp_token(repr(lp01))


print("\n ==> provide liquidity for pair 01 ")
liquid01 = "1000"
tk0.increase_allowance(deployer, repr(pair01), liquid01)
tk1.increase_allowance(deployer, repr(pair01), liquid01)
pair01.add_liquid(deployer, liquid01, liquid01)



# # Swap using method 1 
# tk0.increase_allowance(user2, repr(pair01), "100")
# pair01.swap(user2, "100", [ repr(tk0),repr(tk1)])
# tk0.get_balance(user2.key.acc_address)
# tk1.get_balance(user2.key.acc_address)


# Swap using method 2 
amount_in = "100"
swap_msg =  {
    "amount_in": amount_in,
    "path": [repr(tk0), repr(tk1)]
}
tk0.send(user2, repr(pair01), amount_in, swap_msg)


tk0.get_balance(user2.key.acc_address)
tk1.get_balance(user2.key.acc_address)