#
#
#

from keyring.backend import KeyringBackend


class DummyBackend(KeyringBackend):
    priority = 1

    def set_password(self, servicename, username, password):
        pass

    def delete_password(self, servicename, username):
        pass

    def get_password(self, servicename, username):
        return f'dummy-{servicename}-{username}'


class NoneBackend(KeyringBackend):
    priority = 1

    def set_password(self, servicename, username, password):
        pass

    def delete_password(self, servicename, username):
        pass

    def get_password(self, servicename, username):
        return None
