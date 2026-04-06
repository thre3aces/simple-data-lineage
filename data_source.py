import streamlit as st
import pandas as pd
import os
from databricks import sql

@st.cache_data
def mock_data() -> pd.DataFrame:
    data = [
        {"src": "raw_users", "dst": "stg_users", "job_name": "clean_users", "version": "1.0.0"},
        {"src": "raw_orders", "dst": "stg_orders", "job_name": "clean_orders", "version": "1.0.0"},
        {"src": "stg_users", "dst": "fct_orders", "job_name": "join_orders_users", "version": "1.0.0"},
        {"src": "stg_orders", "dst": "fct_orders", "job_name": "join_orders_users", "version": "1.0.0"},
        {"src": "fct_orders", "dst": "dm_sales_monthly", "job_name": "agg_sales", "version": "1.1.0"},
        {"src": "raw_returns", "dst": "stg_returns", "job_name": "clean_returns", "version": "1.1.0"},
        {"src": "stg_returns", "dst": "fct_returns", "job_name": "process_returns", "version": "1.1.0"},
        {"src": "fct_orders", "dst": "dm_returns_analysis", "job_name": "join_returns", "version": "1.2.0"},
        {"src": "fct_returns", "dst": "dm_returns_analysis", "job_name": "join_returns", "version": "1.2.0"},
    ]
    for i in range(100000):
        data.append({"src": "fct_orders", "dst": f"dm_user_{i}", "job_name": "fanout_job", "version": "2.0.0"})
    return pd.DataFrame(data)

@st.cache_resource(ttl=3600)  # Optional: TTL (Time-To-Live) in seconds to refresh stale connections
def get_db_connection(profile_name: str = None):
    return sql.connect(profile=profile_name)


@st.cache_data
def get_databricks_nodes(table_name: str,
                         profile_name: str) -> pd.DataFrame:
    conn = get_db_connection(profile_name=profile_name)
    with conn.cursor() as cursor:
        # Assuming the table has src, dst, job_name, and version columns
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchall()

        # Convert to list of dicts for DataFrame
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in result]
        return pd.DataFrame(data)
