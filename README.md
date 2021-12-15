[![DOI](https://zenodo.org/badge/437560017.svg)](https://zenodo.org/badge/latestdoi/437560017)

# Code and data for *Price Revelation from Insider Trading: Evidence from Hacked Earnings News*
Journal of Financial Economics

Pre-print available at [SocArXiv](https://doi.org/10.31235/osf.io/qe6tu)

[Pat Akey](https://sites.google.com/view/patakey/home/) (University of Toronto), [Vincent Grégoire](http://www.vincentgregoire.com/) (HEC Montréal), and [Charles Martineau](https://www.charlesmartineau.com/) (University of Toronto)

The latest version of this code can be found at [https://github.com/vgreg/hacked_earnings_jfe](https://github.com/vgreg/hacked_earnings_jfe).

*Note*: this document is written in Github Flavored Markdown. It can be read by any text editor, but is best viewed with a GFM viewer.

Contact:
- For questions related to IBES, RavenPack and main analysis please contact [Charles Martineau](mailto:charles.martineau@utoronto.ca).
- For questions related to TAQ and text analysis, please contact [Vincent Grégoire](mailto:vincent.3.gregoire@hec.ca).


## Code

All provided code has been tested with 3.9.7 and the packages listed in `requirements.txt`.

### Main analysis

We provide two Jupyter notebooks:

- `Main Analysis.ipynb`: Contains the code to replicate most figures and tables of the paper.
- `Insider Trading Measures`: Contains the code to replicate Table 6.

### Text analysis

We provide two Python scripts and one Jupyter notebook:
- `clean_pr_text.py`: Prepare the press releases texts for processing with ElasticNet.
- `pr sentiment.py`: ElasticNet estimation.
- `Wordcloud.ipynb`: Contains the code to replicate the word cloud figures.

### IBES and RavenPack

To process earnings information from IBES and Ravenpack, we used the code from [**How is Earnings News Transmitted to Stock Prices?**](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3060094) (forthcoming at the *Journal of Accounting Research*), available on [github.com/vgreg/earnings_news_jar](https://github.com/vgreg/earnings_news_jar).

### TAQ

For TAQ processing, we used the sample SAS code from [Holden, Craig W., and Stacey Jacobsen. "Liquidity measurement problems in fast, competitive markets: Expensive and cheap solutions." *The Journal of Finance* 69, no. 4 (2014): 1747-1785](https://doi.org/10.1111/jofi.12127) available on [Professor Stacey Jacobsen's website](https://www.smu.edu/cox/Our-People-and-Community/Faculty/Stacey-Jacobsen) and on WRDS. The rest of the processing was done using custom Python scripts tailored for processing on [Compute Canada](https://www.computecanada.ca/)'s Advanced Research Computing Platform. Please contact [Vincent Grégoire](mailto:vincent.3.gregoire@hec.ca) for help in reproducing those steps on your own infrastructure.



## Data

This study employs several datasets:
1. CRSP for daily stock observations (e.g., price, volume).
2. I/B/E/S for earnings announcements (e.g., analyst forecasts and announcement dates and times).
3. TAQ for intraday stock observations (e.g., price and volume).
4. Ravenpack for earnings announcement press releases.
5. Markit, Optionmetrics and Thompson Reuters 13-F data for various controls.
6. Nasdaq ITCH for order-level stock observations (e.g., accurately signed order flow, limit orders).
7. CBOE Global Markets for intraday option transaction data.
8. Press releases for earnings announcements from 2010 to 2015 from EDGAR (i.e., the text of firms’ communications about their earnings to financial market participants).


Researchers can easily retrieve datasets 1 to 5 through [WRDS](https://wrds-www.wharton.upenn.edu/) with the requisite subscriptions. 
[Nasdaq ITCH](http://www.nasdaqtrader.com/Trader.aspx?id=itch) is available for free through a non-disclosure agreement. 
Option trading data must be purchased directly from [CBOE Global Markets](https://www.cboe.com/****). 


Dataset 8 is used as an input to construct a measure of “soft” information contained in the press releases using machine learning methods. The press release data are freely available through the SEC.

### Stock sample

The file `SampleFirms` contains the sample of stocks used in this study, with the following columns:
- `PERMNO`: CRSP security identifier.
- `GVKEY`: Compustat identifier.
- `SYMBOL`: TAQ symbol.
- `date`:  earnings date.
- `Hacked`: indicates if the stock was exposed to a hack (`1`) or not (`0`) at that time.
- `Actual`: indicates if that stock earnings was mentioned in the SEC complaint documentation as evidence of actual trading by the hackers (`1`) or not (`0`).
- `Soft`: the soft information scores for 36,750 stocks for which we were able to retrieve the actual earnings press release. The value corresponds to the predicted announcement returns based on the press release content.

The file `TimeOfFirstTrade` contains the time of the first trade by the hackers according to the SEC complaint, with the following columns:
- `PERMNO`: CRSP security identifier.
- `GVKEY`: Compustat identifier.
- `SYMBOL`: TAQ symbol.
- `TimeOfFirstTrade`: the time of the first trade by the hackers according to the SEC complaint documentation (174 obs.)

The data is provided in multiple formats:
- [Apache Parquet](https://parquet.apache.org/): recommended for [Python](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html) and [R](https://arrow.apache.org/docs/r/reference/read_parquet.html)
- Comma-separated values (CSV)
- Microsft Excel
- Stata
