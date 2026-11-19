import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
import matplotlib.font_manager as fm
os.system('cls')
engine = create_engine(
    'postgresql+psycopg://USER:PASSWORD@localhost:5432/bankstrans'
)



query = """
SELECT 
    customer_id,
    COUNT(transaction_id) AS transaction_count
FROM accounts a
JOIN transactions t
ON t.account_id = a.account_id
GROUP BY customer_id
ORDER BY transaction_count DESC
"""

mont_350 = fm.FontProperties(fname='C:/fonts/Montserrat_350')

mont_500 = fm.FontProperties(fname='C:/fonts/Montserrat_500')


fig, ax = plt.subplots(figsize=(18, 9))

customer_activity = pd.read_sql(query, engine)



ax.scatter(x = customer_activity['customer_id'], y=customer_activity['transaction_count'], marker='o',edgecolors=None,alpha= 0.3, s=30, c='#133b54')

ax.set_yscale('log')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


for tup in customer_activity[customer_activity['transaction_count'] > 10**4].itertuples():
    ax.annotate(
            f'Customer Id: {tup.customer_id}\nTransaction Count: {tup.transaction_count}',
            xy=(tup.customer_id, tup.transaction_count),
            xytext=(500 + tup.customer_id,  0.7 * tup.transaction_count if tup.customer_id == 3 else tup.transaction_count),
            arrowprops={'arrowstyle': '-', 'linewidth': 0.4},
            fontproperties = mont_350
                )

plt.yticks(fontproperties=mont_350, fontsize=12)
plt.xticks(fontproperties=mont_350, fontsize=12)

ax.margins(x=0.03)

ax.grid(axis='y', which='major', alpha=0.5)

ax.set_axisbelow(True)

plt.subplots_adjust(left=0.125, bottom=0.055, right=0.9, top=0.83, wspace=0.2, hspace=0.2)

plt.title('Client Activity', fontproperties=mont_500, fontsize=20, x=0.5, y=1)

plt.minorticks_off()

plt.savefig('CustomerActivity_Analysis', dpi=300)

plt.show()