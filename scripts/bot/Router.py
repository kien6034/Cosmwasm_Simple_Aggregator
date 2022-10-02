from .Bot import Bot


class Router(Bot):
    ## for simplicity, decimal = 6
    def __init__(self, network_type, deployer_key, contract_addr =None) -> None:
        super().__init__(network_type, deployer_key)

        if contract_addr == None:
            self.token_code_id = self.store_contract("router")

            self.contract_addr = self.instantiate_contract(self.token_code_id, {
            })
        else:
            print(f"** Getting contract at: {contract_addr}")
            self.contract_addr = contract_addr

        self.phrase = "ROUTER"
    
    def swap(self,sender, actions): 
        self.execute_contract(
            sender,
            self.contract_addr,
            {
                "swap": {
                    "actions": actions
                }
            },
        )
    
    
    def __repr__(self) -> str:
        return self.contract_addr