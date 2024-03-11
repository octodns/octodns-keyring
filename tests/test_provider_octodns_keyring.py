#
#
#

from unittest import TestCase

from octodns_keyring import (
    KeyringSecrets,
    KeyringSecretsBackendException,
    KeyringSecretsException,
)


class TestKeyringSecrets(TestCase):
    def test_keyring(self):
        ks = KeyringSecrets('test')
        self.assertTrue(ks.backend)
        # we have no idea what secrets this one will have since it's
        # auto-selected by the code based on OS and such

        with self.assertRaises(KeyringSecretsBackendException) as ctx:
            KeyringSecrets('test', backend='')
        self.assertEqual('Unknown backend class: ""', str(ctx.exception))

        with self.assertRaises(KeyringSecretsBackendException) as ctx:
            KeyringSecrets('test', backend='does.not.Exist')
        self.assertEqual(
            'Unknown backend class: "does.not.Exist"', str(ctx.exception)
        )

        with self.assertRaises(KeyringSecretsBackendException) as ctx:
            KeyringSecrets('test', backend='helpers.NoSuchClass')
        self.assertEqual(
            'Unknown backend class: "helpers.NoSuchClass"', str(ctx.exception)
        )

        ks = KeyringSecrets('test', backend='submod.helpers.SubmodBackend')
        # same here
        self.assertEqual('SubmodBackend', ks.backend.__class__.__name__)
        self.assertEqual(
            'submod-octodns-the-secret', ks.fetch('octodns/the-secret', None)
        )

        ks = KeyringSecrets('test', backend='helpers.DummyBackend')
        # not importing and using the class object here so we don't help the
        # code by having everything imported beforhand
        self.assertEqual('DummyBackend', ks.backend.__class__.__name__)
        self.assertEqual(
            'dummy-octodns-the-secret', ks.fetch('octodns/the-secret', None)
        )

        ks = KeyringSecrets('test', backend='helpers.NoneBackend')
        # same here
        self.assertEqual('NoneBackend', ks.backend.__class__.__name__)
        with self.assertRaises(KeyringSecretsException) as ctx:
            ks.fetch('octodns/the-secret', None)
        self.assertEqual(
            'failed to find octodns/the-secret', str(ctx.exception)
        )
