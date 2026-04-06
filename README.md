# Data Lineage Explorer

A simple Streamlit application for examining and visualizing data lineage. It displays data flow between source and destination tables as an interactive graph and a filterable data table.

## Features

- **Interactive Lineage Graph**: Uses `yfiles-graphs-for-streamlit` to visualize the data flow.
- **Advanced Filtering**:
  - Top-level filter for data version (SemVer).
  - Multi-column filtering for source, destination, and job names.
- **Graph Condensation**: Automatically groups large numbers of child nodes at "chokepoints" to keep the visualization manageable. The threshold is adjustable via the sidebar.
- **Multiple Data Sources**: Support for both mock data and Databricks table sources.
- **Data Table View**: View the raw filtered data in a responsive table.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd simple-data-lineage
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

The app supports runtime arguments to specify the data source.

### Option 1: Mock Data (Default)
To run the app with the built-in mock dataset:
```bash
streamlit run app.py
```
Or explicitly:
```bash
streamlit run app.py -- --source mock
```

### Option 2: Databricks Source
To run the app with a Databricks source, you must provide a table name:
```bash
streamlit run app.py -- --source databricks --table my_lineage_table
```

## Testing

The project includes unit tests for the graph condensation logic. To run the tests:

```bash
python3 -m unittest tests/test_utils.py
```

## Project Structure

- `app.py`: Main Streamlit application.
- `data_source.py`: Logic for fetching/generating data (Mock or Databricks).
- `utils.py`: Graph processing and condensation utilities.
- `tests/`: Unit tests for the application logic.
- `requirements.txt`: Python package dependencies.
