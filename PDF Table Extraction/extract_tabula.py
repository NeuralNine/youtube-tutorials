import tabula
import pandas as pd

tables = tabula.read_pdf(
    'documents/safari.pdf',
    pages='all',
    multiple_tables=True,
    lattice=True,      # For tables with borders
    stream=True,       # For tables without borders
    guess=False,
    pandas_options={'header': None},
)

for i, table in enumerate(tables, 1):
    print(table)
            
