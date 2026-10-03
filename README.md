# Tokenized Stocks on Solana vs. Nasdaq: Price Behaviour Outside US Market Hours

**English** | [Deutsch](README.de.md)

**Tesla, Nvidia, Alphabet, Apple and Amazon · 8 July 2025 to 30 September 2026**

**[Open the interactive dashboard](https://tokenized-vs-nasdaq-stocks-after-hours-bpasxc8wni65acwxnmkscb.streamlit.app/)** (English and German)

## What this project asks

Nasdaq's regular session runs from 9:30 to 16:00 New York time on weekdays. Over the 15 months analysed here, the exchange was closed 81 % of the time: every night, every weekend and every public holiday. (The shares also trade in a thin pre-market and post-market, but the official opening and closing prices come from the regular session.) Tokenized versions of the same shares, called xStocks, trade around the clock on the Solana blockchain, so their price keeps moving while the exchange is closed.

This project compares five tokenized stocks with their Nasdaq shares and asks what the token price does during a **closed period**: the time from one closing bell to the next opening bell, which is a night, a weekend or a break around a public holiday. The central question is whether the token price already contains the news of the closed period, so that it shows where the share will open the next morning. Two questions follow from it: whether this can be turned into a profit, and at what time of the night the price adjusts.

The project is written for two audiences: readers from the stock market who have never used a blockchain, and readers from crypto who want to know how closely these tokens follow the real market. Terms from both worlds are explained where they first appear, and the dashboard has a glossary.

The full analysis is in the notebook `tokenized_vs_nasdaq_after_hours.ipynb`, and the dashboard lets you explore every single closed period. This page gives the background, the method and the results.

## The result in short

The token price is a good early indicator of the opening price, but not a source of easy profit.

While Nasdaq is closed, the token market keeps moving: the price spans a median range of 1.0 % to 1.5 % in a regular night and 1.7 % to 2.5 % over a weekend. These moves are not noise. The token's move during a closed period has a correlation of 0.88 to 0.96 with the stock's gap from close to open, and where the stock gapped by at least 0.5 %, the token had moved in the same direction in 95 % to 99 % of the cases. The last token price before the open misses the real opening price by a median of 0.18 % to 0.30 %, which beats yesterday's closing price clearly for Tesla and Nvidia and only slightly for Apple. The adjustment happens mainly in the last hours before the open, when the stock itself trades in the pre-market.

Buying the token at the close and selling it after the open earns 0.06 % to 0.18 % per closed period before costs, about as much as the shares gained from close to open. Over all closed periods, a round-trip cost of 0.3 % turns this into a loss for all five tokens. While Nasdaq is open, the tokens stay within 0.17 % to 0.29 % of the share price on average, and the thinnest token, Amazon, tracks worst.

The seven questions behind these results are answered one by one in the [results section](#results-the-seven-questions).

## Background: the tokens

### What xStocks are and who issues them

All five tokens are **xStocks**, issued by Backed Assets (JE) Limited, a private limited company in Jersey [2][3]. Backed buys the real shares through brokers, deposits them with a regulated custodian and mints one token per share [1], so each xStock is backed 1:1 by the underlying share [2]. A token gives price exposure, not shareholder status: holders do not own the shares and have no voting rights or claims against the company [2]. xStocks are not available in the United States or to US persons, and not in Canada, the United Kingdom or Australia [2][3].

xStocks launched on Solana on 30 June 2025 with more than 55 tokenized stocks and ETFs [1]; this date is the earliest possible start of the data. They trade on centralized exchanges such as Kraken and Bybit and on decentralized exchanges on Solana such as Raydium, which can be reached through the aggregator Jupiter [1]. This project uses decentralized trades only. On 2 December 2025 Kraken announced that it had agreed to acquire Backed, the company behind xStocks [4].

xStocks are not the only tokenized stocks on Solana; Ondo Global Markets, for example, also offers tokenized US stocks there [10]. Other issuers are not part of this project.

### The five tokens

| Token | Solana mint address | Share | Ticker | Exchange | ISIN of the share |
|---|---|---|---|---|---|
| TSLAx | [`XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB`](https://solscan.io/token/XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB) | Tesla, Inc. | TSLA | Nasdaq | US88160R1014 |
| NVDAx | [`Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh`](https://solscan.io/token/Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh) | NVIDIA Corporation | NVDA | Nasdaq | US67066G1040 |
| GOOGLx | [`XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN`](https://solscan.io/token/XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN) | Alphabet Inc., Class A | GOOGL | Nasdaq | US02079K3059 |
| AAPLx | [`XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp`](https://solscan.io/token/XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp) | Apple Inc. | AAPL | Nasdaq | US0378331005 |
| AMZNx | [`Xs3eBt7uRfJX8QUs4suhyU8p2M6DoUDrJyWBa8LLZsg`](https://solscan.io/token/Xs3eBt7uRfJX8QUs4suhyU8p2M6DoUDrJyWBa8LLZsg) | Amazon.com, Inc. | AMZN | Nasdaq | US0231351067 |

The mint address is the unique address of a token on Solana. The five addresses are listed in the Solana Foundation's case study on xStocks [1], and exchange, ticker and ISIN of the shares come from company profiles on StockAnalysis [6]. The Alphabet token tracks the Class A share (GOOGL), not the Class C share (GOOG) [11].

The tokens differ strongly in how much they are traded. In the analysis window, their trades against US-dollar stablecoins on Solana's decentralized exchanges add up as follows (own Dune data). A half-hour has a price if at least one stablecoin trade took place in it and the price was not flagged as an outlier (see [From trades to prices](#from-trades-to-prices)).

| Token | Trades | Volume (million USD) | Half-hours with a price |
|---|---|---|---|
| TSLAx | 3,213,000 | 608.9 | 100.0 % |
| NVDAx | 3,950,211 | 537.7 | 99.9 % |
| GOOGLx | 767,548 | 103.3 | 97.1 % |
| AAPLx | 532,211 | 55.1 | 94.3 % |
| AMZNx | 313,809 | 37.2 | 87.0 % |

### Why these five tokens

The five tokens are not picked by hand. They follow from two rules, applied to every token whose Solana mint address starts with `Xs`, the prefix used by xStocks. The monthly overview from Dune lists 145 symbols with trades from July 2025 on; a few of them are unrelated tokens that share the prefix.

The first rule is continuous trading: at least 5,000 trades in every month from July 2025 to September 2026, so that a token has a usable price series throughout the window. The second rule is a well-known single company without a crypto link, so that readers outside the crypto scene can follow the comparison. The first rule leaves ten tokens. The second removes two ETFs (SPYx, QQQx) and three crypto-related companies (Circle, Strategy, Robinhood). Robinhood is a broker with a large crypto business, so excluding it is a judgement call.

| Token | Underlying | Lowest monthly trades | Volume (million USD) | Decision |
|---|---|---|---|---|
| SPYx | S&P 500 ETF | 110,739 | 2,684.0 | excluded: ETF |
| CRCLx | Circle | 56,522 | 1,187.8 | excluded: crypto-related |
| NVDAx | Nvidia | 96,190 | 750.9 | **selected** |
| TSLAx | Tesla | 164,118 | 730.5 | **selected** |
| QQQx | Nasdaq-100 ETF | 18,174 | 352.8 | excluded: ETF |
| MSTRx | Strategy | 43,736 | 310.5 | excluded: crypto-related |
| GOOGLx | Alphabet | 41,533 | 138.1 | **selected** |
| HOODx | Robinhood | 6,063 | 90.8 | excluded: crypto-related |
| AAPLx | Apple | 18,036 | 83.2 | **selected** |
| AMZNx | Amazon | 8,413 | 53.1 | **selected** |

Volume: all decentralized trades, July 2025 to September 2026. The export leaves out groups with fewer than 100 trades per month, venue and fee tier, so the figures are slightly too low.

Two candidates were considered first and dropped because they were hardly traded in 2025. MSFTx (Microsoft) had no trades in July 2025 and first reached 5,000 trades per month in March 2026. MCDx (McDonald's) had 102 trades in July 2025 and also first reached that level in March 2026.

### Where the tokens trade

Solana dominates on-chain trading of tokenized stocks: in June 2026 it accounted for about 94 % to 96 % of the trading volume across blockchains, according to SolanaFloor [7]. This is why the project uses Solana and not Ethereum.

The market grew strongly during the analysis window. The monthly decentralized volume of all tokens in the overview query rose from 114 million USD in July 2025 to 518 million USD in August 2026. Two months stand far above this trend: June 2026 with 2,290 million USD and September 2026 with 2,105 million USD (own Dune data).

On a decentralized exchange (DEX), a trader swaps against a liquidity pool instead of matching orders in an order book. Several DEXs list the five tokens. Raydium is the main venue, but not for every token to the same degree. Share of the decentralized volume of each token from July 2025 to August 2026 (own Dune data):

| Venue | TSLAx | NVDAx | GOOGLx | AAPLx | AMZNx |
|---|---|---|---|---|---|
| Raydium | 59.3 % | 72.9 % | 41.1 % | 55.6 % | 67.7 % |
| Byreal | 11.1 % | 9.9 % | 30.6 % | 20.5 % | 15.8 % |
| JupiterZ | 6.2 % | 6.1 % | 22.1 % | 14.9 % | 14.8 % |
| Orca (Whirlpool) | 16.3 % | 8.8 % | 3.3 % | 1.7 % | 0.6 % |
| Other | 7.2 % | 2.3 % | 2.9 % | 7.3 % | 1.2 % |

In September 2026 the trading pattern changed. A new venue, Raydium LaunchLab, appeared in August 2026 with only about 158,000 USD of volume (Nvidia token only) and took 12 % to 19 % of the volume of each of the five tokens in September. The share of trades against tokens other than stablecoins or SOL (Solana's own currency) rose from 4.9 % of the volume in August to 38.5 % in September. The stablecoin prices used in this project were not visibly affected: in September 2026 the prices from the other trades deviate from them by a median of 0.04 % to 0.22 %, depending on the token and on what it was traded against.

## Data and method

### Sources

| Data | Source | Detail |
|---|---|---|
| Token trades | Dune, table `dex_solana.trades` [8] | Two SQL queries, each exported once as CSV |
| Stock prices | Yahoo Finance via `yfinance` [9] | Hourly bars with pre-market and post-market, not dividend-adjusted, downloaded on 2 October 2026 |
| Market calendar | Derived from the stock data | The eight Nasdaq holidays of 2026 in the window match Nasdaq's published schedule [5] |

All figures marked "own Dune data" are computed from the files in `data/raw/`. The token selection, the data quality checks and the results of the seven questions are reproduced step by step in the notebook; the venue shares and the split by quote type are computed from the same files but are not part of the notebook.

### From trades to prices

**Token price.** For every token and half-hour, the volume-weighted average price (VWAP) of all trades against USDC or USDT is used. Both are stablecoins, tokens pegged to the US dollar, so the price needs no second conversion. A price that deviates by more than 5 % from the centred 24-hour rolling median is flagged as an outlier and not used (31 half-hours in total). The analysis window starts on 8 July 2025, because the Amazon token traded at unusable prices from 2 to 7 July 2025: between about 180 and 3,300 USD on thin volume (a median of about 265 USD per half-hour), against a real share price of about 220 to 225 USD.

**Stock price.** The open is the open of the 9:30 bar, the close is the close of the last regular bar. On the two shortened trading days in the window (28 November and 24 December 2025) the close is approximated.

**Closed periods.** A closed period is the time between one close and the next open. The window has 311 trading days and therefore 310 closed periods per share: 243 regular nights, 56 weekends and 11 breaks around a public holiday.

**Time zones.** All timestamps are stored in UTC and converted to New York time for the market calendar, so daylight-saving changes are handled automatically.

**Costs.** Pool fees are missing from Dune: the column `fee_tier` of `dex_solana.trades` is filled for only 0.3 % of the volume in the overview, and not at all for Raydium. Trading costs in this project are therefore scenarios, not measurements.

### Data quality

| Check | Result |
|---|---|
| Duplicates in token and stock data | 0 |
| Missing values, prices of zero or below | 0 |
| Trading days per share in the window | 311, identical for all five |
| Days without an opening bar | 0 |
| Incomplete regular sessions | 2 (shortened trading days on 28 November and 24 December 2025) |
| Half-hours without a stablecoin trade | TSLAx 1, NVDAx 7, GOOGLx 615, AAPLx 1,216, AMZNx 2,804 of 21,600 each |
| Bad ticks flagged in post-market stock bars | 11 |

Gaps in the token data are rare during market hours and most frequent at weekends: for the Amazon token 3.6 % of the half-hours are missing during the session and 19.2 % at weekends.

## Results: the seven questions

Each question below starts with its answer, then shows how it was measured. All numbers come from the notebook; the section number in italics tells where to find the calculation. The labels of the charts are in English.

### 1. How close is the token to the stock while Nasdaq is open?

*Notebook, section 12*

**Very close.** Compared hour by hour during the regular session, the token price deviates from the share price by 0.17 % (Nvidia) to 0.29 % (Amazon) on average. In 95 % of the hours the deviation is below 0.48 % to 0.88 %, depending on the token. All five medians are slightly positive (0.03 % to 0.18 %), so the tokens trade at a small premium. The deviation is largest for Amazon, the least traded token.

| Token | Hours compared | Mean absolute deviation | Median deviation | 95 % of the hours below |
|---|---|---|---|---|
| TSLAx | 2,169 | 0.19 % | +0.03 % | 0.55 % |
| NVDAx | 2,169 | 0.17 % | +0.05 % | 0.48 % |
| GOOGLx | 2,167 | 0.24 % | +0.15 % | 0.60 % |
| AAPLx | 2,152 | 0.25 % | +0.18 % | 0.59 % |
| AMZNx | 2,152 | 0.29 % | +0.08 % | 0.88 % |

The comparison is coarse. The token price is the mean of two half-hours, and the stock price is the midpoint of the open and close of the hourly bar, so part of the deviation is price movement within the hour and not a pricing error of the token.

### 2. How far does the token move while Nasdaq is closed?

*Notebook, section 13*

**The longer the exchange is closed, the further the token moves, but not in proportion.** Measured as the range between the highest and the lowest token price during a closed period, the median is 1.0 % (Apple) to 1.5 % (Alphabet) in a regular night of 17.5 hours, 1.7 % (Apple) to 2.5 % (Tesla) over a weekend of about 65 hours, and 1.6 % to 2.2 % in a break around a public holiday. A weekend is almost four times as long as a night, but its range is less than twice as wide.

The net move from the last token price before the close to the last price before the open is smaller than the range: a median of 0.3 % to 0.7 % in a regular night and 0.4 % to 1.3 % over a weekend. There are 56 weekends and 11 holiday breaks per token, so the weekend and holiday results rest on few observations.

![Median range of the token price by type of closed period](figures/03_token_range_by_night_type.png)

### 3. Does the token price predict the opening price?

*Notebook, section 14*

**Largely, yes.** Three measures answer this. All three compare the token with the stock over the same closed period. The token's move runs from its last price before the close to its last price within two hours before the open, and the stock's gap runs from the official close to the official open.

The first measure is the correlation between the two. It is 0.88 (Apple) to 0.96 (Nvidia), where 1 would mean a perfect linear relationship and 0 none, and it is weaker over weekends (0.88) than over regular nights (0.95). The second is the direction: where the stock gapped by at least 0.5 %, the token had moved in the same direction in 95 % to 99 % of the cases. The third is the forecast error, the median distance between the last token price before the open and the real opening price. It is 0.18 % to 0.30 %. As a naive benchmark, yesterday's closing price misses the opening price by 0.32 % to 0.85 %.

Each dot in the first chart is one closed period. The closer the dots lie to the dashed line, the better the token's move matched the stock's gap.

![Token move against the stock's opening gap, one panel per stock](figures/01_token_move_vs_stock_gap.png)

The token forecast beats the benchmark clearly for Tesla (0.22 % against 0.85 %) and Nvidia (0.18 % against 0.83 %), and by about half for Alphabet (0.25 % against 0.53 %) and Amazon (0.30 % against 0.53 %). For Apple the advantage is small (0.27 % against 0.32 %), because Apple's overnight gaps were small in this period and left little to predict.

![Forecast error for the opening price: yesterday's close against the token price before the open](figures/02_opening_price_forecast_error.png)

### 4. Does buying at the close and selling after the open pay?

*Notebook, section 15*

**Not after costs.** The test buys the token in the last half-hour before the close and sells it in the first half-hour after the next open, in every closed period. Before costs the trade earns a mean of 0.06 % (Amazon) to 0.18 % (Nvidia) per closed period, and 51 % to 57 % of the single trades are profitable. Dune provides no pool fees for these tokens, so costs enter as round-trip scenarios from 0.1 % to 1.0 %. The mean gross return is at the same time the break-even cost. At a round-trip cost of 0.1 %, only Nvidia (+0.08 %) and Alphabet (+0.05 %) stay positive; at 0.3 %, all five tokens lose money.

The small gross return is not a token effect. The shares themselves gained 0.05 % to 0.21 % on average from close to open in the same periods, so the trade mostly collects the overnight drift of a rising market.

![Mean return per closed period before costs, with the 0.1 % and 0.3 % cost lines](figures/04_overnight_trade_return_vs_costs.png)

In the dashboard the test can be filtered by type of closed period. Over weekends alone, the average before costs is higher (+0.44 % across the five stocks) and stays positive after a cost of 0.3 % (+0.14 %), while the shares themselves gained 0.1 % to 0.4 % over the same weekends. This rests on 56 weekends per token and should be read with care.

### 5. Do thinly traded tokens track the stock worse?

*Notebook, section 16*

**Yes.** The table compares, for each token, the median volume traded per closed period with the share of half-hours that have a price and the forecast error from question 3.

| Token | Median volume per closed period (USD) | Half-hours with a price | Forecast error |
|---|---|---|---|
| TSLAx | 645,522 | 100.0 % | 0.22 % |
| NVDAx | 394,638 | 100.0 % | 0.18 % |
| GOOGLx | 92,353 | 97.2 % | 0.25 % |
| AAPLx | 28,841 | 94.5 % | 0.27 % |
| AMZNx | 25,960 | 86.5 % | 0.30 % |

Tesla and Nvidia trade several hundred thousand USD per closed period, have a price in practically every half-hour and the smallest forecast errors. Apple and Amazon trade below 30,000 USD per closed period. The Amazon token has no price in 13.5 % of the half-hours of an average closed period and the largest forecast error. The gap between token and stock at the close, called the basis, also fluctuates most for Amazon (standard deviation 0.49 %, against 0.30 % to 0.32 % for the other four tokens). Amazon also has the largest deviation during market hours (question 1).

### 6. When during the night does the price adjust?

*Notebook, section 17*

**Late: mainly in the last hours before the open.** Only regular nights are used here (243 per share, 17.5 hours from the 16:00 close to the 9:30 open), so that every night has the same clock. For every half-hour, the upper panel shows the median distance between the token price and the next opening price. For Tesla and Nvidia, this distance falls slowly from about 0.7 % at the close to about 0.5 % at 04:00, and then to about 0.2 % in the pre-market hours between 04:00 and 09:30, when the stock itself trades again. Apple stays almost flat until the last two hours, because its overnight gaps were small and there was little to adjust.

The lower panel shows when the tokens are traded. Token trading never stops during the night: about 36 % of the night volume is traded between 20:00 and 04:00, when no stock market session is open. The busiest half-hours are the first one after the close and the last one before the open.

![Distance to the next opening price and share of the night volume, by time of night](figures/05_night_path_to_open.png)

### 7. Does the token follow the stock's pre-market and post-market prices?

*Notebook, section 18*

**About as closely as during the regular session.** The shares also trade before the open (pre-market, 4:00 to 9:30) and after the close (post-market, 16:00 to 20:00), with less volume. Compared with these prices hour by hour, the mean deviation of the token is practically the same in all three sessions for Tesla and Nvidia (0.15 % to 0.20 %). For the three thinner tokens it is somewhat higher outside the regular session, by up to 0.06 percentage points.

![Mean deviation between token and stock in pre-market, regular session and post-market](figures/06_deviation_by_session.png)

The token also follows news that arrives right after the close, such as earnings. Its move between the close and the stock's last post-market bar is correlated with the stock's move over the same window at 0.83 to 0.90. On the evenings when the stock moved by at least 1 % after the close (8 to 18 evenings per share), the token moved in the same direction in 93 % to 100 % of the cases.

Pre-market and post-market prices from Yahoo Finance are less reliable than regular-session prices (see the limitations below), so the answer to this question is indicative.

## Limitations

**Short history.** The analysis covers 15 months and 310 closed periods per share, of which only 56 are weekends and 11 include a holiday. Results for weekends and holidays rest on few observations and can be shaped by single events. The market was also still developing: volume grew strongly in 2026 and the trading pattern changed in September 2026, so the results are averages over a changing market.

**Prices and costs.** A 30-minute average is not a price at which a trade could have been executed, so the trading test is an approximation. Costs are scenarios, not measurements: pool fees are not available from Dune, and slippage in thin pools is not modelled. Real costs for the thin tokens are likely to be higher than for the liquid ones.

**Coverage of the market.** Only decentralized trades are included; trades on centralized exchanges such as Kraken are not.

**Stock data.** Pre-market and post-market prices from Yahoo Finance contain bad ticks and missing bars. They are used only for question 7. Dividends are not adjusted: Apple, Alphabet and Nvidia paid five dividends each in the window, between 0.01 and 0.27 USD per share, which slightly distorts the stock gap on the ex-dividend dates.

**Selection.** The threshold of 5,000 trades per month and the exclusion of crypto-related companies are decisions, not facts. A different threshold would add or remove tokens.

**Not investment advice.** This is a data analysis project.

## Repository and files

| File | Content |
|---|---|
| `tokenized_vs_nasdaq_after_hours.ipynb` | The full analysis in 20 sections: selection, data quality, cleaning, the seven questions, limitations, findings |
| `app.py` | Interactive dashboard (Streamlit and Plotly), in English and German, with filters, KPIs, a single-night view and a trading test with a cost slider |
| `sql/` | The two Dune queries behind the token data |
| `data/raw/` | Unchanged exports from Dune and Yahoo Finance |
| `data/clean/` | Cleaned tables written by the notebook |
| `figures/` | Six charts written by the notebook |
| `requirements.txt`, `.streamlit/config.toml` | Python packages and the colours of the dashboard |

The dashboard runs online (link at the top of this page). To run it locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The same installation covers the notebook. Start it from the repository folder, because it reads its data from `data/raw/`.

### Dune queries

| Query | Dune query ID | Output file |
|---|---|---|
| `xstocks_solana_30min_prices_by_quote` | 8887243 | `xstocks_solana_30min_by_quote_2025-06-30_2026-09-30.csv.gz` |
| `xstocks_solana_monthly_overview_fees` | 8887198 | `xstocks_solana_monthly_overview_fees.csv` |

The SQL files are in `sql/`: `xstocks_solana_30min_prices_by_quote.sql` and `xstocks_solana_monthly_overview_fees.sql`.

### Files in `data/raw/`

| File | Rows | Content |
|---|---|---|
| `xstocks_solana_30min_by_quote_2025-06-30_2026-09-30.csv.gz` | 276,486 | 30-minute prices and volume of the five tokens, split by quote type (stablecoin, SOL, other). Gzip-compressed to stay below GitHub's upload limit; pandas reads it directly |
| `xstocks_solana_monthly_overview_fees.csv` | 1,829 | Monthly trades and volume by venue for all tokens with the xStocks mint prefix. Basis of the token selection |
| `stocks_1h_prepost_2025-07-01_2026-09-30.csv` | 26,204 | Hourly stock bars of the five shares |

### Files in `data/clean/`

| File | Rows | Content |
|---|---|---|
| `tokens_30min_clean.csv` | 108,000 | One row per token and half-hour, with the stablecoin price, an outlier flag and labels for the market phase |
| `stocks_1h_clean.csv` | 26,204 | Hourly stock bars with session label and a flag for bad ticks outside market hours |
| `stocks_daily_open_close.csv` | 1,575 | Official open and close per share and trading day |
| `nights.csv` | 1,550 | One row per share and closed period: 310 periods times five shares |

## Sources

Accessed on 2 and 3 October 2026.

1. Solana Foundation, "xStocks: Tokenizing Equities on Solana" (case study): launch date, mint addresses, backing, trading venues. https://solana.com/news/case-study-xstocks
2. Kraken, "xStocks Risk Disclosure": issuer, backing, holder rights, restricted countries, risks. https://www.kraken.com/legal/xstocks
3. xStocks website: issuer and distribution entities, restriction for US persons. https://xstocks.fi/
4. Kraken Blog, "Kraken to acquire Backed", 2 December 2025. https://blog.kraken.com/news/backed-acquisition
5. Nasdaq, stock market holiday schedule and trading hours. https://www.nasdaq.com/market-activity/stock-market-holiday-schedule
6. StockAnalysis, company profiles with exchange, ticker and ISIN: [TSLA](https://stockanalysis.com/stocks/tsla/company/), [NVDA](https://stockanalysis.com/stocks/nvda/company/), [GOOGL](https://stockanalysis.com/stocks/googl/company/), [AAPL](https://stockanalysis.com/stocks/aapl/company/), [AMZN](https://stockanalysis.com/stocks/amzn/company/)
7. SolanaFloor, "Solana Tokenization Roundup: June 2026": Solana's share of tokenized stock trading volume. https://solanafloor.com/news/solana-tokenization-roundup-june-2026
8. Dune Docs, `dex_solana.trades`: table and column definitions. https://docs.dune.com/data-catalog/curated/dex-trades/solana/solana-dex-trades
9. yfinance documentation, `download`: parameters `prepost` and `auto_adjust`. https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html
10. CoinGecko, "What Are Tokenized Stocks and Top Platforms to Get Started": other issuers. https://www.coingecko.com/learn/what-are-tokenized-stocks
11. Kraken, "Alphabet (Class A) (GOOGLx) tokenized stock": share class of the Alphabet token. https://www.kraken.com/xstocks/googlx

## About this project

Code and texts were written with AI assistance and checked by me against the data. How I work with AI is described in my repository [local-ai-workflow](https://github.com/Amirhouschang/local-ai-workflow).

Feedback is welcome through GitHub issues.

## Rights

© 2026 Amirhoushang Rahmannejad. All rights reserved. You are welcome to read and review this project. Copying, modifying or redistributing it requires my written permission.
