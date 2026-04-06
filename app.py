import streamlit as st
import pandas as pd
import networkx as nx
import argparse
import sys
from yfiles_graphs_for_streamlit import StreamlitGraphWidget as GraphWidget
from data_source import mock_data, get_databricks_nodes
from utils import condense_graph

# Set page config
st.set_page_config(page_title="Data Lineage Explorer", layout="wide")

st.title("Data Lineage Explorer")

# --- Parse Runtime Arguments ---
# Streamlit allows passing args via -- followed by args.
parser = argparse.ArgumentParser(description="Data Lineage Explorer Arguments")
parser.add_argument("--source", choices=["mock", "databricks"], default="mock", help="Data source type")
parser.add_argument("--table", type=str, help="Databricks table name (required if source is databricks)")
parser.add_argument("--profile_name", type=str, help="Databricks profile name (required if source is databricks)")

# Use a workaround to handle how Streamlit passes arguments.
# args = parser.parse_args(sys.argv[1:]) if you're calling it from a normal python app.
# In Streamlit, it's safer to check sys.argv if it's passed via `streamlit run app.py -- --source=...`.
try:
    # We find where '--' is and only parse what's after it.
    if "--" in sys.argv:
        args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    else:
        # Fallback for when it's not passed via --
        # Streamlit itself might have some args in sys.argv.
        args, unknown = parser.parse_known_args()
except SystemExit:
    # If parsing fails or --help is called, we can provide a default or handle gracefully.
    args = argparse.Namespace(source="mock", table=None, profile_name=None)

source_type = args.source
table_name = args.table
profile_name = args.profile_name

# --- Filters ---
if source_type == "databricks":
    if not table_name or not profile_name:
        st.sidebar.error("Table name and profile name must be specified via --table and --profile_name runtime arguments for Databricks source.")
        st.stop()
    df = get_databricks_nodes(table_name, profile_name)
else:
    df = mock_data()

st.sidebar.header("Filters")

# Top level filter: version_number (using 'version' column)
versions = sorted(df['version'].unique())
selected_version = st.sidebar.selectbox("Select Version (SemVer)", ["All"] + list(versions))

# Secondary filter: allows filtering for multiple columns
st.sidebar.subheader("Additional Filters")
selected_columns = st.sidebar.multiselect("Select columns to filter by", [c for c in df.columns if c != 'version'])

filters = {}
for col in selected_columns:
    unique_vals = sorted(df[col].unique())
    selected_vals = st.sidebar.multiselect(f"Select values for {col}", unique_vals, default=unique_vals)
    filters[col] = selected_vals

st.sidebar.subheader("Graph Settings")
condense_threshold = st.sidebar.slider("Chokepoint Condense Threshold", 500, 20000, 1000)

# Apply Filters
filtered_df = df.copy()
if selected_version != "All":
    filtered_df = filtered_df[filtered_df['version'] == selected_version]

for col, vals in filters.items():
    if vals:
        filtered_df = filtered_df[filtered_df[col].isin(vals)]



st.subheader("Lineage Data Table")
if len(filtered_df) > 5000:
    st.text("data is still too big even after filtering, truncating to make sure UI doesn't break")

st.dataframe(filtered_df)

# --- Visualization ---
st.subheader("Lineage Graph")

if not filtered_df.empty:
    # Create NetworkX graph
    G_raw = nx.DiGraph()
    for _, row in filtered_df.iterrows():
        G_raw.add_edge(row['src'], row['dst'], label=row['job_name'], version=row['version'])

    # Logic to condense chokepoints
    G = condense_graph(G_raw, condense_threshold)

    # Create yFiles GraphWidget
    w = GraphWidget.from_graph(
        G,
        node_label_mapping=lambda node: node['properties']['label'] if 'label' in node['properties'] else node['id'],
        edge_label_mapping=lambda edge: edge['properties']['label'] if 'label' in edge['properties'] else ""
    )
    
    # Use hierarchic layout for data lineage
    w.hierarchic_layout()
    
    # Display the graph
    w.show()
else:
    st.info("No data available for the selected filters.")

st.markdown("---")
st.caption("Simple Data Lineage Mock App")
