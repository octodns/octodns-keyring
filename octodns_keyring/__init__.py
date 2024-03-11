#
#
#

from importlib import import_module

from keyring import get_keyring

from octodns.secret.base import BaseSecrets
from octodns.secret.exception import SecretsException

# TODO: remove __VERSION__ with the next major version release
__version__ = __VERSION__ = '0.0.1'


class KeyringSecretsException(SecretsException):
    pass


class KeyringSecretsBackendException(KeyringSecretsException):
    pass


class KeyringSecrets(BaseSecrets):
    def __init__(self, name, backend=None):
        super().__init__(name)
        self.backend = self._load_backend(backend)

    def _load_backend(self, backend):
        if backend is None:
            return get_keyring()

        try:
            module_name, class_name = backend.rsplit('.', 1)
            module = import_module(module_name)
        except (ImportError, ValueError):
            self.log.exception(
                '_load_backend: Unable to import module "%s"', backend
            )
            raise KeyringSecretsBackendException(
                f'Unknown backend class: "{backend}"'
            )

        try:
            klass = getattr(module, class_name)
        except AttributeError:
            self.log.exception(
                '__init__: Unable to get class "%s" from module "%s"',
                class_name,
                module,
            )
            raise KeyringSecretsBackendException(
                f'Unknown backend class: "{backend}"'
            )

        return klass()

    def fetch(self, name, source):
        service_name, secret_name = name.split('/')
        ret = self.backend.get_password(service_name, secret_name)
        if ret is None:
            raise KeyringSecretsException(f'failed to find {name}')
        return ret
