# Hadi Traders - Bill & Invoice Generator

A lightweight, streamlined desktop web application built with **Streamlit** and **ReportLab** to generate professional PDF quotation and billing invoices for **Hadi Traders** (Office Furniture & Solutions).

---

## 📌 Features

- **Company Header & Branding**: Automatic inclusion of Hadi Traders business details and address.
- **Client & Job Details**: Fields for Customer Name, Site Location, and Bill Subject.
- **Dynamic Line Items**: Add between 1 and 20 item rows dynamically with Description, Quantity, and Unit Rate.
- **Automatic Calculations**: Real-time line item total, transport charge handling, customizable tax percentage, and grand total.
- **Instant PDF Generation & Download**: Fast A4 PDF document creation with one-click direct browser download.
- **Local Storage Archive**: Automatically saves generated invoices in the `invoices/` directory.

---

## 🛠️ Tech Stack

- **Language**: Python >= 3.12
- **UI Framework**: [Streamlit](https://streamlit.io/)
- **PDF Engine**: [ReportLab](https://www.reportlab.com/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (or standard `pip`)

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.12+** installed on your system.

### Installation

#### Option 1: Using `uv` (Recommended)

1. Clone or open the repository folder:
   ```bash
   cd hadi-traders
   ```

2. Run the application directly with `uv`:
   ```bash
   uv run streamlit run app.py
   ```

#### Option 2: Using standard `pip` and virtual environment

1. Create and activate a virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # OR
   pip install streamlit reportlab
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

The application will start and open automatically in your default browser at `http://localhost:8501`.

---

## 📁 Project Structure

```text
hadi-traders/
├── app.py             # Main Streamlit application and PDF generator
├── pyproject.toml     # Project metadata and dependencies
├── requirements.txt   # Dependencies for cloud deployment
├── uv.lock            # Locked dependency tree (uv)
├── .python-version    # Target Python version (3.12)
├── invoices/          # Directory where generated PDF bills are saved
├── README.md          # Project documentation
└── SPECS.md           # System and technical specification document
```

---

## 📝 Usage Guide

1. **Select Number of Items**: Choose the number of items (1 to 20) from the dropdown.
2. **Fill Customer Details**:
   - Customer Name (e.g., `Muzaffar Ahmed`)
   - Site Location (e.g., `I.I Chundrigar Road, Karachi`)
   - Bill Subject (default: `BILL FOR OFFICE FURNITURE`)
3. **Enter Item Lines**: Enter description, quantity, and unit rate for each item.
4. **Transport & Tax**: Add transport charges (if applicable) and adjust tax percentage.
5. **Generate & Download**: Click **Generate PDF Bill**, preview confirmation, and click **Download Invoice**.

---

## 📄 License

Internal utility for **Hadi Traders**. All rights reserved.
