import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import os

st.set_page_config(page_title="Al Jannat Traders - Invoice Generator", layout="centered")

# ---------------------
# PDF GENERATOR FUNCTION
# ---------------------
def generate_pdf(customer_name, location, subject, items, transport, tax_rate):
    filename = f"{customer_name.replace(' ', '_')}_bill.pdf"
    filepath = os.path.join("invoices", filename)
    os.makedirs("invoices", exist_ok=True)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AL JANNAT TRADERS")
    y -= 20
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "We deal in all kinds of office furniture including Chairs, Tables, Workstations, and Complete Office Solutions")
    y -= 15
    c.drawString(50, y, "New Charlie Trade Centre 2nd Floor A-208, Near Tecno City Mall")

    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"To: {customer_name}")
    y -= 20
    c.drawString(50, y, f"Site Location: {location}")
    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"Subject: {subject}")

    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Description")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Rate")
    c.drawString(400, y, "Total")
    y -= 15
    c.line(50, y, 500, y)

    total_amount = 0
    c.setFont("Helvetica", 10)

    for desc, qty, rate in items:
        line_total = qty * rate
        total_amount += line_total
        y -= 20
        c.drawString(50, y, desc)
        c.drawString(250, y, str(qty))
        c.drawString(300, y, f"{rate:,.0f}")
        c.drawString(400, y, f"{line_total:,.0f}")

    y -= 20
    c.drawString(50, y, "Transport")
    c.drawString(400, y, f"{transport:,.0f}")
    total_amount += transport

    tax = (total_amount * tax_rate) / 100
    grand_total = total_amount + tax

    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "TOTAL AMOUNT:")
    c.drawString(400, y, f"{total_amount:,.0f}")

    y -= 20
    c.drawString(50, y, f"TAX @{tax_rate}%:")
    c.drawString(400, y, f"{tax:,.0f}")

    y -= 20
    c.drawString(50, y, "TOTAL PRICE:")
    c.drawString(400, y, f"{grand_total:,.0f}")

    y -= 40
    c.setFont("Helvetica", 8)
    c.drawString(50, y, f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()
    return filepath


# ---------------------
# STREAMLIT UI
# ---------------------

st.title("🧾 Al Jannat Traders - Bill Generator")

# Controlled via session_state
if "num_items" not in st.session_state:
    st.session_state.num_items = 1

# Use selectbox for smooth reactivity
num_items = st.selectbox("Select number of items", options=list(range(1, 21)), index=st.session_state.num_items - 1)
st.session_state.num_items = num_items

with st.form("bill_form"):
    customer_name = st.text_input("Customer Name")
    location = st.text_input("Site Location")
    subject = st.text_input("Bill Subject", "BILL FOR OFFICE FURNITURE")

    st.markdown("### Add Item Details Below")
    items = []
    for i in range(st.session_state.num_items):
        st.markdown(f"#### Item {i+1}")
        desc = st.text_input(f"Description {i+1}", key=f"desc_{i}")
        qty = st.number_input(f"Quantity {i+1}", min_value=1, step=1, key=f"qty_{i}")
        rate = st.number_input(f"Rate {i+1}", min_value=0.0, step=100.0, key=f"rate_{i}")
        items.append((desc, qty, rate))

    transport = st.number_input("Transport Charges", min_value=0.0, step=100.0)
    tax_rate = st.number_input("Tax %", min_value=0.0, step=0.5, value=5.0)

    submitted = st.form_submit_button("Generate PDF Bill")

if submitted:
    pdf_file = generate_pdf(customer_name, location, subject, items, transport, tax_rate)
    st.success("✅ PDF generated successfully!")
    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download Invoice", f, file_name=pdf_file, mime="application/pdf")
