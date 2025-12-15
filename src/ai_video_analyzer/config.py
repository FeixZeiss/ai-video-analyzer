import os
from pathlib import Path

# ---- Secrets (OAuth) ----
SECRETS_ENV = "AIVA_SECRETS_DIR"
DEFAULT_SECRETS_DIR = "secrets"

TOKEN_FILENAME = "token.json"
CLIENT_SECRET_FILENAME = "client_secret.json"

# ---- Project root (optional) ----
PROJECT_ROOT_ENV = "AIVA_PROJECT_ROOT"

def get_project_root() -> Path:
    """
    Returns the project root. For Option 1 (scripts/ + PYTHONPATH),
    we typically run with cwd = repo root, so Path.cwd() works well.
    You can override by setting AIVA_PROJECT_ROOT.
    """
    env = os.getenv(PROJECT_ROOT_ENV)
    if env:
        return Path(env).resolve()
    return Path.cwd().resolve()


def get_secrets_dir() -> Path:
    """
    Directory containing client_secret.json and token.json.
    Override via AIVA_SECRETS_DIR. Default: <repo>/secrets
    """
    return (get_project_root() / os.getenv(SECRETS_ENV, DEFAULT_SECRETS_DIR)).resolve()


def get_token_path() -> Path:
    return get_secrets_dir() / TOKEN_FILENAME


def get_client_secret_path() -> Path:
    return get_secrets_dir() / CLIENT_SECRET_FILENAME


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def require_file(path: Path, label: str) -> Path:
    if not path.exists():
        raise FileNotFoundError(
            f"{label} not found at: {path}\n"
            f"Fix: create the file or set {SECRETS_ENV} to your secrets folder.\n"
            f"Example (bash): export {SECRETS_ENV}=secrets"
        )
    return path
