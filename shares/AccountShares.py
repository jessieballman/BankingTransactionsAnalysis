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
SELECT
    account_type,
    COUNT(*) AS cnt
FROM accounts
GROUP BY account_type
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

account_shares = pd.read_sql(query, engine)


fig, ax = plt.subplots(figsize=(16, 9))

wedges, _ = plt.pie(account_shares['cnt'], startangle=90, colors=colors, radius=1.3,wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})

for i, wedge in enumerate(wedges):

    angle = (wedge.theta1 + wedge.theta2) / 2

    x = np.cos(np.deg2rad(angle))
    y = np.sin(np.deg2rad(angle))

    plt.annotate(
        f"{account_shares['account_type'][i].replace('_', ' ').title()}\n{(account_shares['cnt'][i]/account_shares['cnt'].sum())*100:.2f}%",
        xy=(x, y),
        xytext=(1.5 * np.sign(x), 1.5 * y),
        arrowprops={'arrowstyle': '-', 'color': '#000000'},
        fontproperties=mont_350
    )

plt.title('Account Shares', x=-0.5, y=0.5, fontproperties=mont_500, fontsize=20)

plt.savefig('AccountShares.png', dpi=300, bbox_inches=None)

plt.show()
