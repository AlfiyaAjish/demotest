import pandas as pd
from scripts.utils.utils import get_postgres_conn


def upload_to_postgres(df: pd.DataFrame, table_name: str, create_new: bool):
    conn = get_postgres_conn()
    cursor = conn.cursor()

    if create_new:
        cols = ", ".join([f'"{col}" TEXT' for col in df.columns])
        cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        cursor.execute(f'CREATE TABLE "{table_name}" ({cols})')
        conn.commit()

    for _, row in df.iterrows():
        columns = ', '.join([f'"{col}"' for col in df.columns])
        values = ', '.join(['%s'] * len(row))
        sql = f'INSERT INTO "{table_name}" ({columns}) VALUES ({values})'
        cursor.execute(sql, tuple(row.astype(str)))

    conn.commit()
    cursor.close()
    conn.close()
