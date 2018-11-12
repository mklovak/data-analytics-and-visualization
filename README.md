

## Task:
The overall task will involve extracting market data for various trading instruments (represented by unique symbols), applying some transformations and statistical functions, and displaying the results in a report.

1.	Obtain the *QUOTES* series from csv files in folder "data" (files in the repository are zipped) : `TYQUOTES.csv`, `FVQUOTES.csv`
	The quotes data is stored as a BBO. BBO stands for best bid/offer, which represents the best bid and ask (ask and offer are interchangeable terms) in the market for a given instrument at any given time (timestamps are unix epoch timestmaps in nanoseconds). At each timestamp it contains, in the following order: bid price, bid quantity, ask price, ask quantity

2.	Calculate a `VwMpt` at each timestamp *t* for each instrument's QUOTES series. `VwMpt`is Volume Weighted Average Price, find some info here- https://www.investopedia.com/terms/v/vwap.asp
	`VwMpt_t = bid_price_t + (ask_price_t-bid_price_t) * (bid_qty_t / (bid_qty_t+ask_qty_t))`

3. Calculate a rolling correlation `rho` of `VwMpt` returns (first difference, i.e. derivative) sampled at 1 minute intervals with a lookback of 100 samples

4. On a webpage, display a plot of `VwMpt` substracted from the first sample (so the time series starts at `0`) of both series on the same line chart, and below it plot the `rho` lined up along the same time axis. You may use a library like [Flot](http://www.flotcharts.org/) or something similar.

## Additional info:
You will need to know some basics of market data and trading concepts. Also, a basic understanding of time series data. These are good starting points:
* [Order Books](http://en.wikipedia.org/wiki/Order_book_%28trading%29)
* [Bid/Ask](https://en.wikipedia.org/wiki/Bid%E2%80%93ask_spread)

## Solution provided:
1. run script.py*
- it takes two unzipped csv files 'data/FVQUOTES.csv' and 'data/TYQUOTES.csv'**
- calculate a VwMpt at each timestamp t for each instrument's QUOTES series
- calculate rolling correlation with lookback of 100 samples
- generate 3 json files: 'data/vwmpt_fv_out_data.json', 'data/vwmpt_ty_out_data.json', 'data/rho_out_data_t.json'
2. open index.html file to view the report in a requested form***




*In order to run script.py you need to have pandas and json libraryes installed on your system.

** Actual input data was deleted from a "data" folder because it may be considered as a confidential data. Contact @mklovak to see how provided solution works.

*** In order to see graph visualisation you need to download, install and link to index.html file jQuery (https://jquery.com/download) and Flot (http://www.flotcharts.org/) libraries.







