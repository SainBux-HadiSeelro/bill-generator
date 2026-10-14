import os
import datetime
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# ---------------------------------------------------------
# PAGE CONFIGURATION & THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hadi Traders | Smart Invoice & Bill Generator",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .badge-tag {
        background-color: #E0F2FE;
        color: #0369A1;
        font-size: 0.8rem;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# PDF GENERATOR ENGINE
# ---------------------------------------------------------
def generate_pdf(customer_name: str, location: str, subject: str, items: list, transport: float, tax_rate: float) -> str:
    """
    Generates a professional corporate A4 invoice PDF using ReportLab.
    Includes business header, aligned columns, right-aligned monetary values,
    and a clean summary breakdown.
    """
    safe_name = "".join(c for c in customer_name if c.isalnum() or c in (" ", "_", "-")).strip()
    safe_name = safe_name.replace(" ", "_") if safe_name else "Client"
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp_str}_invoice.pdf"

    os.makedirs("invoices", exist_ok=True)
    filepath = os.path.join("invoices", filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    left_margin = 45
    right_margin = width - 45
    y = height - 45

    # Header Bar / Brand Background
    c.setFillColor(colors.HexColor("#1E293B"))  # Slate-800
    c.rect(left_margin, y - 55, right_margin - left_margin, 65, fill=1, stroke=0)

    # Header Text
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(left_margin + 15, y - 5, "HADI TRADERS")

    c.setFont("Helvetica", 8.5)
    c.drawString(left_margin + 15, y - 22, "Complete Office Solutions • Chairs • Executive Desks • Workstations")
    c.drawString(left_margin + 15, y - 36, "New Charlie Trade Centre, 2nd Floor A-208, Near Tecno City Mall, Karachi")

    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(right_margin - 15, y - 10, "INVOICE / BILL")
    c.setFont("Helvetica", 9)
    c.drawRightString(right_margin - 15, y - 26, f"Date: {datetime.date.today().strftime('%d-%b-%Y')}")
    c.drawRightString(right_margin - 15, y - 40, f"Ref: HT-{datetime.datetime.now().strftime('%m%d%H%M')}")

    y -= 80

    # Bill To Box
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.rect(left_margin, y - 50, right_margin - left_margin, 52, fill=1, stroke=1)

    c.setFillColor(colors.HexColor("#0F172A"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin + 12, y - 14, f"Billed To: {customer_name if customer_name else 'Valued Client'}")
    c.setFont("Helvetica", 9.5)
    c.drawString(left_margin + 12, y - 28, f"Site / Delivery Location: {location if location else 'On-site'}")
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(left_margin + 12, y - 42, f"Subject: {subject if subject else 'Commercial Supply Invoice'}")

    y -= 75

    # Table Header
    c.setFillColor(colors.HexColor("#0284C7"))  # Sky-600
    c.rect(left_margin, y - 5, right_margin - left_margin, 20, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin + 8, y, "#")
    c.drawString(left_margin + 30, y, "Item Description")
    c.drawRightString(right_margin - 180, y, "Qty")
    c.drawRightString(right_margin - 95, y, "Unit Rate (PKR)")
    c.drawRightString(right_margin - 10, y, "Total (PKR)")

    y -= 18
    subtotal = 0.0
    c.setFont("Helvetica", 9)

    for idx, (desc, qty, rate) in enumerate(items, start=1):
        line_total = qty * rate
        subtotal += line_total

        # Row alternating background
        if idx % 2 == 0:
            c.setFillColor(colors.HexColor("#F8FAFC"))
            c.rect(left_margin, y - 4, right_margin - left_margin, 16, fill=1, stroke=0)

        c.setFillColor(colors.HexColor("#1E293B"))
        c.drawString(left_margin + 8, y, str(idx))
        display_desc = (desc[:45] + "...") if len(desc) > 48 else (desc if desc else f"Item {idx}")
        c.drawString(left_margin + 30, y, display_desc)
        c.drawRightString(right_margin - 180, y, str(qty))
        c.drawRightString(right_margin - 95, y, f"{rate:,.2f}")
        c.drawRightString(right_margin - 10, y, f"{line_total:,.2f}")

        y -= 17
        if y < 140:
            c.showPage()
            y = height - 50

    # Table bottom divider
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(left_margin, y, right_margin, y)
    y -= 20

    # Summary Section
    tax_amount = ((subtotal + transport) * tax_rate) / 100.0
    grand_total = subtotal + transport + tax_amount

    summary_x = right_margin - 220
    c.setFillColor(colors.HexColor("#334155"))
    c.setFont("Helvetica", 9.5)
    c.drawString(summary_x, y, "Subtotal:")
    c.drawRightString(right_margin - 10, y, f"PKR {subtotal:,.2f}")

    y -= 16
    c.drawString(summary_x, y, "Transport & Handling:")
    c.drawRightString(right_margin - 10, y, f"PKR {transport:,.2f}")

    y -= 16
    c.drawString(summary_x, y, f"Sales Tax ({tax_rate}%):")
    c.drawRightString(right_margin - 10, y, f"PKR {tax_amount:,.2f}")

    y -= 22
    # Total Box
    c.setFillColor(colors.HexColor("#0F172A"))
    c.rect(summary_x - 5, y - 6, (right_margin - summary_x) + 10, 22, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(summary_x, y, "GRAND TOTAL:")
    c.drawRightString(right_margin - 10, y, f"PKR {grand_total:,.2f}")

    # Footer note & stamp
    c.setFillColor(colors.HexColor("#64748B"))
    c.setFont("Helvetica", 8)
    footer_text = f"Computer generated bill • Issued by Hadi Traders • System Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    c.drawString(left_margin, 35, footer_text)
    c.drawRightString(right_margin, 35, "Authorized Signatory")

    c.save()
    return filepath

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & SETTINGS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<span class="badge-tag">ENTERPRISE EDITION</span>', unsafe_allow_html=True)
    st.title("🏢 Hadi Traders")
    st.caption("Office Furniture & Complete Corporate Solutions")
    st.markdown("---")

    st.markdown("### ⚙️ Quick Configuration")
    
    # Pre-load sample data toggle
    load_demo = st.checkbox("📋 Load Sample Corporate Demo", value=False, help="Quickly fill in sample data for demonstration")

    num_items = st.selectbox(
        "Number of line items",
        options=list(range(1, 21)),
        index=2 if load_demo else 0
    )

    st.markdown("---")
    st.markdown("### 📍 Business Address")
    st.info(
        "**Hadi Traders**  \n"
        "New Charlie Trade Centre, 2nd Floor A-208,  \n"
        "Near Tecno City Mall, Karachi, Pakistan  \n"
        "📞 *Direct Sales & Quotations Available*"
    )
    st.markdown("---")
    st.caption("Developed with Streamlit & ReportLab Engine")

# ---------------------------------------------------------
# MAIN INTERFACE
# ---------------------------------------------------------
st.markdown('<div class="main-title">🧾 Commercial Invoice & Bill Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Generate standardized, print-ready corporate PDF invoices with real-time financial auditing.</div>', unsafe_allow_html=True)

# Demo defaults
default_customer = "Muzaffar Ahmed" if load_demo else ""
default_location = "I.I Chundrigar Road, Karachi" if load_demo else ""
default_subject = "BILL FOR OFFICE FURNITURE & EXECUTIVE WORKSTATIONS" if load_demo else "BILL FOR OFFICE FURNITURE"

demo_items = [
    ("Ergonomic High-Back Executive Chair (Mesh Support)", 5, 18500.0),
    ("Modular Workstation Table (4-Person Cluster)", 2, 42000.0),
    ("3-Drawer Steel Mobile Pedestal", 5, 8500.0),
]

col_main, col_summary = st.columns([1.6, 1.0], gap="large")

with col_main:
    st.subheader("1. Client & Project Details")
    c1, c2 = st.columns(2)
    with c1:
        customer_name = st.text_input("Customer / Company Name*", value=default_customer, placeholder="e.g. Muzaffar Ahmed / ABC Ltd")
    with c2:
        location = st.text_input("Site / Delivery Location", value=default_location, placeholder="e.g. Shahrah-e-Faisal, Karachi")

    subject = st.text_input("Bill Subject", value=default_subject, placeholder="e.g. Quotation for Office Renovation")

    st.markdown("---")
    st.subheader("2. Line Items Breakdown")

    items = []
    for i in range(num_items):
        item_desc_default = demo_items[i][0] if load_demo and i < len(demo_items) else ""
        item_qty_default = demo_items[i][1] if load_demo and i < len(demo_items) else 1
        item_rate_default = demo_items[i][2] if load_demo and i < len(demo_items) else 0.0

        with st.expander(f"📦 Item #{i+1}", expanded=True):
            f_col1, f_col2, f_col3 = st.columns([2.5, 1, 1.2])
            with f_col1:
                desc = st.text_input(f"Description #{i+1}", value=item_desc_default, key=f"desc_{i}", placeholder="Item title & specifications")
            with f_col2:
                qty = st.number_input(f"Qty #{i+1}", min_value=1, step=1, value=item_qty_default, key=f"qty_{i}")
            with f_col3:
                rate = st.number_input(f"Unit Rate (PKR) #{i+1}", min_value=0.0, step=500.0, value=item_rate_default, key=f"rate_{i}")
            
            line_cost = qty * rate
            st.caption(f"Line Subtotal: **PKR {line_cost:,.2f}**")
            items.append((desc, qty, rate))

    st.markdown("---")
    st.subheader("3. Surcharges & Taxes")
    c_tax1, c_tax2 = st.columns(2)
    with c_tax1:
        transport = st.number_input("Transport & Freight Charges (PKR)", min_value=0.0, step=500.0, value=3500.0 if load_demo else 0.0)
    with c_tax2:
        tax_rate = st.number_input("Sales Tax Percentage (%)", min_value=0.0, max_value=100.0, step=0.5, value=5.0)

# Calculations for Live Dashboard
subtotal = sum(q * r for _, q, r in items)
tax_val = ((subtotal + transport) * tax_rate) / 100.0
grand_total = subtotal + transport + tax_val

with col_summary:
    st.subheader("📊 Live Billing Summary")
    
    st.markdown(
        f"""
        <div class="metric-card">
            <span style="color: #64748B; font-size: 0.9rem;">Grand Total Payable</span>
            <h2 style="color: #0F172A; margin: 0.2rem 0;">PKR {grand_total:,.2f}</h2>
            <span style="color: #0284C7; font-size: 0.85rem; font-weight: 600;">Includes Tax & Handling</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Subtotal", f"PKR {subtotal:,.2f}")
    with m2:
        st.metric("Transport", f"PKR {transport:,.2f}")

    st.metric(f"Tax ({tax_rate}%)", f"PKR {tax_val:,.2f}")

    st.markdown("---")
    st.markdown("### 🖨️ PDF Invoice Actions")

    if st.button("🚀 Generate PDF Invoice", type="primary", use_container_width=True):
        if not customer_name.strip():
            st.error("⚠️ Please specify a **Customer / Company Name** before generating the invoice.")
        else:
            with st.spinner("Compiling ReportLab vector layout..."):
                pdf_path = generate_pdf(customer_name, location, subject, items, transport, tax_rate)
                st.session_state["generated_pdf"] = pdf_path
            st.success("✅ Professional Invoice Generated Successfully!")

    if "generated_pdf" in st.session_state and os.path.exists(st.session_state["generated_pdf"]):
        generated_file = st.session_state["generated_pdf"]
        with open(generated_file, "rb") as file_bytes:
            st.download_button(
                label="📥 Download PDF Invoice",
                data=file_bytes,
                file_name=os.path.basename(generated_file),
                mime="application/pdf",
                use_container_width=True
            )
        st.caption(f"💾 Saved locally to: `{generated_file}`")
