from core.vault import vault_create, vault_open, vault_save


class VaultSession:
    def __init__(self, vault_path: str, password: str, create: bool = False):
        self.vault_path = vault_path
        self.password = password

        if create:
            self.data = vault_create(vault_path, password)
        else:
            self.data = vault_open(vault_path, password)

        self.is_open = True

    def save(self):
        if not self.is_open:
            raise RuntimeError("Vault session is closed.")
        vault_save(self.vault_path, self.password, self.data)

    def close(self):
        if not self.is_open:
            return

        self.save()

        self.data = None
        self.password = None
        self.is_open = False
