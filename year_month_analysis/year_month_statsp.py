import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from sqlalchemy import create_engine
import os
import matplotlib.font_manager as fm
os.system('cls')
engine = create_engine(
    'postgresql+psycopg://USER:PASSWORD@localhost:5432/bankstrans'
)
query = """
SELECT 
    DATE_TRUNC('month', posted_at)::Date AS "Date",
    direction,
    SUM(CASE
            WHEN currency = 'USD' THEN amount
            WHEN currency = 'EUR' THEN amount*1.12
            WHEN currency = 'GBP' THEN amount*1.34
        END) AS month_amount_usd,
    COUNT(amount) AS transactions_per_month
FROM transactions t
JOIN accounts a
ON t.account_id = a.account_id
GROUP BY 
    DATE_TRUNC('month', posted_at),
    direction
ORDER BY DATE_TRUNC('month', posted_at), direction
"""

def format_date(x, pos=None):
    date = mdates.num2date(x)

    if date.month == 1:
        return date.strftime('%b\n%Y')
    else:
        return date.strftime('%b')


year_month_stats = pd.read_sql(query, engine)

mont_350 = fm.FontProperties(fname='C:/fonts/Montserrat_350')

mont_500 = fm.FontProperties(fname='C:/fonts/Montserrat_500')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 9))

year_month_stats['month_amount_usd_mln'] = year_month_stats['month_amount_usd']/1e6

direction_color = {'debit': '#133b54', 'credit': '#f28c42'}

for direction, group in year_month_stats.groupby('direction'):
    group = group.sort_values('Date')
    ax[0].plot(group['Date'], group['month_amount_usd_mln'], color=direction_color[direction])
    ax[0].annotate(direction.capitalize(), xy=(group['Date'].iloc[-1], group['month_amount_usd_mln'].iloc[-1]),xytext=(8,0),textcoords='offset points',va='center', fontproperties=mont_350)
    ax[1].plot(group['Date'], group['transactions_per_month'], color=direction_color[direction])
    ax[1].annotate(direction.capitalize(), xy=(group['Date'].iloc[-1], group['transactions_per_month'].iloc[-1]),xytext=(8,0),textcoords='offset points',va='center', fontproperties=mont_350)


for i in [0,1]:
    ax[i].xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['right'].set_visible(False)
    ax[i].grid(axis='y',alpha=0.5)
    for label in ax[i].get_xticklabels():
        label.set_fontproperties(mont_350)

ax[0].set_title('Monthly USD transaction amount', pad=15, loc='left', fontproperties=mont_350,fontsize=12,)

ax[1].set_title('Monthly transaction count', pad=15, loc='left', fontproperties=mont_350,fontsize=12)

fig.suptitle('Banking Transactions Trends',fontweight='normal',x = 0.05, ha='left',fontproperties=mont_500,fontsize=17)

ax[0].set_yticks([0.5, 1, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0], labels=['0.5M', '1M', '1.5M', '2.0M', '2.5M', '3.0M', '3.5M', '4.0M'], fontproperties=mont_350)

for row in year_month_stats[year_month_stats['month_amount_usd_mln']>3.5].itertuples():
    ax[0].annotate(
    f"{row.month_amount_usd_mln:.2f} mln $",
    xy=(row.Date, row.month_amount_usd_mln),
    xytext=(-50, 10),
    textcoords='offset points',
    fontproperties=mont_350
    )

for row in year_month_stats[year_month_stats['direction'] == 'debit'].sort_values(by='month_amount_usd_mln', ascending=False).iloc[:2, :].itertuples():
    ax[0].annotate(
    f'{row.month_amount_usd_mln:.2f} mln $',
    xy=(row.Date, row.month_amount_usd_mln),
    xytext=(-50, 10),
    textcoords='offset points',
    fontproperties=mont_350
    )

for row in year_month_stats[year_month_stats['transactions_per_month']>14_000].itertuples():
    ax[1].annotate(
    row.transactions_per_month,
    xy=(row.Date, row.transactions_per_month),
    xytext=(-30, 10),
    textcoords='offset points',
    fontproperties=mont_350
    )

for row in year_month_stats[year_month_stats['direction'] == 'credit'].sort_values(by='transactions_per_month', ascending=False).iloc[:2, :].itertuples():
    ax[1].annotate(
        row.transactions_per_month,
        xy=(row.Date, row.transactions_per_month),
        xytext=(-20, 10),
        textcoords='offset points',
        fontproperties=mont_350
    )

plt.savefig('D:/python/bank_project/forpublic/yearmonth.png', dpi=300)

plt.show()