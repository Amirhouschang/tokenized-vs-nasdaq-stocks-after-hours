WITH t AS (
  SELECT
    block_month,
    project,
    fee_tier,
    amount_usd,
    CASE WHEN token_bought_mint_address LIKE 'Xs%'
         THEN token_bought_mint_address ELSE token_sold_mint_address END AS mint,
    CASE WHEN token_bought_mint_address LIKE 'Xs%'
         THEN token_bought_symbol ELSE token_sold_symbol END AS symbol
  FROM dex_solana.trades
  WHERE block_month >= DATE '2025-06-01'
    AND block_month <  DATE '2026-10-01'
    AND (token_bought_mint_address LIKE 'Xs%'
      OR token_sold_mint_address   LIKE 'Xs%')
)
SELECT
  block_month,
  symbol,
  mint,
  project,
  fee_tier,
  count(*)        AS trades,
  sum(amount_usd) AS volume_usd
FROM t
GROUP BY 1, 2, 3, 4, 5
HAVING count(*) >= 100