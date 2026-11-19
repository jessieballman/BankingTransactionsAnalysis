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
    c.customer_id, 
    ROUND(AVG(CASE
        WHEN currency = 'USD' THEN amount
        WHEN currency = 'EUR' THEN amount*1.12
        WHEN currency = 'GBP' THEN amount*1.34
    END),2) AS mean_amount,
    COUNT(*) AS transaction_count 
FROM customers c
JOIN accounts a
ON a.customer_id = c.customer_id
JOIN transactions t
ON t.account_id = a.account_id
GROUP BY c.customer_id
"""

mont_350 = fm.FontProperties(fname='C:/fonts/Montserrat_350', family='Montserrat350')

mont_500 = fm.FontProperties(fname='C:/fonts/Montserrat_500')


fig, ax = plt.subplots(figsize=(18, 9))

ma_customer_count = pd.read_sql(query, engine)


ax.scatter(x = ma_customer_count['mean_amount'], y=ma_customer_count['transaction_count'], marker='o',edgecolors=None,alpha= 0.3, s=30, c='#133b54')

ax.set_yscale('log')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


for tup in ma_customer_count[ma_customer_count['transaction_count'] > 10**4].itertuples():
    ax.annotate(
            f'Customer Id: {tup.customer_id}\nTransaction Count: {tup.transaction_count}',
            xy=(tup.mean_amount, tup.transaction_count),
            xytext=(tup.mean_amount + 10, 0.9 * tup.transaction_count if tup.customer_id == 3 else 1.2 * tup.transaction_count),
            arrowprops={'arrowstyle': '-', 'linewidth': 0.4},
            fontproperties = mont_350
                )

plt.yticks(fontproperties=mont_350, fontsize=12)
plt.xticks(fontproperties=mont_350, fontsize=12)

ax.margins(x=0.03)

ax.grid(axis='y', which='major', alpha=0.5)

ax.set_axisbelow(True)

plt.subplots_adjust(left=0.125, bottom=0.076, right=0.9, top=0.83, wspace=0.2, hspace=0.2)

plt.title('Client Activity', fontproperties=mont_500, fontsize=20, x=0.5, y=1)

plt.minorticks_off()

ax.set_xticklabels([label.get_text() + '$' for label in ax.get_xticklabels()])

plt.xlabel('Mean Amount', fontproperties=mont_350, fontsize=15)

plt.savefig('AmountActivity_Analysis', dpi=300)

plt.show()

