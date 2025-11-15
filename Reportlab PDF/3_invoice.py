from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image, TableStyle, XPreformatted

doc = SimpleDocTemplate(
    'invoice.pdf',
    pagesize=A4,
    rightMargin=20*mm,
    leftMargin=20*mm,
    topMargin=20*mm,
    bottomMargin=20*mm
)

styles = getSampleStyleSheet()
story = []

logo_path = 'nn_logo.jpg'
try:
    logo = Image(logo_path, width=35*mm, height=35*mm)
except:
    logo = Paragraph('<b>ACME Corporation</b>', styles['Title'])

company_info = XPreformatted(
    'ACME Corporation\n123 Market Street\nMetropolis, CA 94103\n+1 (555) 123-4567',
    styles['Normal']
)

header = Table([[logo, company_info]], colWidths=[60*mm, 100*mm])
header.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP')
]))

story += [header, Spacer(1, 20)]

story += [Paragraph('<b>INVOICE</b>', styles['Title']), Spacer(1, 10)]

invoice_info = [
    ['Invoice No:', 'INV-2025-074'],
    ['Date:', '2025-11-05'],
    ['Due Date:', '2025-11-20']
]

customer_info = XPreformatted(
    'John Doe\n45 Elm Avenue\nGotham, NY 10001',
    styles['Normal']
)

left = Table(invoice_info, colWidths=[70, 70])
right = Table([[Paragraph('Bill To:', styles['Normal']), customer_info]], colWidths=[50, 120])

info = Table([[left, right]], colWidths=[90*mm, 90*mm])
info.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP')
]))

story += [info, Spacer(1, 80)]

items = [
    ['Description', 'Qty', 'Unit Price', 'Tax', 'Total'],
    ['Web Design Package', 1, '$1,200.00', '10%', '$1,320.00'],
    ['Hosting (12 months)', 1, '$180.00', '10%', '$198.00'],
    ['Domain (1 year)', 1, '$15.00', '0%', '$15.00'],
    ['Maintenance', 2, '$75.00', '10%', '$165.00']
]

table = Table(items, hAlign='LEFT', colWidths=[200, 50, 70, 50, 70])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
]))

story += [table, Spacer(1, 80)]

totals = [
    ['Subtotal:', '$1,560.00'],
    ['Tax (10%):', '$156.00'],
    ['Total Due:', '$1,716.00']
]

totals_table = Table(totals, colWidths=[370, 70], hAlign='RIGHT')
totals_table.setStyle(TableStyle([
    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
]))

story += [totals_table, Spacer(1, 30)]

story.append(Paragraph('<b>Notes:</b>', styles['Heading3']))
notes = (
    'Thank you for your business. Payment is due within 15 days.\n'
    'Please transfer to account #12345678, ACME Corp Bank, SWIFT: ACMEBANK.'
)
story += [XPreformatted(notes, styles['Normal']), Spacer(1, 40)]
story.append(Paragraph('© 2025 ACME Corporation', styles['Normal']))

doc.build(story)

