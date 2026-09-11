from __future__ import annotations

from pathlib import Path

APP_NAME = "University Press Citation Review Workbench"
APP_VERSION = "0.1.0-codex"
HOST = "127.0.0.1"
DEFAULT_PORT = 8765

APP_ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = APP_ROOT / "upress_workbench" / "static"
VENDOR_ROOT = APP_ROOT / "vendor"
DATA_ROOT = APP_ROOT / "data"
DB_PATH = DATA_ROOT / "workbench.sqlite3"

SUPPORTED_EXTENSIONS = {".docx", ".md", ".txt"}
MAX_FILE_BYTES = 20 * 1024 * 1024
MAX_TOTAL_BYTES = 500 * 1024 * 1024
MAX_CHAPTERS = 250
MAX_DOCX_MEMBERS = 10_000
MAX_DOCX_MEMBER_BYTES = 50 * 1024 * 1024
MAX_DOCX_EXPANDED_BYTES = 200 * 1024 * 1024
MAX_MODEL_INPUT_CHARS = 1_200_000
MAX_REQUEST_BYTES = 64 * 1024
MAX_MODEL_CALLS_PER_RUN = 600
MAX_WORKERS = 3
MAX_PROVIDER_RESPONSE_BYTES = 8 * 1024 * 1024
MAX_PROVIDER_EVENT_BYTES = 16 * 1024 * 1024
CODEX_CALL_TIMEOUT_SECONDS = 900
CODEX_STATUS_TIMEOUT_SECONDS = 15
MAX_OUTPUT_SLUG_CHARS = 48
MAX_WINDOWS_OUTPUT_PATH_CHARS = 240
RUN_FOLDER_PREFIX = "UP-Review"

CROSSREF_ENDPOINT = "https://api.crossref.org/works/"
ALLOWED_EGRESS_HOSTS = {"api.crossref.org"}
DEFAULT_BATCH_MODEL = "default"
PROVIDER_NAME = "Codex CLI"

SKILL_PINS = {
    "reference-citation-integrity": "a49e9f686898030684134ba7a7f84ac8b68fc4dc",
    "scholarly-editorial-integrity": "098080247ab21173bbbe3da3ab90aa3cf860e38c",
}

FORMAL_TERMS = {
    "plagiarism": "text-overlap concern",
    "misconduct": "integrity concern",
    "fabrication": "data-reliability concern",
    "falsification": "data-reliability concern",
    "fraud": "integrity concern",
    "bad faith": "intent-related concern",
}


def ensure_runtime_dirs() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
