import camelot
import pandas as pd


# Lattice -> looks for clearly defined borders / lines like a grid, visible ruling lines between rows and columns
lattice_tables = camelot.read_pdf('documents/safari.pdf', pages='all', flavor='lattice', suppress_stdout=False)

# Stream -> analyzes text positioning and spaces between text, when structure is maintained through spacing
stream_tables = camelot.read_pdf('documents/safari.pdf', pages='all', flavor='stream', suppress_stdout=False)

    
for table in lattice_tables:
    print('Lattice Table')
    print(table.df)

for table in stream_tables:
    print('Stream Table')
    print(table.df)

