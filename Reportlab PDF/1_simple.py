from reportlab.pdfgen import canvas

c = canvas.Canvas('simple.pdf')

c.drawString(100, 750, 'Hello World!')
c.save()

