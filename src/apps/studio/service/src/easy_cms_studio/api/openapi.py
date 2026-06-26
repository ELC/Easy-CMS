import json
from pathlib import Path

from .app import app_factory


def main() -> None:
    output_path = Path(__file__).resolve().parents[3] / "openapi.json"
    output_path.write_text(
        json.dumps(app_factory().openapi(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
