from fireblocks_sdk import FireblocksSDK

API_KEY = "d5ce7e80-d6a5-598a-88a3-037660377627"
with open('/Users/slavaserebriannyi/api_keys/fireblocks_secret.key', 'r') as f:
    SECRET_KEY = f.read()


class FireblocksProvider:
    def __init__(self):
        self._api_key = API_KEY
        self._secret = SECRET_KEY
        self._client = FireblocksSDK(self._secret, self._api_key)

    def create_new_vault_account(self, name):
        new_vault_account = self._client.create_vault_account(name, True)
        return new_vault_account

    def create_new_wallet(self, vault_account_id, asset_id):
        new_wallet = self._client.create_vault_asset(vault_account_id, asset_id)
        return new_wallet

    def get_vault_account_info(self, vault_account_id):
        vault_account = self._client.get_vault_account(vault_account_id)
        return vault_account

    def get_asset_balance(self, vault_account_id, asset_id):
        balance = self._client.get_vault_account_asset(vault_account_id, asset_id)
        return balance

    def create_new_utxo_address(self, vault_account_id, asset_id, description):
        address = self._client.generate_new_address(vault_account_id, asset_id, description)
        return address
