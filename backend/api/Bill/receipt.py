from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from io import BytesIO


def generate_receipt_pdf(bill):
    width = 80 * mm
    height = 220 * mm
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(width, height))

    y = height - 10 * mm
    center = width / 2

    def line(text, size=7, bold=False, gap=5 * mm):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawCentredString(center, y, text)
        y -= gap

    def divider():
        nonlocal y
        c.setFont("Helvetica", 6)
        c.drawCentredString(center, y, "-" * 48)
        y -= 4 * mm

    def row(left, right, size=7, bold=False):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(5 * mm, y, left)
        c.drawRightString(width - 5 * mm, y, right)
        y -= 4.5 * mm

    # ── Header ──────────────────────────────────────────────
    line("SMART STORE", size=12, bold=True, gap=6 * mm)
    line("Tel: (000) 000 - 0000", size=7)
    line("123 Store Street, City 00000", size=7)
    divider()

    # ── Bill meta ───────────────────────────────────────────
    bill_no  = str(bill.id)[:8].upper()
    cashier  = bill.user.username.upper()
    date_str = bill.bill_date.strftime("%m/%d/%Y")
    time_str = bill.bill_date.strftime("%H:%M")

    c.setFont("Helvetica", 6.5)
    c.drawString(5 * mm, y, f"BILL#  {bill_no}")
    c.drawRightString(width - 5 * mm, y, f"DATE: {date_str}")
    y -= 4 * mm
    c.drawString(5 * mm, y, f"CASHIER: {cashier}")
    c.drawRightString(width - 5 * mm, y, f"TIME: {time_str}")
    y -= 4 * mm

    if bill.customer:
        c.drawString(5 * mm, y, f"CUSTOMER: {bill.customer.name.upper()}")
        y -= 4 * mm

    divider()

    # ── Items header ────────────────────────────────────────
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(5 * mm, y, "ITEM")
    c.drawRightString(width - 5 * mm, y, "AMOUNT")
    y -= 4 * mm
    divider()

    # ── Items ───────────────────────────────────────────────
    for item in bill.items.select_related('product').all():
        name       = item.product.product_name.upper()
        qty        = item.quantity
        unit_price = float(item.price)
        total      = unit_price * qty

        c.setFont("Helvetica", 6.5)
        c.drawString(5 * mm, y, name[:28])
        c.drawRightString(width - 5 * mm, y, f"{total:.2f}")
        y -= 4 * mm

        c.setFont("Helvetica", 6)
        c.drawString(8 * mm, y, f"{qty} x {unit_price:.2f}")
        y -= 4 * mm

    divider()

    # ── Totals ──────────────────────────────────────────────
    subtotal = sum(float(i.price) * i.quantity for i in bill.items.all())
    row("SUBTOTAL", f"{subtotal:.2f}")
    row("TAX (0%)", "0.00")
    row("TOTAL", f"{float(bill.total_amount):.2f}", size=8, bold=True)

    divider()

    # ── Items sold ──────────────────────────────────────────
    total_items = sum(i.quantity for i in bill.items.all())
    line(f"# ITEMS SOLD  {total_items}", size=10, bold=True, gap=6 * mm)

    divider()

    # ── Barcode (reportlab built-in) ────────────────────────
    try:
        barcode_value = str(bill.id).replace("-", "")[:20]
        bc = code128.Code128(barcode_value, barHeight=14 * mm, barWidth=0.6)
        bc_width = bc.width
        x_pos = (width - bc_width) / 2
        bc.drawOn(c, x_pos, y - 14 * mm)
        y -= 18 * mm
    except Exception:
        pass

    divider()

    # ── Footer ──────────────────────────────────────────────
    line("Thank you for shopping with us!", size=6.5, gap=4 * mm)
    line(f"{date_str}   {time_str}", size=6.5, gap=4 * mm)
    line("*** CUSTOMER COPY ***", size=6.5, bold=True)

    c.save()
    buffer.seek(0)
    return buffer
