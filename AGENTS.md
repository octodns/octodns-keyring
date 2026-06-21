# Developer Agent Guide for octoDNS Keyring Secrets Source

This repository contains the Keyring secrets backend module for octoDNS. It allows octoDNS to securely retrieve sensitive credentials (API tokens, passwords) using standard system keyring backends (macOS Keychain, Windows Credential Manager, Secret Service, etc.) instead of plain text environment files.

> [!IMPORTANT]
> **Core Workflow and Guidelines**
>
> All agents working on this repository must read and follow the general instructions and workflow guidelines defined in the core octoDNS `AGENTS.md` file.
> - **Local check**: Look for the file at `../octodns/AGENTS.md`.
> - **Remote check**: If the local file is not available, fetch it from GitHub: [octoDNS Core AGENTS.md](https://github.com/octodns/octodns/raw/refs/heads/main/AGENTS.md).
>
> You must align your code structure, style, pull request guidelines, and overall development workflows with the instructions specified there.

## Repository & Module Information

### Key Components

- **Secrets Class**: [KeyringSecrets](file:///home/ross/octodns/octodns-keyring/octodns_keyring/__init__.py#L24-L89) (defined in [octodns_keyring/__init__.py](file:///home/ross/octodns/octodns-keyring/octodns_keyring/__init__.py)). This class connects system keyring clients to the octoDNS secret manager API.
- **Backend Loader**: The method [_load_backend](file:///home/ross/octodns/octodns-keyring/octodns_keyring/__init__.py#L32-L59) imports and instantiates the keyring backend. It defaults to the system keyring (`keyring.get_keyring()`) but allows configuring custom backend modules dynamically using the `backend` keyword string (e.g. `module.Class`).

### Key Workflows & Features

1. **Keyring Methods**: Implements the standard octoDNS secrets manager API:
   - `set(name, value)`: Stores a secret password under the service name.
   - `fetch(name, source)`: Retrieves a secret. It splits the secret name by `/` into a service name and a key name, queries the backend, and automatically converts digit-only string values into `int` or `float` types where appropriate (falling back to string).
   - `delete(name)`: Removes the secret from the keyring.
2. **Dynamic Routing**: Not supported.
3. **Non-Provider nature**: `KeyringSecrets` is a secrets manager backend, not a DNS sync provider. It does not manage DNS zones, plan changes, or compile DNS records.

## Development & Testing

- **Setup Script**: Run `./script/bootstrap` to create a virtual environment, install dependencies (including `keyring`, `black`, `isort`, `pyflakes`, and `pytest`), and configure pre-commit hooks.
- **Test Suite**: Run unit tests using `pytest` via `./script/test` (or `pytest tests/`). Test files are located in [tests/](file:///home/ross/octodns/octodns-keyring/tests).
- **Code Coverage**: Verify code coverage using `./script/coverage`.

## Key Constraints & Behaviors

- **Python Version**: Targets Python `>=3.9`.
- **Formatting**: Code formatting is enforced via `black` (version `>=26.0.0,<27.0.0`) and `isort`.
