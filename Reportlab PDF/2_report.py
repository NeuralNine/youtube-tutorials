from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

doc = SimpleDocTemplate('report.pdf', pagesiz=A4)
styles = getSampleStyleSheet()

title = Paragraph('Sales Report 2025', styles['Title'])

sales_data = {
    'Alpha': [100, 120, 140, 120],
    'Beta': [70, 60, 60, 50],
    'Gamma': [200, 200, 200, 340]
}

table_data = [
    ['Product', 'Q1', 'Q2', 'Q3', 'Q4'],    
    ['Alpha'] + sales_data['Alpha'],
    ['Beta'] + sales_data['Beta'],
    ['Gamma'] + sales_data['Gamma']
]

table = Table(
    table_data,
    style=[
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1, 0), 'Helvetica-Bold')
    ]
)

chart = Drawing(400, 200)

bar_chart = VerticalBarChart()
bar_chart.data = [sales_data['Alpha'], sales_data['Beta'], sales_data['Gamma']]
bar_chart.categoryAxis.categoryNames = ['Q1', 'Q2', 'Q3', 'Q4']
bar_chart.valueAxis.valueMin = 0
bar_chart.valueAxis.valueMax = max(max(series) * 1.1 for series in bar_chart.data)
bar_chart.valueAxis.valueStep = 50

chart.add(bar_chart)

doc.build([title, Spacer(0, 12), table, chart])
