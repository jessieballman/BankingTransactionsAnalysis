SELECT transaction_id, ARRAY_AGG(suspicious) AS suspicious FROM(
    SELECT transaction_id, 'refund_without_buy' AS suspicious FROM transactions t
    WHERE transaction_type = 'refund' 
    AND NOT EXISTS(
        SELECT 1 FROM transactions t2
        WHERE t.account_id = t2.account_id
        AND t2.transaction_type IN ('card_payment', 'direct_debit')
        AND t.merchant_id = t2.merchant_id
        AND t2.posted_at < t.posted_at
        AND t.amount = t2.amount)

    UNION ALL

    SELECT transaction_id, 'duplicated operation' AS suspicious FROM(
        SELECT
            transaction_id,
            ROW(transaction_type || amount || merchant_id || channel || direction) AS current_operation,
            LAG(ROW(transaction_type || amount || merchant_id || channel || direction)) OVER (PARTITION BY account_id ORDER BY posted_at) AS lag_operation,
            posted_at - LAG(posted_at) OVER(PARTITION BY account_id ORDER BY posted_at) AS time_between
        FROM transactions
    )
    WHERE lag_operation = current_operation AND time_between < INTERVAL '5 minute'

    UNION ALL

    SELECT transaction_id, 'big_night_out_operation' AS suspicious FROM transactions t
    JOIN accounts a
    ON a.account_id = t.account_id
    JOIN customers c
    ON c.customer_id = a.customer_id
    JOIN timezones tz
    ON tz.city = c.city AND tz.country = c.country
    JOIN (
        SELECT 
            t.account_id, 
            percentile_cont(0.50) WITHIN GROUP (ORDER BY CASE
                WHEN currency = 'USD' THEN amount
                WHEN currency = 'EUR' THEN amount*1.12
                WHEN currency = 'GBP' THEN amount*1.34
            END) AS median_amount 
        FROM transactions t
        JOIN accounts a
        ON a.account_id = t.account_id
        JOIN customers c
        ON c.customer_id = a.customer_id
        GROUP BY t.account_id) ma
    ON ma.account_id = t.account_id
    WHERE EXTRACT(HOUR FROM posted_at AT TIME ZONE timezone) BETWEEN 0 AND 6 
    AND
    amount > median_amount*2
    AND transaction_type IN ('atm_withdrawal', 'card_payment', 'transfer_out')
)
GROUP BY transaction_id