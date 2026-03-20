import pandas as pd
from pathlib import Path

AUDIT_PATH = Path("data/AuditLog.xlsx")

def loadLog() -> pd.DataFrame:
    if(AUDIT_PATH.exists()):
        df = pd.read_excel(
            AUDIT_PATH,
            engine="openpyxl"
        )
        return df
        
    return None

