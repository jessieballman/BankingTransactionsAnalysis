import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from sqlalchemy import create_engine
import os
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap

os.system('cls')
engine = create_engine(
    'postgresql+psycopg://USER:PASSWORD@localhost:5432/bankstrans'
)


colors = [
    '#133b54',
    '#19364a',
    '#24445c',
    '#386b78',
    '#e8e2d4',
    '#e5a05b',
    '#d18a45',
    '#c76e36',
    '#a94f35'
]

cmap = LinearSegmentedColormap.from_list('bank_heatmap', colors, N=256)

query = """
WITH cnt_trans AS(
    SELECT
        COALESCE(risk_band, 'undefined') AS risk_band,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'atm_withdrawal')::numeric/COUNT(*)::numeric) AS atm_withdrawal_part,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'card_payment')::numeric/COUNT(*)::numeric) AS card_payment_part,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'direct_debit')::numeric/COUNT(*)::numeric) AS direct_debit_part,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'fee')::numeric/COUNT(*)::numeric) AS fee_part,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'interest')::numeric/COUNT(*)::numeric) AS interest_part,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'refund')::numeric/COUNT(*)::numeric) AS refund_part,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'salary')::numeric/COUNT(*)::numeric) AS salary_part,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'transfer_in')::numeric/COUNT(*)::numeric) AS transfer_in_part,
        (COUNT(transaction_id) FILTER (WHERE transaction_type = 'transfer_out')::numeric/COUNT(*)::numeric) AS transfer_out_part
    FROM customers c
    JOIN accounts a
    ON a.customer_id = c.customer_id
    JOIN transactions t
    ON t.account_id = a.account_id
    GROUP BY risk_band
    ),
dir_cnt AS(
    SELECT 
        COALESCE(risk_band, 'undefined') AS risk_band,
        (COUNT(transaction_id) FILTER (WHERE direction = 'credit')::numeric/COUNT(*)::numeric) AS credit_part,
        (COUNT(transaction_id) FILTER (WHERE direction = 'debit')::numeric/COUNT(*)::numeric) AS debit_part
    FROM customers c
    JOIN accounts a
    ON a.customer_id = c.customer_id
    JOIN transactions t
    ON t.account_id = a.account_id
    GROUP BY risk_band
    )
,
chn_cnt AS(
    SELECT
        COALESCE(risk_band, 'undefined') AS risk_band,
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
    GROUP BY risk_band
),

avg_amount AS(
    SELECT 
    COALESCE(risk_band, 'undefined') AS risk_band,
    AVG(CASE
        WHEN currency = 'USD' THEN amount
        WHEN currency = 'EUR' THEN amount*1.12
        WHEN currency = 'GBP' THEN amount*1.34
        END) AS avg_amount_usd,
    percentile_cont(0.50) WITHIN GROUP (ORDER BY 
    CASE
        WHEN currency = 'USD' THEN amount
        WHEN currency = 'EUR' THEN amount*1.12
        WHEN currency = 'GBP' THEN amount*1.34
    END) AS median_amount_usd
FROM customers c
JOIN accounts a
ON a.customer_id = c.customer_id
JOIN transactions t
ON t.account_id = a.account_id
GROUP BY risk_band
),

avg_acc AS(
    SELECT 
        COALESCE(risk_band,'undefined') AS risk_band,
        AVG(account_count) AS average_account_quantity
    FROM(
        SELECT 
            customer_id, 
            COUNT(account_id) AS account_count 
        FROM accounts
        GROUP BY customer_id
    ) AS acc
    JOIN customers c
    ON acc.customer_id = c.customer_id
    GROUP BY risk_band
),

avg_window AS(
    SELECT risk_band, (AVG(wind)::integer * INTERVAL '1 second') AS avg_window FROM(
        SELECT 
            COALESCE(risk_band, 'undefined') AS risk_band, 
            EXTRACT(EPOCH FROM(posted_at  - LAG(posted_at) OVER(PARTITION BY a.customer_id ORDER BY posted_at))) AS wind
        FROM transactions t
        JOIN accounts a
        ON a.account_id = t.account_id
        JOIN customers c
        ON c.customer_id = a.customer_id
    ) AS win
    GROUP BY risk_band
),

proportions AS(
    SELECT 
        COALESCE(risk_band, 'undefined') AS risk_band,
        (SUM(CASE WHEN category IS NULL THEN 1.0 ELSE 0.0 END)/(SUM(CASE WHEN category IS NOT NULL THEN 1.0 ELSE 0.0 END))*1.0) AS non_merchant_to_merchant,
        (SUM(CASE WHEN EXTRACT(HOUR FROM (posted_at AT TIME ZONE timezone)) BETWEEN 0 AND 6 THEN 1.0 ELSE 0.0 END)/(COUNT(*))*1.0) AS night_proportion
    FROM customers c
    JOIN accounts a
    ON c.customer_id = a.customer_id
    JOIN transactions t
    ON a.account_id = t.account_id
    LEFT JOIN merchants m
    ON m.merchant_id = t.merchant_id
    JOIN timezones tz
    ON tz.city = c.city AND tz.country = c.country
    GROUP BY risk_band
),
per_day AS(
    SELECT risk_band, AVG(cnt_per_day) AS avg_trans_per_day FROM(
        SELECT 
            c.customer_id,
            COALESCE(risk_band, 'undefined') AS risk_band,
            DATE_TRUNC('day', t.posted_at AT TIME ZONE timezone) AS posted_at,
            COUNT(*) AS cnt_per_day
        FROM customers c
        JOIN accounts a
        ON c.customer_id = a.customer_id
        JOIN transactions t
        ON a.account_id = t.account_id
        LEFT JOIN merchants m
        ON m.merchant_id = t.merchant_id
        JOIN timezones tt
        ON tt.country = c.country AND tt.city = c.city
        GROUP BY c.customer_id, DATE_TRUNC('day', t.posted_at AT TIME ZONE timezone)
    )
    GROUP BY risk_band
),

acc_type_part AS(
    SELECT
        COALESCE(risk_band,'undefined') AS risk_band,
        ROUND((COUNT(account_id) FILTER(WHERE account_type = 'loan'))::numeric/COUNT(account_id)*100,2) AS loan_part,
        ROUND((COUNT(account_id) FILTER(WHERE account_type = 'current'))::numeric/COUNT(account_id)*100,2) AS current_part,
        ROUND((COUNT(account_id) FILTER(WHERE account_type = 'credit_card'))::numeric/COUNT(account_id)*100,2) AS credit_card_part,
        ROUND((COUNT(account_id) FILTER(WHERE account_type = 'savings'))::numeric/COUNT(account_id)*100,2) AS savings_part
    FROM customers c
    JOIN accounts a
    ON a.customer_id = c.customer_id
    GROUP BY risk_band
)

SELECT 
    aa.risk_band, 
    ROUND(avg_amount_usd,2) AS avg_amount_usd,
    ROUND(median_amount_usd::numeric,2) AS median_amount_usd,
    ROUND(card_part, 2) AS card_part,
    ROUND(online_part, 2) AS online_part,
    ROUND(mobile_part,2) AS mobile_part,
    ROUND(branch_part,2) AS branch_part,
    ROUND(atm_part,2) AS atm_part,
    ROUND(atm_withdrawal_part*100,2) AS atm_withdrawal_part,
    ROUND(card_payment_part*100,2) AS card_payment_part,
    ROUND(direct_debit_part*100,2) AS direct_debit_part,
    ROUND(fee_part*100,2) AS fee_part,
    ROUND(interest_part*100,2) AS interest_part,
    ROUND(refund_part*100,2) AS refund_part,
    ROUND(salary_part*100,2) AS salary_part,
    ROUND(transfer_in_part*100,2) AS transfer_in_part,
    ROUND(transfer_out_part*100,2) AS transfer_out_part,
    ROUND(debit_part*100,2) AS debit_part,
    ROUND(credit_part*100,2) AS credit_part,
    ROUND(average_account_quantity,2) AS average_account_quantity,
    avg_window,
    ROUND(non_merchant_to_merchant*100,2) AS non_merchant_to_merchant,
    ROUND(night_proportion*100, 2) AS night_proportion,
    ROUND(avg_trans_per_day, 2) AS avg_trans_per_day,
    loan_part,
    current_part,
    savings_part,
    credit_card_part
FROM avg_amount aa 
LEFT JOIN chn_cnt cc
ON aa.risk_band = cc.risk_band
LEFT JOIN dir_cnt md
ON aa.risk_band = md.risk_band
LEFT JOIN  cnt_trans mt
ON aa.risk_band = mt.risk_band 
LEFT JOIN avg_acc ac
ON aa.risk_band = ac.risk_band
LEFT JOIN avg_window aw
ON aw.risk_band = aa.risk_band
LEFT JOIN proportions p
ON p.risk_band = aa.risk_band
LEFT JOIN per_day pd
ON pd.risk_band = aa.risk_band
LEFT JOIN acc_type_part atp
ON atp.risk_band = aa.risk_band
"""

