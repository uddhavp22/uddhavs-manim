"""Executable claims ledger for the values shown in the LeNEPA segment."""

MAIN = {
    "D": 192,
    "d": 64,
    "lambda_pred": 1,
    "lambda_time": 20,
    "time_layers": (0, 8),
    "updates": 20_000,
    "seeds": 5,
}

RESULTS = {
    "ptbxl": {"jepa_auroc": 0.892, "jepa_auprc": 0.298,
              "lenepa_auroc": 0.880, "lenepa_auprc": 0.285},
    "diag": {"jepa_auroc": 0.880, "jepa_auprc": 0.597,
             "lenepa_auroc": 0.920, "lenepa_auprc": 0.650},
    "ucr": {"lenepa": 77.65, "mantis": 78.81,
            "moment": 77.89, "nutime": 77.32},
}


def validate() -> None:
    assert MAIN["D"] > MAIN["d"] > 0
    assert MAIN["time_layers"] == (0, 8)
    assert MAIN["seeds"] == 5
    assert RESULTS["ptbxl"]["jepa_auroc"] > RESULTS["ptbxl"]["lenepa_auroc"]
    assert RESULTS["diag"]["lenepa_auroc"] > RESULTS["diag"]["jepa_auroc"]
    assert RESULTS["diag"]["lenepa_auprc"] > RESULTS["diag"]["jepa_auprc"]
    assert RESULTS["ucr"]["mantis"] > RESULTS["ucr"]["lenepa"]
    assert RESULTS["ucr"]["moment"] > RESULTS["ucr"]["lenepa"]
    assert RESULTS["ucr"]["lenepa"] > RESULTS["ucr"]["nutime"]


if __name__ == "__main__":
    validate()
    print("facts: all LeNEPA claims are internally consistent")

