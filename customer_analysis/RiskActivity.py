import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import seaborn as sns
import os
import matplotlib.font_manager as fm
os.system('cls')
engine = create_engine(
    'postgresql+psycopg://USER:PASSWORD@localhost:5432/bankstrans'
)



query = """
SELECT 
    COALESCE(risk_band, 'undefined') AS risk_band,
    c.customer_id, 
    COUNT(*) AS transaction_count 
FROM customers c
JOIN accounts a
ON a.customer_id = c.customer_id
JOIN transactions t
ON t.account_id = a.account_id
GROUP BY risk_band, c.customer_id

"""

mont_350 = fm.FontProperties(fname='C:/fonts/Montserrat_350', family='Montserrat350')

mont_500 = fm.FontProperties(fname='C:/fonts/Montserrat_500')


fig, ax = plt.subplots(figsize=(18, 9))

rb_customer_count = pd.read_sql(query, engine)


sns.stripplot(data= rb_customer_count, x = 'risk_band', y='transaction_count',edgecolors=None,alpha= 0.3, size=6, c='#133b54', ax=ax)

ax.set_yscale('log')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


plt.yticks(fontproperties=mont_350, fontsize=12)
plt.xticks(fontproperties=mont_350, fontsize=12)

ax.margins(x=0.03)

ax.grid(axis='y', which='major', alpha=0.5)

ax.set_axisbelow(True)

plt.subplots_adjust(left=0.125, bottom=0.076, right=0.9, top=0.83, wspace=0.2, hspace=0.2)

ax.set_xlabel('Risk Band', fontproperties=mont_350, fontsize=15)

ax.set_ylabel(None)

plt.title('Client Activity', fontproperties=mont_500, fontsize=20, x=0.5, y=1)

plt.minorticks_off()

plt.savefig('RiskBandActivity_Analysis', dpi=300)

plt.show()