mont_350 = fm.FontProperties(fname='C:/fonts/Montserrat_350')

mont_500 = fm.FontProperties(fname='C:/fonts/Montserrat_500')

risk_band_analysis = pd.read_sql(query, engine)

risk_band_analysis.sort_values(by='risk_band', inplace=True)

risk_band_analysis.set_index('risk_band',inplace=True)

risk_band_zscore = risk_band_analysis.copy()

risk_band_analysis['avg_window'] = (round(risk_band_analysis['avg_window'].dt.total_seconds()/3600,2)).astype(str) + 'h'

risk_band_zscore['avg_window'] = risk_band_zscore['avg_window'].dt.total_seconds()

for col in risk_band_zscore.columns:
    risk_band_zscore[col] = (risk_band_zscore[col] - risk_band_zscore[col].mean())/risk_band_zscore[col].std()

for col in risk_band_analysis.columns:
    if '_part' in col or '_proportion' in col or 'merchant' in col:
        risk_band_analysis[col] = risk_band_analysis[col].astype(str) + '%'
    elif '_usd' in col:
        risk_band_analysis[col] = risk_band_analysis[col].astype(str) + '$'
    else:
        continue

fig, ax = plt.subplots(figsize=(45, 8), dpi=200)

sns.heatmap(risk_band_zscore, annot=risk_band_analysis,cmap=cmap, fmt='',square=True, linewidths=1.5,center=0, linecolor="#FFFFFF", annot_kws={'size': 11, 'fontproperties': mont_350},ax=ax)

