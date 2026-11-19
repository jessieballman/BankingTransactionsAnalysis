import pandas as pd
import matplotlib.pyplot as plt
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

mont_350 = fm.FontProperties(fname='C:/fonts/Montserrat_350')

mont_500 = fm.FontProperties(fname='C:/fonts/Montserrat_500')

query = """
WITH summary AS(
    SELECT
        c.country,
        c.city,
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
    ON c.country = b.country AND c.city = b.city
    LEFT JOIN accounts a
    ON a.customer_id = c.customer_id
    LEFT JOIN transactions t
    ON a.account_id = t.account_id
    GROUP BY c.country, c.city
),

chn_cnt AS(
    SELECT
        country,
        city,
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
    GROUP BY country,city
),

risk_part AS(
    SELECT 
        country,
        city,
        ROUND(SUM(CASE WHEN risk_band IS NULL THEN 1 ELSE 0 END)/COUNT(*)::numeric*100,2) AS undefined_risk_part,
        ROUND(SUM(CASE WHEN risk_band = 'low' THEN 1 ELSE 0 END)/COUNT(*)::numeric*100,2) AS low_risk_part,
        ROUND(SUM(CASE WHEN risk_band = 'medium' THEN 1 ELSE 0 END)/COUNT(*)::numeric*100,2)AS medium_risk_part,
        ROUND(SUM(CASE WHEN risk_band = 'high' THEN 1 ELSE 0 END)/COUNT(*)::numeric*100,2) AS high_risk_part
    FROM customers
    GROUP BY country,city
),

trans_cnt AS(
    SELECT
        country,
        city,
        ROUND(AVG(cnt),2) AS average_trans_cnt,
        percentile_cont(0.50) WITHIN GROUP (ORDER BY cnt) AS median_trans_cnt
    FROM(
        SELECT
            country,
            city,
            c.customer_id,
            COUNT(DISTINCT transaction_id) AS cnt
        FROM customers c
        JOIN accounts a
        ON c.customer_id = a.customer_id
        JOIN transactions t
        ON a.account_id = t.account_id
        GROUP BY country,city,c.customer_id
    )
    GROUP BY country,city
)

SELECT
    s.country,
    s.city,
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
ON cc.country = s.country AND cc.city = s.city
JOIN risk_part rp
ON rp.country = s.country AND rp.city = s.city
JOIN trans_cnt tc
ON tc.country = s.country AND tc.city = s.city


"""

city_analysis = pd.read_sql(query, engine)

city_analysis.sort_values(by='country', inplace=True)



# A cycle that generates a z-score for each country and creates a heat map of cities within each country based on that z-score.
for country in city_analysis['country'].drop_duplicates():
    cmap = LinearSegmentedColormap.from_list('cca_htm', colors, N=256)
    fig, ax = plt.subplots(figsize=(18, 5))
    cca = city_analysis[city_analysis['country'] == country]
    ccazscore = cca.copy()
    ccazscore.drop(['country'], axis=1, inplace=True)
    cca.drop(['country'],axis=1,inplace=True)
    cca.set_index('city', inplace=True)
    ccazscore.set_index('city', inplace=True)
    for col in ccazscore.columns:
        std = ccazscore[col].std()
        if std == 0 or pd.isna(std):
            ccazscore[col] = 0
        else:
            ccazscore[col] = (ccazscore[col]-ccazscore[col].mean())/std
    for col in cca.columns:
        if '_part' in col:
            cca[col] = cca[col].astype(str) + '%'
        elif '_usd' in col:
            cca[col] = cca[col].astype(str) + '$'
        else:
            continue
    sns.heatmap(ccazscore, annot=cca,fmt='', cmap=cmap, square=True, linewidths=1.5, linecolor='#FFFFFF', annot_kws={'size': 11, 'fontproperties': mont_350},ax=ax)

    ax.set_xticklabels([col.replace('_', ' ').title() for col in ccazscore.columns])

    cbar = ax.collections[0].colorbar

    for label in cbar.ax.get_yticklabels():
        label.set_fontproperties(mont_350)

    cbar.set_ticks([cbar.vmin, 0, cbar.vmax])

    cbar.set_ticklabels(['Low', 'Medium', 'High'])

    ax.set_ylabel(f'{country}', fontproperties=mont_500)
    
    plt.savefig(f'{country}_Analysis.png', bbox_inches='tight')
