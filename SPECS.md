# System & Technical Specifications: Hadi Traders Bill Generator

**Document Version:** 1.0.0  
**Project:** Hadi Traders - Invoice & Bill Generator  
**Status:** Implemented (Active)  
**Primary Target File:** `app.py`  

---

## 1. Executive Summary & Purpose

The **Hadi Traders Bill Generator** is an internal business tool designed to generate standardized commercial invoices/bills for office furniture sales and installations. The system replaces manual invoice formatting with an automated, reactive web interface that compiles entries into printable A4-sized PDF documents with automated price, transport, and taxation calculations.

---

## 2. System Architecture

The application is structured as a single-tier lightweight desktop web app:

```
[ User Browser / Streamlit Frontend ]
                │
                ▼ (Form Submission)
[ Business Logic & Calculation Layer ]
                │
                ▼
[ PDF Engine (ReportLab Canvas) ] ──▶ [ Local Storage (invoices/*.pdf) ]
                │
                ▼
[ Browser Download Stream ]
```

### 2.1 Technology Stack & Versions
- **Language Runtime:** Python 3.12+
- **Application Framework:** Streamlit (`>=1.46.1`)
- **PDF Generation Library:** ReportLab (`>=4.4.2`)
- **Package & Dependency Management:** `uv` (`pyproject.toml`, `uv.lock`)
- **Target Page Format:** Standard ISO 216 A4 (595.27 x 841.89 points)

---

## 3. Functional Specifications

### 3.1 Input Parameters & Form Controls

| Field Name | Type | UI Component | Default Value | Validation / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `num_items` | Integer | `st.selectbox` | `1` | Options: 1 to 20 |
| `customer_name` | String | `st.text_input` | Empty string | Plain text; spaces converted to `_` in filename |
| `location` | String | `st.text_input` | Empty string | Delivery / site installation address |
| `subject` | String | `st.text_input` | `"BILL FOR OFFICE FURNITURE"` | Title/subject of bill |
| `desc_{i}` | String | `st.text_input` | Empty string | Description of furniture item |
| `qty_{i}` | Integer | `st.number_input` | `1` | Min: `1`, Step: `1` |
| `rate_{i}` | Float | `st.number_input` | `0.0` | Min: `0.0`, Step: `100.0` |
| `transport` | Float | `st.number_input` | `0.0` | Min: `0.0`, Step: `100.0` |
| `tax_rate` | Float | `st.number_input` | `5.0` | Min: `0.0`, Step: `0.5` |

---

## 4. Calculation & Business Rules

### 4.1 Formulas

1. **Line Total:**
   $$\text{Line Total}_i = \text{qty}_i \times \text{rate}_i$$

2. **Items Subtotal:**
   $$\text{Items Subtotal} = \sum_{i=1}^{N} \text{Line Total}_i$$

3. **Subtotal With Transport:**
   $$\text{Subtotal} = \text{Items Subtotal} + \text{transport}$$

4. **Tax Calculation:**
   $$\text{Tax Amount} = \frac{\text{Subtotal} \times \text{tax\_rate}}{100}$$

5. **Grand Total:**
   $$\text{Grand Total} = \text{Subtotal} + \text{Tax Amount}$$

### 4.2 Formatting
- Currency amounts are rounded and displayed with thousand separators without fractional decimals: `{:,.0f}` (e.g. `15,000`, `1,250,000`).

---

## 5. PDF Layout & Design Specification

### 5.1 Document Dimensions & Coordinates
- **Page Size:** A4 (`595.27 pt` width $\times$ `841.89 pt` height).
- **Coordinate System:** Origin `(0, 0)` is bottom-left corner.
- **Top Margin Anchor:** Starts at $y = \text{height} - 50$ ($791.89\text{ pt}$).
- **Left Margin:** $X = 50\text{ pt}$.

### 5.2 Header Section
- **Company Name:** Font `Helvetica-Bold`, size `16pt`. Output: `HADI TRADERS`
- **Sub-tagline:** Font `Helvetica`, size `9pt`. Output: `"We deal in all kinds of office furniture including Chairs, Tables, Workstations, and Complete Office Solutions"`
- **Physical Address:** Font `Helvetica`, size `9pt`. Output: `"New Charlie Trade Centre 2nd Floor A-208, Near Tecno City Mall"`

### 5.3 Customer & Site Section
- **Recipient:** `To: {customer_name}` (Font `Helvetica-Bold`, `12pt`)
- **Site Location:** `Site Location: {location}` (Font `Helvetica-Bold`, `12pt`)
- **Subject:** `Subject: {subject}` (Font `Helvetica-Bold`, `11pt`)

### 5.4 Items Table Grid
- **Columns:**
  - `Description`: $X = 50\text{ pt}$
  - `Qty`: $X = 250\text{ pt}$
  - `Rate`: $X = 300\text{ pt}$
  - `Total`: $X = 400\text{ pt}$
- **Divider Line:** Drawn from $(50, y)$ to $(500, y)$ with stroke width 1.
- **Item Rows:** Decrement $y$ by $20\text{ pt}$ per row in `Helvetica`, `10pt`.

### 5.5 Summary & Totals
- `Transport`: Decrement $y$ by $20\text{ pt}$, value at $X=400\text{ pt}$.
- `TOTAL AMOUNT:`: Font `Helvetica-Bold`, `10pt`.
- `TAX @{tax_rate}%:`: Font `Helvetica-Bold`, `10pt`.
- `TOTAL PRICE:`: Font `Helvetica-Bold`, `10pt`.
- **Timestamp Footer:** Font `Helvetica`, `8pt`, formatted as `YYYY-MM-DD HH:MM:SS`.

---

## 6. Storage & File Management

- **Directory:** `./invoices/` (auto-created via `os.makedirs("invoices", exist_ok=True)`).
- **Naming Convention:** `{customer_name.replace(' ', '_')}_bill.pdf` (e.g. `Muzaffar_Ahmed_bill.pdf`).
- **Download Action:** Served via standard MIME type `application/pdf` via Streamlit's `st.download_button`.

---

## 7. Known Edge Cases & Recommended Future Enhancements

| Issue / Limitation | Current Behavior | Recommended Enhancement |
| :--- | :--- | :--- |
| **Page Overflow** | Fixed single page canvas; choosing 15–20 items may overflow off the bottom edge. | Migrate from raw `canvas` to ReportLab `Platypus` (`SimpleDocTemplate`, `Table`, `Paragraph`) for automatic multi-page pagination. |
| **Special Characters in Filename** | Names with `/`, `\`, `:`, `?` can cause file write errors on Windows/Linux. | Sanitize filename using regex before passing to `os.path.join`. |
| **Download Path Display** | Download button uses full path string for `file_name`. | Wrap with `os.path.basename(filepath)` for clean browser downloads. |
| **Data Persistence** | Invoices are only saved as PDFs on disk, no historical ledger or database. | Optional SQLite database for saving invoices, search, and invoice re-printing. |
| **Invoice Numbering** | No unique invoice ID / sequential numbering (e.g., `AJT-2026-001`). | Auto-incrementing invoice number sequence. |