ax.set_xticklabels([col.replace('_', ' ').title() for col in risk_band_zscore.columns], fontproperties=mont_350)

ax.set_yticklabels([label.get_text().capitalize() for label in ax.get_yticklabels()], fontproperties=mont_350)

ax.set_ylabel('Risk Band', fontproperties=mont_500)

cbar = ax.collections[0].colorbar

for label in cbar.ax.get_yticklabels():
    label.set_fontproperties(mont_350)

cbar.set_ticks([cbar.vmin, 0, cbar.vmax])

cbar.set_ticklabels(['Low', 'Medium', 'High'])


for start, stop, t in [('avg_amount_usd', 'median_amount_usd', 'Amount'), ('card_part', 'atm_part', 'Channel'), ('atm_withdrawal_part', 'transfer_out_part', 'Transaction Type'), ('debit_part', 'credit_part', 'Direction'), ('average_account_quantity', 'avg_trans_per_day', 'Behavior'), ('loan_part', 'credit_card_part', 'Account Type')]:
    rect = Rectangle(
        xy=(risk_band_zscore.columns.get_loc(start) + 0.02, 1.02),
        width=risk_band_zscore.columns.get_loc(stop) - risk_band_zscore.columns.get_loc(start) + 0.96,
        height=0.15,
        clip_on=False,
        transform=ax.get_xaxis_transform(),
        color='#e8e2d4'
    )
    ax.add_patch(rect)

    ax.text(
        risk_band_zscore.columns.get_loc(start) + (risk_band_zscore.columns.get_loc(stop) - risk_band_zscore.columns.get_loc(start) + 0.96)/2,
        1.085,
        t,
        transform=ax.get_xaxis_transform(),
        ha='center',
        va='center',
        fontproperties=mont_350,
        fontsize=15
    )

fig.savefig('RiskBand_Analysis.png', dpi=400, bbox_inches='tight')