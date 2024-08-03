import pandas as pd
from pathlib import Path
from ..utils import logger

def load_to_csv(df: pd.DataFrame, destination: str | Path):
    try:
        # Create parent directories if not yet available
        destination.parent.mkdir(parents=True, exist_ok=True)

        # Drop duplicate records
        df = df.drop_duplicates().copy()

        df.to_csv(destination, index=False)
        logger.info(f"{destination} has been saved.")

    # Log any errors; no exceptions will be raised
    except Exception as e:
        logger.error(f"Error occured in saving {destination}. {e}")