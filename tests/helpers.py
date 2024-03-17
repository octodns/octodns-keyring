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


class UsernameBackend(KeyringBackend):
    '''Whatever is passed as username is returned as the secret value'''

    priority = 1

    def set_password(self, servicename, username, password):
        pass

    def delete_password(self, servicename, username):
        pass

    def get_password(self, servicename, username):
        return username


class TupleBackend(KeyringBackend):
    '''Always returns a tuple with the answer to everything'''

    priority = 1

    def set_password(self, servicename, username, password):
        pass

    def delete_password(self, servicename, username):
        pass

    def get_password(self, servicename, username):
        return (42,)
