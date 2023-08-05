from io import BytesIO
from typing import Any
import pandas as pd


def df_to_xlsx(
    df: pd.DataFrame, **kwargs: Any
) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, **kwargs)
    return output.getvalue()