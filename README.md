# Parishioner Clusters

This project analyzes and clusters parishioner families based on their addresses and proximity.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/parishioner-clusters.git
cd parishioner-clusters
```

### 2. Set Up Python Environment

It is recommended to use a virtual environment.

#### Using `venv` (Standard Library)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Libraries

Install dependencies using `pip`:

```bash
pip3 install -r requirements.txt
```

### 4. Usage

- Place your data files (e.g., `parishioners.csv`) in the project directory data.
- Run analysis scripts as needed:

```bash
# Generate data/parishioner-address.csv
python3 src/cluster_analyzer.py update

# Generate output/address_clusters.html
python3 src/cluster_analyzer.py map

# Generate output/clusters.txt
python3 src/cluster_analyzer.py cluster
```

---

## Project Structure

- `data/parishioners.csv` — Main data file with parishioner addresses.
- `data/parishioner-address.csv` — Processed data with cleansed address and lat lng.
- `cluster_analyzer.py` — analysis script 
- `README.md` — Project instructions.
- `requirements.tx` - list of depenedencies needed 

- `output/address_clusters.html` - Parishioners address clustered on a map (zoom in and out vary the clustering)
- `output/clusters.txt` - For each parishioners address, lists all parishioners within 10 mile radius

---

## License

MIT License (2025)