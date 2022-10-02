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
tk0 = Token(network, deployer_key, "TKA", [(deployer.key.acc_address, "1000"),(user2.key.acc_address, "1000")], deployer.key.acc_address)
tk1 = Token(network, deployer_key, "TKB", [(deployer.key.acc_address, "1000"),(user2.key.acc_address, "1000")], deployer.key.acc_address)
tk2 = Token(network, deployer_key, "TKC", [(deployer.key.acc_address, "1000"),(user2.key.acc_address, "1000")], deployer.key.acc_address)


# deploy pair and lp token
pair01 = Pair("localterra", deployer_key, repr(tk0), repr(tk1), "50")
lp01 = Token(network, deployer_key, "LLP", [(deployer.key.acc_address, "100")], repr(pair01))
pair01.set_lp_token(repr(lp01))

pair12 = Pair("localterra", deployer_key, repr(tk1), repr(tk2), "50")
lp01 = Token(network, deployer_key, "LLP", [(deployer.key.acc_address, "100")], repr(pair01))
pair01.set_lp_token(repr(lp01))

print("\n ==> provide liquidity for pair 01 ")
liquid01 = "100"
tk0.increase_allowance(deployer, repr(pair01), liquid01)
tk1.increase_allowance(deployer, repr(pair01), liquid01)
pair01.add_liquid(deployer, liquid01, liquid01)

print("\n ==> provide liquidity for pair 12 ")
liquid12 = "100"
tk1.increase_allowance(deployer, repr(pair12), liquid12)
tk2.increase_allowance(deployer, repr(pair12), liquid12)
pair12.add_liquid(deployer, liquid12, liquid12)

# deploy lp token 
router = Router(network, deployer_key)

swap_actions = [
    {
        "pair_id": repr(pair01),
        "amount_in": "100",
        "path": [repr(tk0), repr(tk1)]
    },
    {
        "pair_id": repr(pair12),
        "amount_in": "10",
        "path": [repr(tk1), repr(tk2)]
    }
]

tk0.increase_allowance(deployer, repr(router), "100")
tk1.increase_allowance(deployer, repr(router), "100")
tk2.increase_allowance(deployer, repr(router), "100")
router.swap(deployer, swap_actions)

