WITH tokens (mint, symbol) AS (
  VALUES
    ('XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB', 'TSLAx'),
    ('Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh', 'NVDAx'),
    ('XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN', 'GOOGLx'),
    ('XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp', 'AAPLx'),
    ('Xs3eBt7uRfJX8QUs4suhyU8p2M6DoUDrJyWBa8LLZsg', 'AMZNx')
),
raw AS (
  SELECT
    block_time,
    amount_usd,
    token_bought_mint_address IN (
      'XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB',
      'Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh',
      'XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN',
      'XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp',
      'Xs3eBt7uRfJX8QUs4suhyU8p2M6DoUDrJyWBa8LLZsg') AS bought_is_stock,
    token_bought_mint_address,
    token_sold_mint_address,
    token_bought_amount,
    token_sold_amount
  FROM dex_solana.trades
  WHERE block_month >= DATE '2025-06-01'
    AND block_month <  DATE '2026-10-01'
    AND block_time  >= TIMESTAMP '2025-06-30 00:00:00'
    AND block_time  <  TIMESTAMP '2026-10-01 00:00:00'
    AND amount_usd > 0
    AND (token_bought_mint_address IN (
           'XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB',
           'Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh',
           'XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN',
           'XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp',
           'Xs3eBt7uRfJX8QUs4suhyU8p2M6DoUDrJyWBa8LLZsg')
      OR token_sold_mint_address IN (
           'XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB',
           'Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh',
           'XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN',
           'XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp',
           'Xs3eBt7uRfJX8QUs4suhyU8p2M6DoUDrJyWBa8LLZsg'))
),
trades AS (
  SELECT
    block_time,
    amount_usd,
    CASE WHEN bought_is_stock THEN token_bought_mint_address ELSE token_sold_mint_address END AS mint,
    CASE WHEN bought_is_stock THEN token_bought_amount ELSE token_sold_amount END AS token_amount,
    CASE WHEN bought_is_stock THEN token_sold_mint_address ELSE token_bought_mint_address END AS quote_mint
  FROM raw
)
SELECT
  from_unixtime(floor(to_unixtime(t.block_time) / 1800) * 1800) AS time_utc,
  k.symbol,
  CASE
    WHEN t.quote_mint IN ('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
                          'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB') THEN 'stable'
    WHEN t.quote_mint = 'So11111111111111111111111111111111111111112' THEN 'sol'
    ELSE 'other'
  END                                                 AS quote_type,
  count(*)                                            AS trades,
  sum(t.amount_usd)                                   AS volume_usd,
  sum(t.amount_usd) / sum(t.token_amount)             AS vwap_usd,
  max_by(t.amount_usd / t.token_amount, t.block_time) AS close_usd
FROM trades t
JOIN tokens k ON k.mint = t.mint
WHERE t.token_amount > 0
GROUP BY 1, 2, 3