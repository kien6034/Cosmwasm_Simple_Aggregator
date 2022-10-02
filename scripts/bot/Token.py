from re import L
from .Bot import Bot
import json,base64

class Token(Bot):
    ## for simplicity, decimal = 6
    def __init__(self, network_type, deployer_key, symbol, initial_balances, minter, contract_addr=None) -> None:
        super().__init__(network_type, deployer_key)
        self.symbol = symbol

        initial_balances_data = []
        for user in initial_balances:
            initial_balances_data.append(
                {
                    "address": user[0],
                    "amount": user[1]
                }
            )
        if contract_addr == None:
            self.token_code_id = self.store_contract("terraswap_token")

            self.contract_addr = self.instantiate_contract(self.token_code_id, {
                "name": symbol,
                "symbol": symbol,
                "decimals": 6,
                "initial_balances": initial_balances_data,
                "mint": {
                    "minter": minter
                }
            })
        else: 
            print(f"** Getting contract at: {contract_addr}")
            self.contract_addr = contract_addr

    
    def increase_allowance(self, owner, spender, amount): 
        self.execute_contract(
            owner,
            self.contract_addr,
            {
                "increase_allowance": {
                    "spender": spender,
                    "amount": amount
                }
            },
            additional_msg = self.symbol
        )


    def send(self, sender, contract, amount, msg):
        send_msg = json.dumps(msg).strip().replace(' ', '').encode()
        send_msg_encoded = base64.b64encode(send_msg).decode()

        self.execute_contract(
            sender,
            self.contract_addr,
            {
                "send": {
                    "contract": contract,
                    "amount": amount,
                    "msg": send_msg_encoded
                }
            },
            additional_msg = self.symbol
        )
    
    def get_balance(self, user):
        return self.query_contract(
            self.contract_addr,
            {
                "balance": {
                    "address": user
                }
            },
            additional_msg= self.symbol
        )


    def mint(self, owner, recipient, amount): 
        self.execute_contract(
            owner,
            self.contract_addr,
            {
                "mint": {
                    "recipient": recipient,
                    "amount": amount
                }
            },
            additional_msg = self.symbol
        )

    def __repr__(self) -> str:
        return self.contract_addr