"""Interactive dashboard: tokenized stocks on Solana vs. Nasdaq outside US market hours.

Run with:  streamlit run app.py
Reads the cleaned tables written by the notebook into data/clean/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

CLEAN_DIR = Path("data/clean")
NY = "America/New_York"
ORDER = ["TSLA", "NVDA", "GOOGL", "AAPL", "AMZN"]
NIGHT_TYPES = ["overnight", "weekend", "holiday"]

# Colours follow the entity, never its rank: a stock keeps its colour under every filter
STOCK_COLORS = {"TSLA": "#2a78d6", "NVDA": "#eb6834", "GOOGL": "#1baf7a", "AAPL": "#eda100", "AMZN": "#e87ba4"}
NIGHT_COLORS = {"overnight": "#2a78d6", "weekend": "#eb6834", "holiday": "#1baf7a"}
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID, SHADE = "#0b0b0b", "#52514e", "#e4e3df", "#f0efec"

# ----------------------------------------------------------------------------- texts
TEXT = {
    "en": {
        "page_title": "Tokenized Stocks vs. Nasdaq",
        "title": "Tokenized Stocks on Solana vs. Nasdaq",
        "subtitle": "What happens to the price while the stock exchange is closed?",
        "intro": "Nasdaq trades from 9:30 to 16:00 New York time. Tokenized versions of the same shares trade "
                 "around the clock on the Solana blockchain. This dashboard compares five tokens with their "
                 "shares over every night, weekend and public holiday from 8 July 2025 to 30 September 2026.",
        "f_stocks": "Stocks", "f_types": "Type of closed period", "f_dates": "Period",
        "overnight": "Regular night", "weekend": "Weekend", "holiday": "Break with a holiday",
        "no_data": "No closed periods match the filters. Please widen the selection.",
        "k_n": "Closed periods", "k_n_help": "One closed period = from one closing bell to the next opening bell, per stock.",
        "k_corr": "Correlation", "k_corr_help": "Correlation between the token's move while Nasdaq is closed and the stock's gap from close to open. 1 = identical moves.",
        "k_err": "Token forecast error", "k_err_help": "Median distance between the token price shortly before the open and the real opening price.",
        "k_err_vs": "yesterday's close: {v} %",
        "k_dir": "Same direction", "k_dir_help": "Share of closed periods in which token and stock moved in the same direction. Only periods with a stock gap of at least 0.5 %.",
        "k_range": "Token range while closed", "k_range_help": "Median distance between the highest and lowest token price during a closed period.",
        "tab_overview": "Overview", "tab_night": "Single night", "tab_time": "Over time",
        "tab_profile": "Course of a night", "tab_trade": "Trading test", "tab_data": "Data and method",
        "ov_scatter": "Token move while closed vs. the stock's opening gap",
        "ov_scatter_note": "One dot per stock and closed period. Dots on the diagonal mean the token moved exactly as far as the stock later gapped.",
        "ax_token_move": "Token move, close to pre-open (%)", "ax_stock_gap": "Stock gap, close to open (%)",
        "ov_bar": "How well is the opening price predicted?",
        "ov_bar_note": "Median error in % of two forecasts for the opening price. Lower is better.",
        "s_naive": "Yesterday's close", "s_token": "Token before the open",
        "ax_error": "Median absolute error (%)",
        "ov_read_trad": "**If you come from the stock market:** the token works like an around-the-clock indication for the share. Its price before the opening bell already contains most of the overnight news.",
        "ov_read_crypto": "**If you come from crypto:** these tokens are backed by real shares, so their price is anchored to Nasdaq. The on-chain market does the price discovery while the exchange is closed, and Nasdaq confirms it at the open.",
        "n_stock": "Stock", "n_sort": "Order of the list", "n_sort_gap": "Largest opening gap first", "n_sort_date": "By date",
        "n_pick": "Closed period", "n_title": "{ticker}: token and stock from {d1} to {d2}",
        "n_note": "Grey area: Nasdaq is closed. The stock line outside the regular session shows pre-market and post-market prices from Yahoo Finance, where available. Times are New York time.",
        "s_token_line": "Token (30-minute average)", "s_stock_line": "Stock (hourly)",
        "m_close": "Close", "m_open": "Open",
        "ax_price": "Price (USD)", "ax_time_ny": "New York time",
        "nk_gap": "Stock gap", "nk_move": "Token move", "nk_err": "Token vs. opening price", "nk_vol": "Token volume while closed",
        "t_err": "Token forecast error by month", "t_err_note": "Median distance between the token price before the open and the real opening price, per month.",
        "t_vol": "Token trading volume while Nasdaq is closed", "t_vol_note": "USD volume against stablecoins during closed periods, per month. The market grew strongly in 2026.",
        "ax_month": "Month", "ax_volume": "Volume (million USD)",
        "p_title": "Distance to the next opening price during a regular night",
        "p_note": "Regular nights only (17.5 hours). The token price approaches the next opening price mainly in the pre-market hours.",
        "ax_distance": "Median distance to next open (%)",
        "p_vol": "When are the tokens traded during the night?", "ax_vol_share": "Share of night volume (%)",
        "ph_post": "Post-market", "ph_closed": "Stock market fully closed", "ph_pre": "Pre-market",
        "tick_close": "16:00<br>close", "tick_open": "09:30<br>open",
        "tr_intro": "Test of a simple strategy: buy the token in the last half-hour before the close, sell it in the first half-hour after the next open, in every closed period.",
        "tr_cost": "Round-trip trading cost (%)",
        "tr_cost_help": "Fees and price impact for buying and selling together. Dune does not provide pool fees for these tokens, so this is a scenario.",
        "tr_bar": "Mean return per closed period after costs", "ax_net": "Mean net return (%)",
        "tr_line": "Cumulative return of the strategy", "tr_line_note": "Sum of the returns per closed period, average of the selected stocks. The stock line shows what the shares themselves gained from close to open, without costs.",
        "s_gross": "Token strategy before costs", "s_net": "Token strategy after costs", "s_stock_on": "Stock, close to open",
        "ax_cum": "Cumulative return (%)", "ax_date": "Date",
        "tr_k_gross": "Mean return before costs", "tr_k_net": "Mean return after costs", "tr_k_win": "Periods with a profit after costs",
        "tr_result_pos": "At this cost level the strategy earns money on average for: {names}.",
        "tr_result_neg": "At this cost level the strategy loses money on average for every selected stock.",
        "tr_caveat": "The return before costs is not a token effect: the shares themselves rose by a similar amount overnight in this period.",
        "d_table": "Closed periods (filtered)", "d_download": "Download table as CSV",
        "d_cols": {"ticker": "Stock", "prev_trading_day": "Close on", "next_trading_day": "Open on", "night_type": "Type",
                   "stock_close": "Stock close", "stock_open": "Stock open", "token_close": "Token at close",
                   "token_pre_open": "Token before open", "stock_gap_pct": "Stock gap %", "token_move_pct": "Token move %",
                   "pre_open_error_pct": "Token vs. open %", "token_range_pct": "Token range %",
                   "coverage_pct": "Half-hours with price %", "token_volume_usd": "Token volume USD"},
        "d_gloss": "Glossary for both worlds",
        "d_gloss_trad": "**Terms from crypto**\n\n- **Tokenized stock:** a blockchain token backed 1:1 by a real share held by a custodian. Here: xStocks, issued by Backed.\n- **Solana:** the blockchain on which these tokens are traded.\n- **DEX:** decentralized exchange. Trades run against a liquidity pool instead of an order book.\n- **Stablecoin:** a token pegged to the US dollar (USDC, USDT). Token prices here are prices against stablecoins.\n- **Liquidity:** the money available in a pool. Thin pools mean larger price jumps per trade.",
        "d_gloss_crypto": "**Terms from the stock market**\n\n- **Regular session:** Nasdaq trades from 9:30 to 16:00 New York time.\n- **Pre-market and post-market:** limited trading from 4:00 to 9:30 and from 16:00 to 20:00, with less volume.\n- **Opening gap:** the jump between yesterday's closing price and today's opening price.\n- **Closed period:** the time between a close and the next open: a night (17.5 hours), a weekend (about 65 hours) or longer with a holiday.\n- **Basis:** the difference between the token price and the share price at the same moment.",
        "d_method": "Method and limits",
        "d_method_text": "- **Token prices:** 30-minute volume-weighted average prices of DEX trades against stablecoins, from Dune (`dex_solana.trades`).\n- **Stock prices:** hourly bars from Yahoo Finance, including pre-market and post-market. Opening and closing prices come from the regular session.\n- **Selection:** the five tokens are the only well-known single companies without a crypto link among the ten xStocks tokens with at least 5,000 trades in every month.\n- **Limits:** 15 months of data, only 56 weekends and 11 breaks with a holiday. Trading costs are scenarios, not measurements. Prices are averages, not executable quotes. Dividends are not adjusted.\n- **Not investment advice.** This is a data analysis project.",
        "footer": "Data: Dune and Yahoo Finance · Period: 8 July 2025 to 30 September 2026 · Analysis: Amirhoushang Rahmannejad",
    },
    "de": {
        "page_title": "Tokenisierte Aktien vs. Nasdaq",
        "title": "Tokenisierte Aktien auf Solana vs. Nasdaq",
        "subtitle": "Was passiert mit dem Preis, während die Börse geschlossen ist?",
        "intro": "Die Nasdaq handelt von 9:30 bis 16:00 Uhr New Yorker Zeit. Tokenisierte Versionen derselben Aktien "
                 "werden auf der Solana-Blockchain rund um die Uhr gehandelt. Dieses Dashboard vergleicht fünf Token "
                 "mit ihren Aktien über jede Nacht, jedes Wochenende und jeden Feiertag vom 8. Juli 2025 bis 30. September 2026.",
        "f_stocks": "Aktien", "f_types": "Art der Börsenpause", "f_dates": "Zeitraum",
        "overnight": "Normale Nacht", "weekend": "Wochenende", "holiday": "Pause mit Feiertag",
        "no_data": "Keine Börsenpause passt zu den Filtern. Bitte die Auswahl erweitern.",
        "k_n": "Börsenpausen", "k_n_help": "Eine Börsenpause = von einer Schlussglocke bis zur nächsten Eröffnung, je Aktie.",
        "k_corr": "Korrelation", "k_corr_help": "Korrelation zwischen der Token-Bewegung während der Börsenpause und dem Sprung der Aktie von Schluss zu Eröffnung. 1 = identische Bewegung.",
        "k_err": "Prognosefehler des Tokens", "k_err_help": "Mittlerer Abstand zwischen dem Token-Preis kurz vor der Eröffnung und dem echten Eröffnungskurs (Median).",
        "k_err_vs": "Vortagesschluss: {v} %",
        "k_dir": "Gleiche Richtung", "k_dir_help": "Anteil der Börsenpausen, in denen Token und Aktie in dieselbe Richtung liefen. Nur Pausen mit einem Aktiensprung von mindestens 0,5 %.",
        "k_range": "Token-Spanne in der Pause", "k_range_help": "Mittlerer Abstand zwischen höchstem und tiefstem Token-Preis während einer Börsenpause (Median).",
        "tab_overview": "Überblick", "tab_night": "Einzelne Nacht", "tab_time": "Zeitverlauf",
        "tab_profile": "Verlauf einer Nacht", "tab_trade": "Handelstest", "tab_data": "Daten und Methode",
        "ov_scatter": "Token-Bewegung in der Börsenpause gegen den Eröffnungssprung der Aktie",
        "ov_scatter_note": "Ein Punkt je Aktie und Börsenpause. Punkte auf der Diagonale bedeuten: Der Token bewegte sich genau so weit, wie die Aktie später sprang.",
        "ax_token_move": "Token-Bewegung, Schluss bis vor Eröffnung (%)", "ax_stock_gap": "Aktiensprung, Schluss bis Eröffnung (%)",
        "ov_bar": "Wie gut wird der Eröffnungskurs vorhergesagt?",
        "ov_bar_note": "Mittlerer Fehler in % von zwei Prognosen für den Eröffnungskurs (Median). Niedriger ist besser.",
        "s_naive": "Schlusskurs vom Vortag", "s_token": "Token vor der Eröffnung",
        "ax_error": "Mittlerer absoluter Fehler (%)",
        "ov_read_trad": "**Wenn Sie vom Aktienmarkt kommen:** Der Token wirkt wie eine Indikation für die Aktie rund um die Uhr. Sein Preis vor der Eröffnung enthält schon den größten Teil der Nachrichten aus der Nacht.",
        "ov_read_crypto": "**Wenn Sie aus der Krypto-Welt kommen:** Diese Token sind durch echte Aktien gedeckt, ihr Preis hängt deshalb an der Nasdaq. Der On-Chain-Markt übernimmt die Preisfindung, solange die Börse zu ist, und die Nasdaq bestätigt sie bei der Eröffnung.",
        "n_stock": "Aktie", "n_sort": "Reihenfolge der Liste", "n_sort_gap": "Größter Eröffnungssprung zuerst", "n_sort_date": "Nach Datum",
        "n_pick": "Börsenpause", "n_title": "{ticker}: Token und Aktie vom {d1} bis {d2}",
        "n_note": "Graue Fläche: Die Nasdaq ist geschlossen. Die Aktienlinie außerhalb der regulären Sitzung zeigt Vor- und Nachbörsenkurse von Yahoo Finance, soweit vorhanden. Zeiten in New Yorker Zeit.",
        "s_token_line": "Token (30-Minuten-Durchschnitt)", "s_stock_line": "Aktie (stündlich)",
        "m_close": "Schluss", "m_open": "Eröffnung",
        "ax_price": "Preis (USD)", "ax_time_ny": "New Yorker Zeit",
        "nk_gap": "Aktiensprung", "nk_move": "Token-Bewegung", "nk_err": "Token gegen Eröffnungskurs", "nk_vol": "Token-Volumen in der Pause",
        "t_err": "Prognosefehler des Tokens je Monat", "t_err_note": "Mittlerer Abstand zwischen Token-Preis vor der Eröffnung und echtem Eröffnungskurs, je Monat (Median).",
        "t_vol": "Token-Handelsvolumen, während die Nasdaq geschlossen ist", "t_vol_note": "USD-Volumen gegen Stablecoins in den Börsenpausen, je Monat. Der Markt ist 2026 stark gewachsen.",
        "ax_month": "Monat", "ax_volume": "Volumen (Mio. USD)",
        "p_title": "Abstand zum nächsten Eröffnungskurs im Verlauf einer normalen Nacht",
        "p_note": "Nur normale Nächte (17,5 Stunden). Der Token-Preis nähert sich dem nächsten Eröffnungskurs vor allem in der Vorbörse.",
        "ax_distance": "Mittlerer Abstand zur Eröffnung (%)",
        "p_vol": "Wann werden die Token in der Nacht gehandelt?", "ax_vol_share": "Anteil am Nachtvolumen (%)",
        "ph_post": "Nachbörse", "ph_closed": "Börse ganz geschlossen", "ph_pre": "Vorbörse",
        "tick_close": "16:00<br>Schluss", "tick_open": "09:30<br>Eröffnung",
        "tr_intro": "Test einer einfachen Strategie: den Token in der letzten halben Stunde vor Börsenschluss kaufen und in der ersten halben Stunde nach der nächsten Eröffnung verkaufen, in jeder Börsenpause.",
        "tr_cost": "Handelskosten für Kauf und Verkauf zusammen (%)",
        "tr_cost_help": "Gebühren und Preiswirkung für Kauf und Verkauf zusammen. Dune liefert für diese Token keine Pool-Gebühren, deshalb ist das ein Szenario.",
        "tr_bar": "Mittlere Rendite je Börsenpause nach Kosten", "ax_net": "Mittlere Nettorendite (%)",
        "tr_line": "Aufsummierte Rendite der Strategie", "tr_line_note": "Summe der Renditen je Börsenpause, Durchschnitt der gewählten Aktien. Die Aktienlinie zeigt, was die Aktien selbst von Schluss zu Eröffnung gewannen, ohne Kosten.",
        "s_gross": "Token-Strategie vor Kosten", "s_net": "Token-Strategie nach Kosten", "s_stock_on": "Aktie, Schluss bis Eröffnung",
        "ax_cum": "Aufsummierte Rendite (%)", "ax_date": "Datum",
        "tr_k_gross": "Mittlere Rendite vor Kosten", "tr_k_net": "Mittlere Rendite nach Kosten", "tr_k_win": "Pausen mit Gewinn nach Kosten",
        "tr_result_pos": "Bei diesen Kosten verdient die Strategie im Mittel Geld bei: {names}.",
        "tr_result_neg": "Bei diesen Kosten verliert die Strategie im Mittel bei jeder gewählten Aktie Geld.",
        "tr_caveat": "Die Rendite vor Kosten ist kein Token-Effekt: Die Aktien selbst stiegen in diesem Zeitraum über Nacht ähnlich stark.",
        "d_table": "Börsenpausen (gefiltert)", "d_download": "Tabelle als CSV herunterladen",
        "d_cols": {"ticker": "Aktie", "prev_trading_day": "Schluss am", "next_trading_day": "Eröffnung am", "night_type": "Art",
                   "stock_close": "Aktie Schluss", "stock_open": "Aktie Eröffnung", "token_close": "Token bei Schluss",
                   "token_pre_open": "Token vor Eröffnung", "stock_gap_pct": "Aktiensprung %", "token_move_pct": "Token-Bewegung %",
                   "pre_open_error_pct": "Token gegen Eröffnung %", "token_range_pct": "Token-Spanne %",
                   "coverage_pct": "Halbe Stunden mit Preis %", "token_volume_usd": "Token-Volumen USD"},
        "d_gloss": "Glossar für beide Welten",
        "d_gloss_trad": "**Begriffe aus der Krypto-Welt**\n\n- **Tokenisierte Aktie:** ein Blockchain-Token, der 1:1 durch eine echte Aktie bei einem Verwahrer gedeckt ist. Hier: xStocks, ausgegeben von Backed.\n- **Solana:** die Blockchain, auf der diese Token gehandelt werden.\n- **DEX:** dezentrale Börse. Gehandelt wird gegen einen Liquiditätspool statt über ein Orderbuch.\n- **Stablecoin:** ein Token, der an den US-Dollar gebunden ist (USDC, USDT). Die Token-Preise hier sind Preise gegen Stablecoins.\n- **Liquidität:** das Geld, das in einem Pool bereitliegt. Dünne Pools bedeuten größere Preissprünge je Trade.",
        "d_gloss_crypto": "**Begriffe vom Aktienmarkt**\n\n- **Reguläre Sitzung:** Die Nasdaq handelt von 9:30 bis 16:00 Uhr New Yorker Zeit.\n- **Vorbörse und Nachbörse:** eingeschränkter Handel von 4:00 bis 9:30 Uhr und von 16:00 bis 20:00 Uhr, mit weniger Volumen.\n- **Eröffnungssprung (Gap):** der Sprung zwischen dem Schlusskurs von gestern und dem Eröffnungskurs von heute.\n- **Börsenpause:** die Zeit zwischen Schluss und nächster Eröffnung: eine Nacht (17,5 Stunden), ein Wochenende (rund 65 Stunden) oder länger mit Feiertag.\n- **Basis:** der Unterschied zwischen Token-Preis und Aktienkurs im selben Moment.",
        "d_method": "Methode und Grenzen",
        "d_method_text": "- **Token-Preise:** volumengewichtete 30-Minuten-Durchschnittspreise von DEX-Trades gegen Stablecoins, aus Dune (`dex_solana.trades`).\n- **Aktienkurse:** Stundenkerzen von Yahoo Finance, mit Vor- und Nachbörse. Eröffnungs- und Schlusskurse stammen aus der regulären Sitzung.\n- **Auswahl:** Die fünf Token sind die einzigen bekannten Einzelfirmen ohne Krypto-Bezug unter den zehn xStocks-Token mit mindestens 5.000 Trades in jedem Monat.\n- **Grenzen:** 15 Monate Daten, nur 56 Wochenenden und 11 Pausen mit Feiertag. Handelskosten sind Szenarien, keine Messwerte. Preise sind Durchschnitte, keine handelbaren Kurse. Dividenden sind nicht bereinigt.\n- **Keine Anlageberatung.** Dies ist ein Datenanalyse-Projekt.",
        "footer": "Daten: Dune und Yahoo Finance · Zeitraum: 8. Juli 2025 bis 30. September 2026 · Analyse: Amirhoushang Rahmannejad",
    },
}

st.set_page_config(page_title="Tokenized Stocks vs. Nasdaq", layout="wide")


# ----------------------------------------------------------------------------- data
@st.cache_data
def load_data():
    daily = pd.read_csv(CLEAN_DIR / "stocks_daily_open_close.csv", parse_dates=["day", "open_utc", "close_utc"])
    nights = pd.read_csv(CLEAN_DIR / "nights.csv", parse_dates=["prev_trading_day", "next_trading_day"])
    nights = nights.merge(daily.rename(columns={"day": "prev_trading_day"})[["ticker", "prev_trading_day", "close_utc"]],
                          on=["ticker", "prev_trading_day"])
    nights = nights.merge(daily.rename(columns={"day": "next_trading_day"})[["ticker", "next_trading_day", "open_utc"]],
                          on=["ticker", "next_trading_day"])
    tokens = pd.read_csv(CLEAN_DIR / "tokens_30min_clean.csv", parse_dates=["time_utc", "prev_trading_day"],
                         usecols=["time_utc", "ticker", "price_usd", "volume_usd", "night_type", "prev_trading_day"])
    stocks = pd.read_csv(CLEAN_DIR / "stocks_1h_clean.csv", parse_dates=["time_utc"],
                         usecols=["time_utc", "ticker", "session", "close", "is_spike"])
    return nights, tokens, stocks[~stocks["is_spike"]]


@st.cache_data
def night_profile(tickers):
    """Median distance to the next open and volume share by hours since the close (regular nights)."""
    nights, tokens, _ = load_data()
    regular = nights[(nights["night_type"] == "overnight") & (nights["hours_closed"] == 17.5)
                     & nights["ticker"].isin(tickers)]
    path = tokens[tokens["night_type"] == "overnight"].merge(
        regular[["ticker", "prev_trading_day", "close_utc", "stock_open"]], on=["ticker", "prev_trading_day"])
    path["hours"] = (path["time_utc"] - path["close_utc"]).dt.total_seconds() / 3600
    path["distance"] = 100 * (path["price_usd"] / path["stock_open"] - 1).abs()
    distance = path.pivot_table(index="hours", columns="ticker", values="distance", aggfunc="median")
    volume = 100 * path.groupby("hours")["volume_usd"].sum() / path["volume_usd"].sum()
    return distance, volume


nights_all, tokens_all, stocks_all = load_data()

# ----------------------------------------------------------------------------- language and helpers
head_left, head_right = st.columns([5, 1])
with head_right:
    lang_label = st.radio("Sprache / Language", ["English", "Deutsch"], horizontal=True, label_visibility="collapsed")
LANG = "de" if lang_label == "Deutsch" else "en"
T = TEXT[LANG]


def num(value, digits=2, sign=False):
    """Format a number with the decimal mark of the selected language."""
    if value is None or pd.isna(value):
        return "–"
    text = f"{value:+,.{digits}f}" if sign else f"{value:,.{digits}f}"
    if LANG == "de":
        text = text.replace(",", " ").replace(".", ",").replace(" ", ".")
    return text


def date_text(ts):
    return ts.strftime("%d.%m.%Y") if LANG == "de" else ts.strftime("%d %b %Y")


def style(fig, height=380, legend=True):
    """One look for every chart: light surface, hairline grid, muted axes."""
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=30, b=10), template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=MUTED, size=13), separators=",." if LANG == "de" else ".,",
        showlegend=legend, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""),
        hoverlabel=dict(bgcolor="white", font_size=13),
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=MUTED, zerolinewidth=1)
    return fig


with head_left:
    st.title(T["title"])
    st.subheader(T["subtitle"])
st.write(T["intro"])

# ----------------------------------------------------------------------------- filters (one row above everything)
first_day, last_day = nights_all["prev_trading_day"].min().date(), nights_all["prev_trading_day"].max().date()
f1, f2, f3 = st.columns([2, 2, 3])
sel_stocks = f1.multiselect(T["f_stocks"], ORDER, default=ORDER)
sel_types = f2.multiselect(T["f_types"], NIGHT_TYPES, default=NIGHT_TYPES, format_func=lambda k: T[k])
sel_dates = f3.slider(T["f_dates"], min_value=first_day, max_value=last_day, value=(first_day, last_day),
                      format="DD.MM.YYYY" if LANG == "de" else "YYYY-MM-DD")

nights = nights_all[nights_all["ticker"].isin(sel_stocks) & nights_all["night_type"].isin(sel_types)
                    & (nights_all["prev_trading_day"].dt.date >= sel_dates[0])
                    & (nights_all["prev_trading_day"].dt.date <= sel_dates[1])]
stocks_shown = [s for s in ORDER if s in sel_stocks]
if nights.empty:
    st.warning(T["no_data"])
    st.stop()

# ----------------------------------------------------------------------------- KPI row
valid = nights.dropna(subset=["token_move_pct", "stock_gap_pct"])
real_gap = valid[valid["stock_gap_pct"].abs() >= 0.5]
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric(T["k_n"], num(len(nights), 0), help=T["k_n_help"])
k2.metric(T["k_corr"], num(valid["token_move_pct"].corr(valid["stock_gap_pct"])), help=T["k_corr_help"])
k3.metric(T["k_err"], f"{num(valid['pre_open_error_pct'].abs().median())} %",
          delta=T["k_err_vs"].format(v=num(valid["stock_gap_pct"].abs().median())), delta_color="off",
          delta_arrow="off", help=T["k_err_help"])
k4.metric(T["k_dir"], f"{num(100 * (np.sign(real_gap['token_move_pct']) == np.sign(real_gap['stock_gap_pct'])).mean(), 1)} %"
          if len(real_gap) else "–", help=T["k_dir_help"])
k5.metric(T["k_range"], f"{num(nights['token_range_pct'].median())} %", help=T["k_range_help"])

tabs = st.tabs([T["tab_overview"], T["tab_night"], T["tab_time"], T["tab_profile"], T["tab_trade"], T["tab_data"]])

# ----------------------------------------------------------------------------- tab 1: overview
with tabs[0]:
    left, right = st.columns(2)
    with left:
        st.markdown(f"**{T['ov_scatter']}**")
        limit = float(np.ceil(max(valid["token_move_pct"].abs().quantile(0.995),
                                  valid["stock_gap_pct"].abs().quantile(0.995), 2)))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[-limit, limit], y=[-limit, limit], mode="lines", hoverinfo="skip",
                                 line=dict(color=MUTED, width=1), showlegend=False))
        for kind in [k for k in NIGHT_TYPES if k in sel_types]:
            g = valid[valid["night_type"] == kind]
            fig.add_trace(go.Scatter(
                x=g["token_move_pct"], y=g["stock_gap_pct"], mode="markers", name=T[kind],
                marker=dict(color=NIGHT_COLORS[kind], size=8, opacity=0.7, line=dict(color="white", width=1)),
                customdata=np.stack([g["ticker"], g["prev_trading_day"].dt.strftime("%Y-%m-%d"),
                                     g["next_trading_day"].dt.strftime("%Y-%m-%d")], axis=-1),
                hovertemplate="<b>%{customdata[0]}</b> %{customdata[1]} → %{customdata[2]}<br>"
                              + T["ax_token_move"] + ": %{x:.2f}<br>" + T["ax_stock_gap"] + ": %{y:.2f}<extra></extra>"))
        fig.update_xaxes(title_text=T["ax_token_move"], range=[-limit, limit])
        fig.update_yaxes(title_text=T["ax_stock_gap"], range=[-limit, limit])
        st.plotly_chart(style(fig, 430), width="stretch")
        st.caption(T["ov_scatter_note"])
    with right:
        st.markdown(f"**{T['ov_bar']}**")
        err = valid.groupby("ticker").agg(naive=("stock_gap_pct", lambda s: s.abs().median()),
                                          token=("pre_open_error_pct", lambda s: s.abs().median())).reindex(stocks_shown)
        fig = go.Figure()
        for column, name, color in [("naive", T["s_naive"], ORANGE), ("token", T["s_token"], BLUE)]:
            fig.add_trace(go.Bar(x=err.index, y=err[column], name=name, marker_color=color,
                                 marker_line=dict(color="white", width=2),
                                 text=[num(v) for v in err[column]], textposition="outside", textfont=dict(color=MUTED),
                                 hovertemplate="%{x} · " + name + ": %{y:.2f} %<extra></extra>"))
        fig.update_layout(barmode="group", bargap=0.3)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(title_text=T["ax_error"], rangemode="tozero")
        st.plotly_chart(style(fig, 430), width="stretch")
        st.caption(T["ov_bar_note"])
    c1, c2 = st.columns(2)
    c1.info(T["ov_read_trad"])
    c2.info(T["ov_read_crypto"])

# ----------------------------------------------------------------------------- tab 2: single night
with tabs[1]:
    a, b, c = st.columns([1, 2, 4])
    stock = a.selectbox(T["n_stock"], stocks_shown)
    sort_by = b.radio(T["n_sort"], ["gap", "date"], horizontal=True,
                      format_func=lambda k: T["n_sort_gap"] if k == "gap" else T["n_sort_date"])
    pool = nights[nights["ticker"] == stock].dropna(subset=["token_close", "token_pre_open"])
    pool = (pool.reindex(pool["stock_gap_pct"].abs().sort_values(ascending=False).index) if sort_by == "gap"
            else pool.sort_values("prev_trading_day"))
    if pool.empty:
        st.warning(T["no_data"])
    else:
        choice = c.selectbox(
            T["n_pick"], pool.index,
            format_func=lambda i: f"{date_text(pool.loc[i, 'prev_trading_day'])} → {date_text(pool.loc[i, 'next_trading_day'])}"
                                  f" · {T[pool.loc[i, 'night_type']]} · {T['nk_gap']} {num(pool.loc[i, 'stock_gap_pct'], 2, True)} %")
        row = pool.loc[choice]
        t0, t1 = row["close_utc"] - pd.Timedelta("3h"), row["open_utc"] + pd.Timedelta("3h")
        tok = tokens_all[(tokens_all["ticker"] == stock) & (tokens_all["time_utc"] >= t0)
                         & (tokens_all["time_utc"] <= t1)].dropna(subset=["price_usd"])
        stk = stocks_all[(stocks_all["ticker"] == stock) & (stocks_all["time_utc"] >= t0 - pd.Timedelta("1h"))
                         & (stocks_all["time_utc"] <= t1)].copy()
        # a bar's close is the price at the end of the bar: the last regular bar is 30 minutes, the others 60
        stk["end_utc"] = stk["time_utc"] + pd.to_timedelta(
            np.where((stk["session"] == "market_hours") & (stk["time_utc"].dt.tz_convert(NY).dt.strftime("%H:%M") == "15:30")
                     | (stk["time_utc"].dt.tz_convert(NY).dt.strftime("%H:%M") == "09:00"), 30, 60), unit="min")
        stk = stk[(stk["end_utc"] >= t0) & (stk["end_utc"] <= t1)]

        k = st.columns(4)
        k[0].metric(T["nk_gap"], f"{num(row['stock_gap_pct'], 2, True)} %")
        k[1].metric(T["nk_move"], f"{num(row['token_move_pct'], 2, True)} %")
        k[2].metric(T["nk_err"], f"{num(row['pre_open_error_pct'], 2, True)} %")
        k[3].metric(T["nk_vol"], f"{num(row['token_volume_usd'], 0)} USD")

        st.markdown("**" + T["n_title"].format(ticker=stock, d1=date_text(row["prev_trading_day"]),
                                              d2=date_text(row["next_trading_day"])) + "**")
        fig = go.Figure()
        fig.add_vrect(x0=row["close_utc"].tz_convert(NY), x1=row["open_utc"].tz_convert(NY),
                      fillcolor=SHADE, opacity=1, line_width=0, layer="below")
        fig.add_trace(go.Scatter(x=tok["time_utc"].dt.tz_convert(NY) + pd.Timedelta("15min"), y=tok["price_usd"],
                                 mode="lines", name=T["s_token_line"], line=dict(color=BLUE, width=2),
                                 hovertemplate="%{y:.2f} USD<extra>" + T["s_token_line"] + "</extra>"))
        fig.add_trace(go.Scatter(x=stk["end_utc"].dt.tz_convert(NY), y=stk["close"], mode="lines+markers",
                                 name=T["s_stock_line"], line=dict(color=ORANGE, width=2), marker=dict(size=6),
                                 hovertemplate="%{y:.2f} USD<extra>" + T["s_stock_line"] + "</extra>"))
        for label, when, price, position in [(T["m_close"], row["close_utc"], row["stock_close"], "top left"),
                                             (T["m_open"], row["open_utc"], row["stock_open"], "top right")]:
            fig.add_trace(go.Scatter(x=[when.tz_convert(NY)], y=[price], mode="markers+text", showlegend=False,
                                     marker=dict(color=ORANGE, size=12, line=dict(color="white", width=2)),
                                     text=[f"{label} {num(price)}"], textposition=position, textfont=dict(color=INK),
                                     hovertemplate=label + ": %{y:.2f} USD<extra></extra>"))
        fig.update_xaxes(title_text=T["ax_time_ny"],
                         tickformat="%H:%M<br>%d.%m." if LANG == "de" else "%H:%M<br>%d %b",
                         hoverformat="%d.%m.%Y %H:%M" if LANG == "de" else "%d %b %Y %H:%M")
        fig.update_yaxes(title_text=T["ax_price"])
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(style(fig, 460), width="stretch")
        st.caption(T["n_note"])

# ----------------------------------------------------------------------------- tab 3: over time
with tabs[2]:
    monthly = nights.assign(month=nights["next_trading_day"].dt.to_period("M").dt.to_timestamp())
    err_m = monthly.assign(e=monthly["pre_open_error_pct"].abs()).pivot_table(
        index="month", columns="ticker", values="e", aggfunc="median")
    vol_m = monthly.pivot_table(index="month", columns="ticker", values="token_volume_usd", aggfunc="sum") / 1e6
    month_format = "%m.%Y" if LANG == "de" else "%b %Y"

    st.markdown(f"**{T['t_err']}**")
    fig = go.Figure()
    for ticker in stocks_shown:
        fig.add_trace(go.Scatter(x=err_m.index, y=err_m[ticker], mode="lines+markers", name=ticker,
                                 line=dict(color=STOCK_COLORS[ticker], width=2), marker=dict(size=6),
                                 hovertemplate=ticker + ": %{y:.2f} %<extra></extra>"))
    fig.update_xaxes(title_text=T["ax_month"], tickformat=month_format, hoverformat=month_format)
    fig.update_yaxes(title_text=T["ax_error"], rangemode="tozero")
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(style(fig), width="stretch")
    st.caption(T["t_err_note"])

    st.markdown(f"**{T['t_vol']}**")
    fig = go.Figure()
    for ticker in stocks_shown:
        fig.add_trace(go.Scatter(x=vol_m.index, y=vol_m[ticker], mode="lines+markers", name=ticker,
                                 line=dict(color=STOCK_COLORS[ticker], width=2), marker=dict(size=6),
                                 hovertemplate=ticker + ": %{y:.1f}<extra></extra>"))
    fig.update_xaxes(title_text=T["ax_month"], tickformat=month_format, hoverformat=month_format)
    fig.update_yaxes(title_text=T["ax_volume"], rangemode="tozero")
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(style(fig), width="stretch")
    st.caption(T["t_vol_note"])

# ----------------------------------------------------------------------------- tab 4: course of a night
with tabs[3]:
    distance, volume = night_profile(tuple(stocks_shown))
    ticks = [0, 4, 8, 12, 17.5]
    tick_text = [T["tick_close"], "20:00", "00:00", "04:00", T["tick_open"]]

    st.markdown(f"**{T['p_title']}**")
    fig = go.Figure()
    fig.add_vrect(x0=4, x1=12, fillcolor=SHADE, opacity=1, line_width=0, layer="below")
    for ticker in stocks_shown:
        fig.add_trace(go.Scatter(x=distance.index, y=distance[ticker], mode="lines", name=ticker,
                                 line=dict(color=STOCK_COLORS[ticker], width=2),
                                 hovertemplate=ticker + ": %{y:.2f} %<extra></extra>"))
    for x_pos, label in [(2, T["ph_post"]), (8, T["ph_closed"]), (14.75, T["ph_pre"])]:
        fig.add_annotation(x=x_pos, y=1, yref="paper", text=label, showarrow=False, font=dict(color=MUTED, size=12),
                           yanchor="top")
    fig.update_xaxes(tickvals=ticks, ticktext=tick_text, range=[-0.4, 18.3], showgrid=False, title_text=T["ax_time_ny"])
    fig.update_yaxes(title_text=T["ax_distance"], rangemode="tozero")
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(style(fig, 420), width="stretch")
    st.caption(T["p_note"])

    st.markdown(f"**{T['p_vol']}**")
    fig = go.Figure(go.Bar(x=volume.index + 0.25, y=volume, marker_color=BLUE, marker_line=dict(color="white", width=2),
                           hovertemplate="%{y:.1f} %<extra></extra>"))
    fig.add_vrect(x0=4, x1=12, fillcolor=SHADE, opacity=1, line_width=0, layer="below")
    fig.update_xaxes(tickvals=ticks, ticktext=tick_text, range=[-0.4, 18.3], showgrid=False, title_text=T["ax_time_ny"])
    fig.update_yaxes(title_text=T["ax_vol_share"])
    st.plotly_chart(style(fig, 280, legend=False), width="stretch")

# ----------------------------------------------------------------------------- tab 5: trading test
with tabs[4]:
    st.write(T["tr_intro"])
    cost = st.slider(T["tr_cost"], 0.0, 1.0, 0.3, 0.05, help=T["tr_cost_help"])
    trades = nights.dropna(subset=["trade_pct"]).copy()
    trades["net_pct"] = trades["trade_pct"] - cost

    k = st.columns(3)
    k[0].metric(T["tr_k_gross"], f"{num(trades['trade_pct'].mean(), 2, True)} %")
    k[1].metric(T["tr_k_net"], f"{num(trades['net_pct'].mean(), 2, True)} %")
    k[2].metric(T["tr_k_win"], f"{num(100 * (trades['net_pct'] > 0).mean(), 1)} %")

    left, right = st.columns(2)
    with left:
        st.markdown(f"**{T['tr_bar']}**")
        net = trades.groupby("ticker")["net_pct"].mean().reindex(stocks_shown)
        fig = go.Figure(go.Bar(x=net.index, y=net, marker_color=BLUE, marker_line=dict(color="white", width=2),
                               text=[num(v, 2, True) for v in net], textposition="outside", textfont=dict(color=MUTED),
                               hovertemplate="%{x}: %{y:.2f} %<extra></extra>"))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(title_text=T["ax_net"])
        st.plotly_chart(style(fig, 400, legend=False), width="stretch")
        winners = [s for s in stocks_shown if net[s] > 0]
        st.caption(T["tr_result_pos"].format(names=", ".join(winners)) if winners else T["tr_result_neg"])
    with right:
        st.markdown(f"**{T['tr_line']}**")
        by_day = trades.groupby("next_trading_day").agg(gross=("trade_pct", "mean"), net=("net_pct", "mean"),
                                                        stock=("stock_gap_pct", "mean")).sort_index().cumsum()
        fig = go.Figure()
        for column, name, color in [("gross", T["s_gross"], BLUE), ("net", T["s_net"], ORANGE),
                                    ("stock", T["s_stock_on"], AQUA)]:
            fig.add_trace(go.Scatter(x=by_day.index, y=by_day[column], mode="lines", name=name,
                                     line=dict(color=color, width=2),
                                     hovertemplate=name + ": %{y:.1f} %<extra></extra>"))
        fig.update_xaxes(title_text=T["ax_date"], tickformat="%m.%Y" if LANG == "de" else "%b %Y",
                         hoverformat="%d.%m.%Y" if LANG == "de" else "%d %b %Y")
        fig.update_yaxes(title_text=T["ax_cum"])
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(style(fig, 400), width="stretch")
        st.caption(T["tr_line_note"])
    st.info(T["tr_caveat"])

# ----------------------------------------------------------------------------- tab 6: data and method
with tabs[5]:
    st.markdown(f"**{T['d_table']}**")
    columns = list(T["d_cols"].keys())
    table = nights.sort_values(["prev_trading_day", "ticker"])[columns].copy()
    table["prev_trading_day"] = table["prev_trading_day"].dt.date
    table["next_trading_day"] = table["next_trading_day"].dt.date
    table["night_type"] = table["night_type"].map(lambda kind: T[kind])
    st.dataframe(table.rename(columns=T["d_cols"]), width="stretch", hide_index=True, height=420,
                 column_config={T["d_cols"][c]: st.column_config.NumberColumn(format="%.2f") for c in columns
                                if c.endswith("_pct") or c.startswith(("stock_", "token_c", "token_p"))}
                 | {T["d_cols"]["token_volume_usd"]: st.column_config.NumberColumn(format="%.0f")})
    st.download_button(T["d_download"], table.rename(columns=T["d_cols"]).to_csv(index=False).encode("utf-8"),
                       file_name="closed_periods.csv", mime="text/csv")

    with st.expander(T["d_gloss"], expanded=True):
        g1, g2 = st.columns(2)
        g1.markdown(T["d_gloss_trad"])
        g2.markdown(T["d_gloss_crypto"])
    with st.expander(T["d_method"]):
        st.markdown(T["d_method_text"])

st.caption(T["footer"])
