SELECT
    'FirstAnomaly' AS period,

    -- Countries
    ROUND(COUNT(*) FILTER (WHERE c.country = 'CA')/COUNT(*)::numeric*100,2) AS CA_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'DK')/COUNT(*)::numeric*100,2) AS DK_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'PT')/COUNT(*)::numeric*100,2) AS PT_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'ES')/COUNT(*)::numeric*100,2) AS ES_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'SI')/COUNT(*)::numeric*100,2) AS SI_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'US')/COUNT(*)::numeric*100,2) AS US_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'FR')/COUNT(*)::numeric*100,2) AS FR_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'NO')/COUNT(*)::numeric*100,2) AS NO_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'GB')/COUNT(*)::numeric*100,2) AS GB_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'IT')/COUNT(*)::numeric*100,2) AS IT_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'NZ')/COUNT(*)::numeric*100,2) AS NZ_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'AU')/COUNT(*)::numeric*100,2) AS AU_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'NL')/COUNT(*)::numeric*100,2) AS NL_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'SE')/COUNT(*)::numeric*100,2) AS SE_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'FI')/COUNT(*)::numeric*100,2) AS FI_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'DE')/COUNT(*)::numeric*100,2) AS DE_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'IE')/COUNT(*)::numeric*100,2) AS IE_part,

    -- Categories
    ROUND(COUNT(*) FILTER (WHERE category IS NULL)/COUNT(*)::numeric*100,2) AS non_merchant_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'utilities')/COUNT(*)::numeric*100,2) AS utilities_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'transport')/COUNT(*)::numeric*100,2) AS transport_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'restaurants')/COUNT(*)::numeric*100,2) AS restaurants_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'home')/COUNT(*)::numeric*100,2) AS home_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'health')/COUNT(*)::numeric*100,2) AS health_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'clothing')/COUNT(*)::numeric*100,2) AS clothing_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'electronics')/COUNT(*)::numeric*100,2) AS electronics_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'groceries')/COUNT(*)::numeric*100,2) AS groceries_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'entertainment')/COUNT(*)::numeric*100,2) AS entertainment_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'travel')/COUNT(*)::numeric*100,2) AS travel_part,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE joined_on > '2024-10-01' AND joined_on < '2025-01-01')::numeric/('2025-01-01'::date - '2024-10-01'::date)::numeric AS new_customers_per_day,

    -- Risk Bands
    ROUND(((COUNT(*) FILTER (WHERE risk_band = 'high'))/COUNT(*)::numeric)*100,2) AS high_risk,
    ROUND(((COUNT(*) FILTER (WHERE risk_band = 'low'))/COUNT(*)::numeric)*100,2) AS low_risk,
    ROUND(((COUNT(*) FILTER (WHERE risk_band = 'medium'))/COUNT(*)::numeric)*100,2) AS medium_risk,
    ROUND(((COUNT(*) FILTER (WHERE risk_band IS NULL))/COUNT(*)::numeric)*100,2) AS undefined_risk,

    -- Transactions Types
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'atm_withdrawal')/COUNT(*)::numeric)*100,2) AS atm_withdrawal_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'card_payment')/COUNT(*)::numeric)*100,2) AS card_payment_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'direct_debit')/COUNT(*)::numeric)*100,2) AS direct_debit_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'fee')/COUNT(*)::numeric)*100,2) AS fee_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'interest')/COUNT(*)::numeric)*100,2) AS interest_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'refund')/COUNT(*)::numeric)*100,2) AS refund_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'salary')/COUNT(*)::numeric)*100,2) AS salary_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'transfer_in')/COUNT(*)::numeric)*100,2) AS transfer_in_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'transfer_out')/COUNT(*)::numeric)*100,2) AS transfer_out_part,

    -- Directions
    ROUND((COUNT(transaction_id) FILTER (WHERE direction = 'credit')/COUNT(*)::numeric)*100,2) AS credit_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE direction = 'debit')/COUNT(*)::numeric)*100,2) AS debit_part,

    -- Channels
    ROUND((SUM(CASE WHEN channel = 'card' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS card_part,
    ROUND((SUM(CASE WHEN channel = 'online' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS online_part,
    ROUND((SUM(CASE WHEN channel = 'mobile' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS mobile_part,
    ROUND((SUM(CASE WHEN channel = 'branch' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS branch_part,
    ROUND((SUM(CASE WHEN channel = 'atm' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS atm_part,

    -- Nigth Part
    ROUND(((COUNT(*) FILTER(WHERE EXTRACT(HOUR FROM posted_at AT TIME ZONE timezone) BETWEEN 0 AND 6))/COUNT(*)::numeric)*100,2) AS night_proportion
FROM transactions t
JOIN accounts a
ON t.account_id = a.account_id
JOIN customers c
ON c.customer_id = a.customer_id
JOIN timezones tz
ON tz.city = c.city AND tz.country = c.country
LEFT JOIN merchants m
ON m.merchant_id = t.merchant_id
WHERE posted_at > '2024-10-01' AND posted_at < '2025-01-01'

UNION ALL

SELECT
    'Average' AS period,

    -- Countries
    ROUND(COUNT(*) FILTER (WHERE c.country = 'CA')/COUNT(*)::numeric*100,2) AS CA_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'DK')/COUNT(*)::numeric*100,2) AS DK_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'PT')/COUNT(*)::numeric*100,2) AS PT_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'ES')/COUNT(*)::numeric*100,2) AS ES_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'SI')/COUNT(*)::numeric*100,2) AS SI_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'US')/COUNT(*)::numeric*100,2) AS US_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'FR')/COUNT(*)::numeric*100,2) AS FR_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'NO')/COUNT(*)::numeric*100,2) AS NO_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'GB')/COUNT(*)::numeric*100,2) AS GB_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'IT')/COUNT(*)::numeric*100,2) AS IT_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'NZ')/COUNT(*)::numeric*100,2) AS NZ_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'AU')/COUNT(*)::numeric*100,2) AS AU_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'NL')/COUNT(*)::numeric*100,2) AS NL_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'SE')/COUNT(*)::numeric*100,2) AS SE_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'FI')/COUNT(*)::numeric*100,2) AS FI_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'DE')/COUNT(*)::numeric*100,2) AS DE_part,
    ROUND(COUNT(*) FILTER (WHERE c.country = 'IE')/COUNT(*)::numeric*100,2) AS IE_part,

    -- Categories
    ROUND(COUNT(*) FILTER (WHERE category IS NULL)/COUNT(*)::numeric*100,2) AS non_merchant_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'utilities')/COUNT(*)::numeric*100,2) AS utilities_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'transport')/COUNT(*)::numeric*100,2) AS transport_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'restaurants')/COUNT(*)::numeric*100,2) AS restaurants_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'home')/COUNT(*)::numeric*100,2) AS home_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'health')/COUNT(*)::numeric*100,2) AS health_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'clothing')/COUNT(*)::numeric*100,2) AS clothing_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'electronics')/COUNT(*)::numeric*100,2) AS electronics_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'groceries')/COUNT(*)::numeric*100,2) AS groceries_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'entertainment')/COUNT(*)::numeric*100,2) AS entertainment_part,
    ROUND(COUNT(*) FILTER (WHERE category = 'travel')/COUNT(*)::numeric*100,2) AS travel_part,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE joined_on < '2024-10-01' OR (joined_on > '2025-01-01' AND joined_on < '2025-10-01'))::numeric/(('2025-10-01'::date - MIN(joined_on)-('2025-01-01'::date - '2024-10-01'::date)))::numeric AS new_customers_per_day,

    -- Risk Bands
    ROUND(((COUNT(*) FILTER (WHERE risk_band = 'high'))/COUNT(*)::numeric)*100,2) AS high_risk,
    ROUND(((COUNT(*) FILTER (WHERE risk_band = 'low'))/COUNT(*)::numeric)*100,2) AS low_risk,
    ROUND(((COUNT(*) FILTER (WHERE risk_band = 'medium'))/COUNT(*)::numeric)*100,2) AS medium_risk,
    ROUND(((COUNT(*) FILTER (WHERE risk_band IS NULL))/COUNT(*)::numeric)*100,2) AS undefined_risk,

    -- Transactions Types
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'atm_withdrawal')/COUNT(*)::numeric)*100,2) AS atm_withdrawal_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'card_payment')/COUNT(*)::numeric)*100,2) AS card_payment_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'direct_debit')/COUNT(*)::numeric)*100,2) AS direct_debit_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'fee')/COUNT(*)::numeric)*100,2) AS fee_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'interest')/COUNT(*)::numeric)*100,2) AS interest_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'refund')/COUNT(*)::numeric)*100,2) AS refund_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'salary')/COUNT(*)::numeric)*100,2) AS salary_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'transfer_in')/COUNT(*)::numeric)*100,2) AS transfer_in_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE transaction_type = 'transfer_out')/COUNT(*)::numeric)*100,2) AS transfer_out_part,

    -- Directions
    ROUND((COUNT(transaction_id) FILTER (WHERE direction = 'credit')/COUNT(*)::numeric)*100,2) AS credit_part,
    ROUND((COUNT(transaction_id) FILTER (WHERE direction = 'debit')/COUNT(*)::numeric)*100,2) AS debit_part,

    -- Channels
    ROUND((SUM(CASE WHEN channel = 'card' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS card_part,
    ROUND((SUM(CASE WHEN channel = 'online' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS online_part,
    ROUND((SUM(CASE WHEN channel = 'mobile' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS mobile_part,
    ROUND((SUM(CASE WHEN channel = 'branch' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS branch_part,
    ROUND((SUM(CASE WHEN channel = 'atm' THEN 1 ELSE 0 END)/COUNT(*)::numeric)*100.0,2) AS atm_part,

    -- Nigth Part
    ROUND(((COUNT(*) FILTER(WHERE EXTRACT(HOUR FROM posted_at AT TIME ZONE timezone) BETWEEN 0 AND 6))/COUNT(*)::numeric)*100,2) AS night_proportion
FROM transactions t
JOIN accounts a
ON t.account_id = a.account_id
JOIN customers c
ON c.customer_id = a.customer_id
JOIN timezones tz
ON tz.city = c.city AND tz.country = c.country
LEFT JOIN merchants m
ON m.merchant_id = t.merchant_id
WHERE posted_at < '2024-10-01' OR (posted_at > '2025-01-01' AND posted_at < '2025-10-01')