import json
import jsonschema
from pathlib import Path
import sqlite3
import os

CONTRACTS_DIR = Path(__file__).parent
ROOT_DIR = CONTRACTS_DIR.parent

def validate_json(schema_path: Path, data_path: Path):
    print(f"Validating {data_path.name} against {schema_path.name}...")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = json.loads(data_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=data, schema=schema)
    print(f"[OK] {data_path.name} successfully validated!")

def main():
    print("=== Starting Contract Validation Suite ===")

    # 1. Validate Contract A
    validate_json(
        CONTRACTS_DIR / "contract-a-roadmap-discovery.json",
        CONTRACTS_DIR / "contract-a-roadmap-discovery.sample.json"
    )

    # 2. Validate Contract B
    validate_json(
        CONTRACTS_DIR / "contract-b-crawl-state.json",
        CONTRACTS_DIR / "contract-b-crawl-state.sample.json"
    )

    # Validate actual crawl state record if DB exists
    db_path = ROOT_DIR / "crawl_state.db"
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lessons LIMIT 1")
        row = cursor.fetchone()
        if row:
            record = dict(row)
            schema = json.loads((CONTRACTS_DIR / "contract-b-crawl-state.json").read_text(encoding="utf-8"))
            jsonschema.validate(instance=record, schema=schema)
            print("[OK] Actual crawl_state.db record successfully validated against Contract B!")
        conn.close()

    # 3. Validate Contract C
    validate_json(
        CONTRACTS_DIR / "contract-c-raw-lesson.json",
        CONTRACTS_DIR / "contract-c-raw-lesson.sample.json"
    )

    # Validate actual raw lesson json if exists
    raw_lessons_dir = ROOT_DIR / "raw_data" / "lessons"
    if raw_lessons_dir.exists():
        json_files = list(raw_lessons_dir.glob("*.json"))
        if json_files:
            sample_raw = json.loads(json_files[0].read_text(encoding="utf-8"))
            schema = json.loads((CONTRACTS_DIR / "contract-c-raw-lesson.json").read_text(encoding="utf-8"))
            jsonschema.validate(instance=sample_raw, schema=schema)
            print(f"[OK] Actual raw lesson ({json_files[0].name}) successfully validated against Contract C!")

    # 4. Validate Contract E
    validate_json(
        CONTRACTS_DIR / "contract-e-frontend-data.json",
        CONTRACTS_DIR / "contract-e-frontend-data.sample.json"
    )

    # Validate actual frontend roadmap-data.json if exists
    frontend_data_path = ROOT_DIR / "frontend" / "src" / "roadmap-data.json"
    if frontend_data_path.exists():
        frontend_data = json.loads(frontend_data_path.read_text(encoding="utf-8"))
        schema = json.loads((CONTRACTS_DIR / "contract-e-frontend-data.json").read_text(encoding="utf-8"))
        jsonschema.validate(instance=frontend_data, schema=schema)
        print("[OK] Actual frontend/src/roadmap-data.json successfully validated against Contract E!")
        print("-> Frontend and Processor compatibility verified: roadmap-data.json conforms to Contract E.")

    print("\n=== All Contracts Validated Successfully! ===")

if __name__ == "__main__":
    main()
