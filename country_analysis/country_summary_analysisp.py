import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
import matplotlib.font_manager as fm

os.system('cls')
engine = create_engine(
    'postgresql+psycopg://USER:PASSWORD@localhost:5432/bankstrans'
)

mont_350 = fm.FontProperties(fname='C:/fonts/Montserrat_350')

mont_500 = fm.FontProperties(fname='C:/fonts/Montserrat_500')

colors = [
    '#24516b',
    '#c76e36',
    '#56877f',
    '#d5a04f'
]



query = """
WITH summary AS(
    SELECT
        c.country,
        COUNT(DISTINCT branch_id) branch_cnt,
        COUNT(DISTINCT c.customer_id) AS clients_cnt,
        ROUND(AVG(CASE
                WHEN currency = 'USD' THEN amount
                WHEN currency = 'EUR' THEN amount*1.12
                WHEN currency = 'GBP' THEN amount*1.34
            END)::numeric,2) AS avg_amount_usd,
        ROUND(percentile_cont(0.50) WITHIN GROUP (ORDER BY
            CASE
                WHEN currency = 'USD' THEN amount
                WHEN currency = 'EUR' THEN amount*1.12
                WHEN currency = 'GBP' THEN amount*1.34
                END)::numeric,2) AS median_amount_usd,
        COUNT(DISTINCT transaction_id) AS transactions_cnt
    FROM customers c
    JOIN branches b
    ON c.country = b.country
    LEFT JOIN accounts a
    ON a.customer_id = c.customer_id
    LEFT JOIN transactions t
    ON a.account_id = t.account_id
    GROUP BY c.country
),

chn_cnt AS(
    SELECT
        country,
        ROUND((SUM(CASE WHEN channel = 'card' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS card_part,
        ROUND((SUM(CASE WHEN channel = 'online' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS online_part,
        ROUND((SUM(CASE WHEN channel = 'mobile' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS mobile_part,
        ROUND((SUM(CASE WHEN channel = 'branch' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS branch_part,
        ROUND((SUM(CASE WHEN channel = 'atm' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS atm_part
    FROM customers c
    JOIN accounts a
    ON a.customer_id = c.customer_id
    JOIN transactions t
    ON t.account_id = a.account_id
    GROUP BY country
),

risk_part AS(
    SELECT 
        country,
        ROUND(SUM(CASE WHEN risk_band IS NULL THEN 1 ELSE 0 END)/COUNT(*)::numeric*100,2) AS undefined_risk_part,
        ROUND(SUM(CASE WHEN risk_band = 'low' THEN 1 ELSE 0 END)/COUNT(*)::numeric*100,2) AS low_risk_part,
        ROUND(SUM(CASE WHEN risk_band = 'medium' THEN 1 ELSE 0 END)/COUNT(*)::numeric*100,2)AS medium_risk_part,
        ROUND(SUM(CASE WHEN risk_band = 'high' THEN 1 ELSE 0 END)/COUNT(*)::numeric*100,2) AS high_risk_part
    FROM customers
    GROUP BY country
),


trans_cnt AS(
    SELECT
        country,
        ROUND(AVG(cnt),2) AS average_trans_cnt,
        percentile_cont(0.50) WITHIN GROUP (ORDER BY cnt) AS median_trans_cnt
    FROM(
        SELECT
            country,
            c.customer_id,
            COUNT(DISTINCT transaction_id) AS cnt
        FROM customers c
        JOIN accounts a
        ON c.customer_id = a.customer_id
        JOIN transactions t
        ON a.account_id = t.account_id
        GROUP BY country,c.customer_id
    )
    GROUP BY country
)

SELECT 
    s.country,
    branch_cnt,
    clients_cnt,
    transactions_cnt,
    avg_amount_usd,
    median_amount_usd,
    average_trans_cnt,
    median_trans_cnt,
    card_part,
    online_part,
    mobile_part,
    branch_part,
    atm_part,
    undefined_risk_part,
    low_risk_part,
    medium_risk_part,
    high_risk_part
FROM summary s
JOIN chn_cnt cc
ON cc.country = s.country
JOIN risk_part rp
ON rp.country = s.country
JOIN trans_cnt tc
ON tc.country = s.country
"""

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 9))

country_analysis = pd.read_sql(query, engine)

for i in range(3):
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['left'].set_visible(False)
    ax[i].spines['right'].set_visible(False)
    ax[i].grid(axis='y', visible=True, alpha=0.3)
    ax[i].set_axisbelow(True)

ax[0].bar(country_analysis['country'], country_analysis['clients_cnt'], color='#24516b')

ax[1].bar(country_analysis['country'], country_analysis['transactions_cnt'], color='#c76e36')

ax[2].bar(country_analysis['country'], country_analysis['branch_cnt'], color='#e5a05b')

for i in range(3):
    for label in ax[i].get_xticklabels():
        label.set_fontproperties(mont_350)

    for label in ax[i].get_yticklabels():
        label.set_fontproperties(mont_350)


plt.subplots_adjust(left=0.052, right=0.974, bottom=0.11, top=0.88, wspace=0.2, hspace=0.2)


ax[0].set_title('Client Count', fontproperties=mont_350, fontsize=13)

ax[1].set_title('Transactions Count', fontproperties=mont_350, fontsize=13)

ax[2].set_title('Branch Count', fontproperties=mont_350, fontsize=13)

fig.suptitle(
    'Summary Statistics, by Country',
    transform=fig.transFigure,
    x=0.5, 
    y=0.95,
    ha='center',
    va='center',
    fontproperties=mont_500,
    fontsize=20)

plt.text(
    transform=fig.transFigure,
    x=0.5, 
    y=0.05,
    ha='center',
    va='center',
    s=(
    f'Most Popular: {country_analysis["country"].loc[country_analysis['clients_cnt'].idxmax()]}      '
    f'Highest Transactions Count: {country_analysis["country"].loc[country_analysis['transactions_cnt'].idxmax()]}      '
    f'Highest Branch Count: {country_analysis["country"].loc[country_analysis['branch_cnt'].idxmax()]}      '
    ),
    fontproperties=mont_350, 
    fontsize=15)

country_analysis

plt.savefig('CountrySummary_Analysis.png', dpi=300)

plt.show()