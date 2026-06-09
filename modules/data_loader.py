import pandas as pd


def load_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df, None

    except Exception as e:
        return None, str(e)