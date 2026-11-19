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

query = """
SELECT transaction_id, COALESCE(category, 'non_merchant') AS category FROM transactions t
LEFT JOIN merchants m
ON t.merchant_id = m.merchant_id
"""

fig, ax = plt.subplots(figsize=(16, 9))

trans_category = pd.read_sql(query, engine)

category_count = trans_category.groupby('category').agg(count=('transaction_id', 'size')).reset_index()

print(category_count)

wedges, _ =ax.pie(category_count['count'], startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}, colors=colors, radius=1.5)

for i, wedge in enumerate(wedges):
    angle = (wedge.theta1+wedge.theta2)/2

    x = np.cos(np.deg2rad(angle))
    y = np.sin(np.deg2rad(angle))

    ax.annotate(
        f'{category_count['category'].iloc[i].replace('_', ' ').title()}\n{category_count['count'].iloc[i]/category_count['count'].sum()*100:.2f}%',
        xy=(x, y),
        xytext=((1.2 if category_count['category'].iloc[i] in ['clothing', 'utilities'] else 1.5) * np.sign(x), 1.55 * y),
        ha = 'left' if x > 0 else 'right',
        va = 'center',
        fontproperties=mont_350,
        arrowprops={'arrowstyle': '-', 'color': '#000000'}
        )

plt.title('Category Shares', x=-0.5, y=0.5, fontproperties=mont_500, fontsize=20)

plt.text( x=-2.95, y=-1.5, s='"Non Merchant" mean transactions like: withdrawal, transfer_in/out etc.', fontproperties=mont_350, fontsize=10)

plt.savefig('CategoryShares.png', dpi=300, bbox_inches=None)

plt.show()
