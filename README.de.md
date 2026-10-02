# Tokenisierte Aktien auf Solana vs. Nasdaq: Preisverhalten außerhalb der US-Börsenzeiten

[English](README.md) | **Deutsch**

**Tesla, Nvidia, Alphabet, Apple und Amazon · 8. Juli 2025 bis 30. September 2026**

**Interaktives Dashboard (Deutsch und Englisch):** https://tokenized-vs-nasdaq-stocks-after-hours.streamlit.app

Die Nasdaq handelt von 9:30 bis 16:00 Uhr New Yorker Zeit. Tokenisierte Versionen derselben Aktien werden auf der Solana-Blockchain rund um die Uhr gehandelt. Dieses Projekt vergleicht fünf tokenisierte Aktien mit ihren zugrunde liegenden Aktien und fragt, was mit dem Token-Preis passiert, während die Börse geschlossen ist: über Nacht, am Wochenende und an Feiertagen.

Das Projekt richtet sich an zwei Gruppen: an Leute vom Aktienmarkt, die noch nie eine Blockchain benutzt haben, und an Leute aus der Krypto-Welt, die wissen wollen, wie eng diese Token dem echten Markt folgen. Ein Glossar für beide steht im Dashboard.

## Kernergebnisse

- **Die Token folgen den Aktien eng, solange die Nasdaq offen ist.** Die mittlere absolute Abweichung liegt bei 0,17 % (Nvidia) bis 0,29 % (Amazon).
- **Der Token-Markt bewegt sich weiter, während die Nasdaq geschlossen ist**, und das ist 81 % der Zeit. Die mittlere Preisspanne (Median) liegt bei 1,0 % bis 1,5 % in einer normalen Nacht und bei 1,7 % bis 2,5 % über ein Wochenende.
- **Der Token-Preis nimmt den Eröffnungskurs vorweg.** Die Korrelation zwischen der Token-Bewegung in einer Börsenpause und dem Eröffnungssprung der Aktie liegt bei 0,88 bis 0,96. Wo die Aktie um mindestens 0,5 % sprang, war der Token in 95 % bis 99 % der Fälle vorher in dieselbe Richtung gelaufen.
- **Die Prognose ist gut, aber nicht perfekt.** Der Token-Preis vor der Eröffnung verfehlt den echten Eröffnungskurs im Median um 0,18 % bis 0,30 %. Das ist bei Tesla und Nvidia deutlich besser als der Schlusskurs vom Vortag (0,85 % und 0,83 %), bei Apple aber nur knapp (0,27 % gegen 0,32 %).
- **Die Anpassung passiert spät in der Nacht.** Bei Tesla und Nvidia sinkt der Abstand zum nächsten Eröffnungskurs von rund 0,7 % beim Schluss auf rund 0,5 % um 4:00 Uhr und dann in der Vorbörse auf rund 0,2 %.
- **Es gibt keinen einfachen Handel mit Gewinn.** Beim Schluss kaufen und nach der Eröffnung verkaufen bringt vor Kosten 0,06 % bis 0,18 % je Börsenpause, etwa so viel, wie die Aktien selbst über Nacht gewannen. Bei Kosten von 0,3 % für Kauf und Verkauf zusammen verlieren alle fünf Token Geld.
- **Liquidität zählt.** Der dünn gehandelte Amazon-Token hat den größten Prognosefehler (0,30 %), der stark gehandelte Nvidia-Token den kleinsten (0,18 %).

Die Beschriftung der Charts ist englisch.

![Token-Bewegung gegen Eröffnungssprung](figures/01_token_move_vs_stock_gap.png)

![Prognosefehler für den Eröffnungskurs](figures/02_opening_price_forecast_error.png)

![Preisverlauf in einer normalen Nacht](figures/05_night_path_to_open.png)

![Handelsrendite gegen Kosten](figures/04_overnight_trade_return_vs_costs.png)

## Was in diesem Repository liegt

