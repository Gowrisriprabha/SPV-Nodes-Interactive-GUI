# SPV Nodes Interactive GUI

## Overview

The **SPV Nodes Interactive GUI** is a graphical user interface (GUI) for interacting with Simplified Payment Verification (SPV) nodes in a blockchain network. It enables users to query blockchain data efficiently without running a full node, making it lightweight and resource-efficient.

## Features

- **User-friendly GUI** for blockchain interactions
- **Efficient SPV-based queries** without requiring a full blockchain node
- **Blockchain data visualization**
- **Interactive and responsive design**

## Prerequisites

Ensure that you have the following installed on your system:

- Python 3.8 or later
- `pip` (Python package manager)
- `Graphviz` (for visualization)

## Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/your-repository/SPV-Nodes-Interactive-GUI.git
   cd SPV-Nodes-Interactive-GUI
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Ensure Graphviz is installed**

   - Download and install from [Graphviz Official Site](https://graphviz.org/download/).
   - Verify installation:
     ```sh
     dot -V
     ```

## Running the Application

To launch the GUI, execute the following command:

```sh
python frontend.py
```

## Project Structure

```
SPV-Nodes-Interactive-GUI/
│-- frontend.py           # Main GUI script
│-- blockchain_data.json  # Blockchain data storage
│-- requirements.txt      # Required Python dependencies
│-- Procfile              # Deployment configuration
│-- README.md             # Documentation
│-- image.jpg             # UI reference image (if applicable)
└── .git/                 # Version control
```

## Troubleshooting

If you encounter issues, try the following:

- Ensure Python and dependencies are installed properly.
- Check that Graphviz is installed and accessible in your system's PATH.
- Run the script in a virtual environment:
  ```sh
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  python frontend.py
  ```

## Contributors

- [https://github.com/Gowrisriprabha](https://github.com/Gowrisriprabha)
- **https\://github.com/Amodinii**

##
