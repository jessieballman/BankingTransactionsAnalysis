import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
import matplotlib.font_manager as fm
import numpy as np
os.system('cls')
engine = create_engine(
    'postgresql+psycopg://USER:PASSWORD@localhost:5432/bankstrans'
)
query = """
SELECT * FROM transactions
"""

mont_350 = fm.FontProperties(fname='C:/fonts/Montserrat_350')

mont_500 = fm.FontProperties(fname='C:/fonts/Montserrat_500')

colors = [
    '#133b54',
    '#f28c42',
    '#24516b',
    '#c76e36',
    '#315f70',
    '#b85c38',
    '#24445c',
    '#d18a45',
    '#386b78',
    '#a94f35',
    '#19364a',
    '#e5a05b',
]

transactions = pd.read_sql(query, engine, parse_dates=['posted-at'])

trans_type_count = transactions.groupby('transaction_type').agg(count=('transaction_id', 'size')).reset_index()

fig, ax = plt.subplots(figsize=(18, 9))

wedges, _ = plt.pie(
        x=trans_type_count['count'],
        colors=colors,
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        radius=1.3)

values = trans_type_count['count']

labels = trans_type_count['transaction_type'].str.replace('_', ' ').str.title()

for i, wedge in enumerate(wedges):
    angle = (wedge.theta1 + wedge.theta2)/2

    x = np.cos(np.deg2rad(angle))
    y = np.sin(np.deg2rad(angle))

    lable = f'{labels[i]}\n{values[i]/values.sum() *100:.2f}%'

    plt.annotate(lable,
                xy=(x, y),
                xytext=(1.4 * np.sign(x), 1.4 * y),
                ha = 'left' if x>0 else 'right',
                va = 'center',
                arrowprops={'arrowstyle': '-', 'color': '#000000'},
                fontproperties=mont_350
                )


plt.title('Transaction Type Shares', x = -0.5, y = 0.5 ,fontproperties=mont_500, fontsize= 20)

plt.savefig('TransactionTypeShares.png', dpi=300, bbox_inches=None)

plt.show()