| Datei | Inhalt |
|---|---|
| `tokenized_vs_nasdaq_after_hours.ipynb` | Die ganze Analyse in 20 Abschnitten: Auswahl, Datenqualität, Bereinigung, sieben Fragen, Grenzen, Ergebnisse (auf Englisch) |
| `app.py` | Interaktives Dashboard (Streamlit und Plotly), auf Englisch und Deutsch, mit Filtern, Kennzahlen, einer Ansicht für einzelne Nächte und einem Handelstest mit Kosten-Regler |
| `sql/` | Die zwei Dune-Abfragen hinter den Token-Daten |
| `data/raw/` | Unveränderte Exporte aus Dune und Yahoo Finance |
| `data/clean/` | Bereinigte Tabellen, die das Notebook schreibt |
| `figures/` | Sechs Charts, die das Notebook schreibt |

Das Dashboard läuft online unter https://tokenized-vs-nasdaq-stocks-after-hours.streamlit.app. Lokal starten:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Die sieben Fragen

| # | Frage | Antwort | Abschnitt im Notebook |
|---|---|---|---|
| 1 | Wie nah ist der Token an der Aktie während der Börsenzeit? | Mittlere absolute Abweichung 0,17 % bis 0,29 % | 12 |
| 2 | Wie weit bewegt sich der Token, während die Nasdaq geschlossen ist? | Spanne im Median 1,0 % bis 1,5 % je Nacht, 1,7 % bis 2,5 % je Wochenende | 13 |
| 3 | Sagt der Token den Eröffnungskurs voraus? | Ja: Korrelation 0,88 bis 0,96, Fehler im Median 0,18 % bis 0,30 % | 14 |
| 4 | Lohnt es sich, beim Schluss zu kaufen und nach der Eröffnung zu verkaufen? | Nein: 0,06 % bis 0,18 % vor Kosten, negativ bei 0,3 % Kosten | 15 |
| 5 | Folgen dünne Token der Aktie schlechter als liquide? | Ja: Prognosefehler und Datenlücken wachsen, wenn das Volumen sinkt | 16 |
| 6 | Wann in der Nacht passt sich der Preis an? | Vor allem in der Vorbörse (4:00 bis 9:30 Uhr) | 17 |
| 7 | Folgt der Token den Kursen der Vor- und Nachbörse? | Etwa so eng wie während der Sitzung | 18 |

## Die fünf Assets

