import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")

validation_results = []


def log_failure(rule, severity, table, message):
    validation_results.append({
        "rule": rule,
        "severity": severity,
        "table": table,
        "message": message
    })


def dq01_pk_uniqueness(df, table_name):
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        log_failure(
            "DQ-01",
            "CRITICAL",
            table_name,
            f"{duplicates} duplicate rows found"
        )


def dq06_positive_sales(df):
    if "sales" in df.columns:
        invalid = (df["sales"] <= 0).sum()

        if invalid > 0:
            log_failure(
                "DQ-06",
                "WARNING",
                "profitandloss",
                f"{invalid} non-positive sales rows"
            )


def run_validations():

    for file in RAW_PATH.glob("*.xlsx"):

        try:
            df = pd.read_excel(file)

            dq01_pk_uniqueness(
                df,
                file.stem
            )

            dq06_positive_sales(df)

        except Exception as e:

            log_failure(
                "SYSTEM",
                "CRITICAL",
                file.stem,
                str(e)
            )

    pd.DataFrame(
        validation_results
    ).to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print(
        f"Validation complete. "
        f"{len(validation_results)} issues found."
    )


if __name__ == "__main__":
    run_validations()
    