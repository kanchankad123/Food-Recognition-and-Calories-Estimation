import os
import pandas as pd


SUPPORTED_INPUT_EXTS = {".csv", ".xlsx"}


def read_input_file(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext not in SUPPORTED_INPUT_EXTS:
        raise ValueError(f"Unsupported input extension: {ext}. Use .csv or .xlsx")

    if ext == ".csv":
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    return df


def write_output_file(df: pd.DataFrame, path: str) -> None:
    ext = os.path.splitext(path)[1].lower()
    if ext == "":
        # default to csv
        path = f"{path}.csv"
        ext = ".csv"

    if ext == ".csv":
        df.to_csv(path, index=False)
    elif ext == ".xlsx":
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
    else:
        raise ValueError(f"Unsupported output extension: {ext}. Use .csv or .xlsx")