| Token | Mint-Adresse auf Solana | Aktie | Ticker | Börse | ISIN der Aktie |
|---|---|---|---|---|---|
| TSLAx | [`XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB`](https://solscan.io/token/XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB) | Tesla, Inc. | TSLA | Nasdaq | US88160R1014 |
| NVDAx | [`Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh`](https://solscan.io/token/Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh) | NVIDIA Corporation | NVDA | Nasdaq | US67066G1040 |
| GOOGLx | [`XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN`](https://solscan.io/token/XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN) | Alphabet Inc., Class A | GOOGL | Nasdaq | US02079K3059 |
| AAPLx | [`XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp`](https://solscan.io/token/XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp) | Apple Inc. | AAPL | Nasdaq | US0378331005 |
| AMZNx | [`Xs3eBt7uRfJX8QUs4suhyU8p2M6DoUDrJyWBa8LLZsg`](https://solscan.io/token/Xs3eBt7uRfJX8QUs4suhyU8p2M6DoUDrJyWBa8LLZsg) | Amazon.com, Inc. | AMZN | Nasdaq | US0231351067 |

- Die fünf Mint-Adressen stehen in der Fallstudie der Solana Foundation zu xStocks [1].
- Börse, Ticker und ISIN der Aktien: Unternehmensprofile bei StockAnalysis [6].
- Der Alphabet-Token bildet die Class-A-Aktie (GOOGL) ab, nicht die Class-C-Aktie (GOOG).

Token-Aktivität im Analysezeitraum (Trades gegen USD-Stablecoins auf dezentralen Börsen von Solana, eigene Dune-Daten):

| Token | Trades | Volumen (Mio. USD) | Halbe Stunden mit Preis |
|---|---|---|---|
| TSLAx | 3.213.000 | 608,9 | 100,0 % |
| NVDAx | 3.950.211 | 537,7 | 99,9 % |
| GOOGLx | 767.548 | 103,3 | 97,1 % |
| AAPLx | 532.211 | 55,1 | 94,3 % |
| AMZNx | 313.809 | 37,2 | 87,0 % |

## Wer diese Token herausgibt

Alle fünf Token sind **xStocks**.

- **Emittent:** Backed Assets (JE) Limited, eine Gesellschaft mit beschränkter Haftung auf Jersey [2][3].
- **Deckung:** Jeder xStock ist 1:1 durch die zugrunde liegende Aktie gedeckt. Die Aktien liegen bei Verwahrstellen, geregelt durch einen Verwahrvertrag [2]. Laut der Solana-Fallstudie kauft der Emittent die echten Aktien über Broker, hinterlegt sie bei einem regulierten Verwahrer und gibt je Aktie einen Token aus [1].
- **Rechte:** Halter von xStocks besitzen die zugrunde liegenden Aktien nicht und haben weder Stimmrechte noch Ansprüche gegen das Unternehmen [2]. Ein Token gibt die Preisentwicklung wieder, macht aber niemanden zum Aktionär.
- **Verfügbarkeit:** xStocks sind in den USA und für US-Personen nicht verfügbar, ebenso nicht in Kanada, Großbritannien und Australien [2][3].
- **Start:** xStocks starteten am 30. Juni 2025 auf Solana mit mehr als 55 tokenisierten Aktien und ETFs [1]. Dieses Datum ist der früheste mögliche Beginn der Daten.
- **Technik:** Die Token nutzen den Token-2022-Standard von Solana (Token Extensions) [1].
- **Handelsorte:** zentrale Börsen (Kraken, Bybit) und dezentrale Börsen auf Solana wie Raydium, erreichbar über den Aggregator Jupiter [1]. Dieses Projekt nutzt nur dezentrale Trades.
- **Eigentümer des Emittenten:** Am 2. Dezember 2025 gab Kraken bekannt, die Übernahme von Backed vereinbart zu haben, dem Unternehmen hinter xStocks [4].

xStocks ist nicht der einzige Emittent tokenisierter Aktien auf Solana; auch Ondo Global Markets bietet dort zum Beispiel tokenisierte US-Aktien an [10]. Andere Emittenten sind nicht Teil dieses Projekts.

## Warum diese fünf Token

Die Token ergeben sich aus zwei Regeln, angewendet auf jeden Token, dessen Mint-Adresse auf Solana mit `Xs` beginnt, dem Präfix von xStocks (Monatsübersicht aus Dune, 153 Symbole, darunter einige fremde Token mit demselben Präfix):

1. **Durchgehender Handel:** mindestens 5.000 Trades in jedem Monat von Juli 2025 bis September 2026.
2. **Bekannte Einzelfirma ohne Krypto-Bezug**, damit auch Leser außerhalb der Krypto-Szene dem Vergleich folgen können.

Regel 1 lässt zehn Token übrig. Regel 2 entfernt zwei ETFs und drei krypto-nahe Unternehmen.

| Token | Basiswert | Niedrigste Trades in einem Monat | Volumen (Mio. USD) | Entscheidung |
|---|---|---|---|---|
| SPYx | S&P-500-ETF | 110.739 | 2.684,0 | ausgeschlossen: ETF |
| CRCLx | Circle | 56.522 | 1.187,8 | ausgeschlossen: krypto-nah |
| NVDAx | Nvidia | 96.190 | 750,9 | **gewählt** |
| TSLAx | Tesla | 164.118 | 730,5 | **gewählt** |
| QQQx | Nasdaq-100-ETF | 18.174 | 352,8 | ausgeschlossen: ETF |
| MSTRx | Strategy | 43.736 | 310,5 | ausgeschlossen: krypto-nah |
| GOOGLx | Alphabet | 41.533 | 138,1 | **gewählt** |
| HOODx | Robinhood | 6.063 | 90,8 | ausgeschlossen: krypto-nah |
| AAPLx | Apple | 18.036 | 83,2 | **gewählt** |
| AMZNx | Amazon | 8.413 | 53,1 | **gewählt** |

Volumen: alle dezentralen Trades, Juli 2025 bis September 2026. Der Export lässt Gruppen mit weniger als 100 Trades je Monat, Handelsort und Gebührenstufe weg, die Zahlen sind deshalb leicht zu niedrig. Der Ausschluss von Robinhood, einem Broker mit großem Krypto-Geschäft, ist eine Ermessensentscheidung.

Zwei Kandidaten wurden zuerst erwogen und verworfen, weil sie 2025 kaum gehandelt wurden:

| Token | Trades im Juli 2025 | Erster Monat mit mindestens 5.000 Trades |
|---|---|---|
| MSFTx (Microsoft) | 0 | März 2026 |
| MCDx (McDonald's) | 102 | März 2026 |

## Marktumfeld

- **Solana dominiert den On-Chain-Handel mit tokenisierten Aktien.** Im Juni 2026 entfielen laut SolanaFloor rund 94 % bis 96 % des Handelsvolumens tokenisierter Aktien über alle Blockchains auf Solana [7]. Deshalb nutzt das Projekt Solana und nicht Ethereum.
- **Der Markt ist im Analysezeitraum stark gewachsen.** Das monatliche dezentrale Volumen aller Token in der Übersichtsabfrage stieg von 114 Mio. USD im Juli 2025 auf 2.290 Mio. USD im Juni 2026 und lag im September 2026 bei 2.105 Mio. USD (eigene Dune-Daten).
- **Raydium ist der wichtigste Handelsort, aber nicht für jeden Token gleich stark.** Anteil am dezentralen Volumen von Juli 2025 bis August 2026 (eigene Dune-Daten):

| Handelsort | TSLAx | NVDAx | GOOGLx | AAPLx | AMZNx |
|---|---|---|---|---|---|
| Raydium | 59,3 % | 72,9 % | 41,1 % | 55,6 % | 67,7 % |
| Byreal | 11,1 % | 9,9 % | 30,6 % | 20,5 % | 15,8 % |
| JupiterZ | 6,2 % | 6,1 % | 22,1 % | 14,9 % | 14,8 % |
| Orca (Whirlpool) | 16,3 % | 8,8 % | 3,3 % | 1,7 % | 0,6 % |
| Andere | 7,1 % | 2,3 % | 2,9 % | 7,3 % | 1,1 % |

- **Im September 2026 änderte sich das Handelsmuster.** Ein neuer Handelsort, Raydium LaunchLab, kam auf 12 % bis 19 % des Volumens der fünf Token, und der Anteil der Trades gegen andere Token als Stablecoins oder SOL stieg von 4,9 % des Volumens im August auf 38,5 % im September. Die hier verwendeten Stablecoin-Preise waren davon nicht sichtbar betroffen: Die Preise aus den übrigen Trades weichen im Median um 0,1 % bis 0,2 % davon ab.

## Daten

### Quellen der Daten

| Daten | Quelle | Detail |
|---|---|---|
| Token-Trades | Dune, Tabelle `dex_solana.trades` [8] | Zwei SQL-Abfragen, jede einmal als CSV exportiert |
| Aktienkurse | Yahoo Finance über `yfinance` [9] | Stundenkerzen mit Vor- und Nachbörse, nicht um Dividenden bereinigt, heruntergeladen am 2. Oktober 2026 |
| Börsenkalender | Aus den Aktiendaten abgeleitet | Die acht Nasdaq-Feiertage 2026 im Zeitraum stimmen mit dem veröffentlichten Kalender der Nasdaq überein [5] |

### Dune-Abfragen

| Abfrage | Dune-Abfrage-ID | Ausgabedatei |
|---|---|---|
| `xstocks_solana_30min_prices_by_quote` | 8887243 | `xstocks_solana_30min_by_quote_2025-06-30_2026-09-30.csv` |
| `xstocks_solana_monthly_overview_fees` | 8887198 | `xstocks_solana_monthly_overview_fees.csv` |

Die SQL-Dateien liegen in `sql/`: `xstocks_solana_30min_prices_by_quote.sql` und `xstocks_solana_monthly_overview_fees.sql`.

### Dateien in `data/raw/`

| Datei | Zeilen | Inhalt |
|---|---|---|
| `xstocks_solana_30min_by_quote_2025-06-30_2026-09-30.csv` | 276.486 | 30-Minuten-Preise und Volumen der fünf Token, getrennt nach Gegenwährung (Stablecoin, SOL, andere) |
| `xstocks_solana_monthly_overview_fees.csv` | 1.829 | Trades und Volumen je Monat und Handelsort für alle Token mit dem Mint-Präfix von xStocks. Grundlage der Token-Auswahl |
| `stocks_1h_prepost_2025-07-01_2026-09-30.csv` | 26.204 | Stundenkerzen der fünf Aktien |

### Dateien in `data/clean/`

| Datei | Zeilen | Inhalt |
|---|---|---|
| `tokens_30min_clean.csv` | 108.000 | Eine Zeile je Token und halbe Stunde, mit Stablecoin-Preis, Ausreißer-Markierung und Etiketten für die Börsenphase |
| `stocks_1h_clean.csv` | 26.204 | Stundenkerzen mit Etikett für die Sitzung und Markierung für Fehlkurse außerhalb der Börsenzeit |
| `stocks_daily_open_close.csv` | 1.575 | Offizielle Eröffnung und offizieller Schluss je Aktie und Handelstag |
| `nights.csv` | 1.550 | Eine Zeile je Aktie und Börsenpause: 310 Pausen mal fünf Aktien |

### Was Dune nicht liefert

Die Pool-Gebühren fehlen. Die Spalte `fee_tier` von `dex_solana.trades` ist nur für 0,3 % des Volumens in der Übersicht gefüllt, für Raydium gar nicht. Die Handelskosten in diesem Projekt sind deshalb Szenarien, keine Messwerte.

## Methode in Kürze

- **Token-Preis:** volumengewichteter 30-Minuten-Durchschnittspreis der Trades gegen USDC oder USDT. Ein Preis, der um mehr als 5 % vom zentrierten gleitenden 24-Stunden-Median abweicht, wird als Ausreißer markiert und nicht verwendet (insgesamt 31 halbe Stunden).
- **Analysezeitraum:** beginnt am 8. Juli 2025. Der Amazon-Token wurde vom 2. bis 7. Juli 2025 zu unbrauchbaren Preisen gehandelt (zwischen rund 180 und 3.300 USD bei wenigen Dollar Volumen, bei einem echten Aktienkurs von rund 225 USD).
- **Aktienkurs:** Die Eröffnung ist der Eröffnungskurs der Kerze um 9:30 Uhr, der Schluss ist der Schlusskurs der letzten regulären Kerze. An den zwei verkürzten Handelstagen im Zeitraum ist der Schluss angenähert.
- **Börsenpause:** die Zeit zwischen einem Schluss und der nächsten Eröffnung. Der Zeitraum enthält 243 normale Nächte, 56 Wochenenden und 11 Pausen mit Feiertag.
- **Zeitzonen:** Alle Zeitstempel sind in UTC gespeichert und werden für den Börsenkalender in New Yorker Zeit umgerechnet. So ist die Umstellung zwischen Sommer- und Winterzeit automatisch berücksichtigt.

## Datenqualität

| Prüfung | Ergebnis |
|---|---|
| Duplikate in Token- und Aktiendaten | 0 |
| Fehlende Werte, Preise von null oder darunter | 0 |
| Handelstage je Aktie im Zeitraum | 311, für alle fünf gleich |
| Tage ohne Eröffnungskerze | 0 |
| Unvollständige reguläre Sitzungen | 2 (verkürzte Handelstage am 28. November und 24. Dezember 2025) |
| Halbe Stunden ohne Stablecoin-Trade | TSLAx 1, NVDAx 7, GOOGLx 615, AAPLx 1.216, AMZNx 2.804 von je 21.600 |
| Markierte Fehlkurse in Nachbörsen-Kerzen | 11 |

Lücken in den Token-Daten sind während der Börsenzeit selten und am Wochenende am häufigsten: Beim Amazon-Token fehlen 3,6 % der halben Stunden während der Sitzung und 19,2 % am Wochenende.

## Grenzen

- **Kurze Historie.** 15 Monate und 310 Börsenpausen je Aktie, davon nur 56 Wochenenden und 11 mit Feiertag.
- **Durchschnittspreise.** Ein 30-Minuten-Durchschnitt ist kein Preis, zu dem ein Trade hätte ausgeführt werden können. Der Handelstest ist eine Näherung.
- **Kosten sind Szenarien.** Pool-Gebühren liefert Dune nicht, und Slippage in dünnen Pools ist nicht modelliert.
- **Nur dezentrale Trades.** Trades auf zentralen Börsen wie Kraken sind nicht enthalten.
- **Vor- und Nachbörsen-Kurse** von Yahoo Finance enthalten Fehlkurse und fehlende Kerzen. Sie werden nur für Frage 7 verwendet.
- **Dividenden sind nicht bereinigt.** Apple, Alphabet und Nvidia zahlten im Zeitraum je fünf Dividenden, zwischen 0,01 und 0,27 USD je Aktie.
- **Ein Markt in Entwicklung.** Das Volumen ist 2026 stark gewachsen, und das Handelsmuster änderte sich im September 2026. Die Ergebnisse sind Durchschnitte über einen Markt im Wandel.
- **Entscheidungen bei der Auswahl.** Die Schwelle von 5.000 Trades je Monat und der Ausschluss krypto-naher Unternehmen sind Entscheidungen, keine Tatsachen.
- **Keine Anlageberatung.** Dies ist ein Datenanalyse-Projekt.

## Quellen

Abgerufen am 2. und 3. Oktober 2026.

1. Solana Foundation, "xStocks: Tokenizing Equities on Solana" (Fallstudie): Startdatum, Mint-Adressen, Deckung, Token-Standard, Handelsorte. https://solana.com/news/case-study-xstocks
2. Kraken, "xStocks Risk Disclosure": Emittent, Deckung, Rechte der Halter, gesperrte Länder, Risiken. https://www.kraken.com/legal/xstocks
3. Website von xStocks: Emittent und Vertriebsgesellschaften, Sperre für US-Personen. https://xstocks.fi/
4. Kraken Blog, "Kraken to acquire Backed", 2. Dezember 2025. https://blog.kraken.com/news/backed-acquisition
5. Nasdaq, Feiertagskalender und Handelszeiten. https://www.nasdaq.com/market-activity/stock-market-holiday-schedule
6. StockAnalysis, Unternehmensprofile mit Börse, Ticker und ISIN: [TSLA](https://stockanalysis.com/stocks/tsla/company/), [NVDA](https://stockanalysis.com/stocks/nvda/company/), [GOOGL](https://stockanalysis.com/stocks/googl/company/), [AAPL](https://stockanalysis.com/stocks/aapl/company/), [AMZN](https://stockanalysis.com/stocks/amzn/company/)
7. SolanaFloor, "Solana Tokenization Roundup: June 2026": Anteil von Solana am Handelsvolumen tokenisierter Aktien. https://solanafloor.com/news/solana-tokenization-roundup-june-2026
8. Dune Docs, `dex_solana.trades`: Definition der Tabelle und ihrer Spalten. https://docs.dune.com/data-catalog/curated/dex-trades/solana/solana-dex-trades
9. Dokumentation von yfinance, `download`: Parameter `prepost` und `auto_adjust`. https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html
10. CoinGecko, "What Are Tokenized Stocks and Top Platforms to Get Started": andere Emittenten. https://www.coingecko.com/learn/what-are-tokenized-stocks

Alle Zahlen mit dem Hinweis "eigene Dune-Daten" sind aus den Dateien in `data/raw/` berechnet. Die Token-Auswahl, die Prüfungen der Datenqualität und die Ergebnisse der sieben Fragen sind im Notebook Schritt für Schritt nachvollziehbar; die Anteile der Handelsorte und die Aufteilung nach Gegenwährung sind aus denselben Dateien berechnet, stehen aber nicht im Notebook.

## Über dieses Projekt

Code und Texte sind mit KI-Unterstützung entstanden und von mir gegen die Daten geprüft. Wie ich mit KI arbeite, beschreibt mein Repository [local-ai-workflow](https://github.com/Amirhouschang/local-ai-workflow).

Rückmeldungen gern über GitHub-Issues.

## Rechte

© 2026 Amirhoushang Rahmannejad. Alle Rechte vorbehalten. Ansehen und Prüfen ist ausdrücklich erwünscht. Kopieren, Ändern oder Weiterverbreiten nur mit meiner schriftlichen Erlaubnis.
