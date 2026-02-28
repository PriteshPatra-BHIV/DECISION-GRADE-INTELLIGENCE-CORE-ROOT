import json
from pathlib import Path
from datetime import datetime
import os

MODULE_DIR = Path(__file__).parent
ARCHIVE_FILE = MODULE_DIR / "ambiguity_archive.json"


class AmbiguityArchive:

    def archive(self, previous_state, context_reference):
        if previous_state != "Ambiguous":
            return  # Only archive ambiguity

        entry = {
            "archived_state": previous_state,
            "context_reference": context_reference,
            "archived_at": datetime.utcnow().isoformat()
        }

        if ARCHIVE_FILE.exists():
            with open(ARCHIVE_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(entry)

        with open(ARCHIVE_FILE, "w") as f:
            json.dump(data, f, indent=4)

        return entry


if __name__ == "__main__":
    archive = AmbiguityArchive()
    result = archive.archive(
        previous_state="Ambiguous",
        context_reference="Signal_#789"
    )
    print("Archived:", result)
