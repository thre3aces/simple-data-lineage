import streamlit as st
import pandas as pd

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

@st.cache_data
def get_databricks_nodes(table_name: str) -> pd.DataFrame:
    # This is a placeholder for actual Databricks logic.
    # It returns mock data representing data from a table.
    data = [
        {"src": f"raw_{table_name}", "dst": f"stg_{table_name}", "job_name": f"clean_{table_name}", "version": "1.0.0"},
        {"src": f"stg_{table_name}", "dst": f"fct_{table_name}", "job_name": f"process_{table_name}", "version": "1.0.0"},
    ]
    return pd.DataFrame(data)