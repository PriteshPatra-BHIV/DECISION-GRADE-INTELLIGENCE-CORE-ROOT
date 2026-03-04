import os

# Root folder
ROOT = "dgic"
PHASE = "phase-epistemic-constitution"

# Folder structure
structure = {
    "day-1": [
        "epistemic_authority_constitution.md",
        "non_authority_inheritance_spec.md",
        "schema_versioning_rules.md",
        "version_mismatch_policy.md"
    ],
    "day-2": [
        "envelope_hashing_spec.md",
        "collapse_escalation_barrier.md",
        "collapse_integrity_proof.md"
    ],
    "day-3": [
        "cross_layer_replay_spec.md",
        "replay_bridge_proof.md",
        "contamination_scenarios.md",
        "boundary_integrity_report.md",
        "SOVEREIGN_EPISTEMIC_CONSTITUTION.md",
        "integration_consumption_guide_enforcement.md",
        "integration_consumption_guide_core.md",
        "FINAL_HANDOVER_EPISTEMIC_PHASE.md"
    ],
    "schema": [
        "epistemic_envelope_schema_v1.json",
        "replay_ledger_format.json"
    ],
    "matrix": [
        "epistemic_capability_matrix.json",
        "privilege_escalation_matrix.md"
    ],
    "tests/mutation_detection_tests": [
        "test_envelope_mutation.py"
    ],
    "tests/collapse_escalation_tests": [
        "test_illegal_collapse.py"
    ],
    "reports": [
        "day1_summary.md",
        "day2_summary.md",
        "day3_summary.md"
    ]
}


def create_structure():
    base_path = os.path.join(ROOT, PHASE)

    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)

        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")

        for file in files:
            file_path = os.path.join(folder_path, file)

            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write(f"# {file}\n")
                print(f"Created file: {file_path}")

    print("\n✅ Constitutional phase structure created successfully.")


if __name__ == "__main__":
    create_structure()