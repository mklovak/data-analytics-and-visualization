'''

## Task
The overall task will involve extracting market data for various trading instruments (represented by unique symbols),
applying some transformations and statistical functions, and displaying the results in a report.

1. Obtain the following *QUOTES* series from csv files: `TYQUOTES.csv`, `FVQUOTES.csv`
  The quotes data is stored as a BBO. BBO stands for best bid/offer, which represents the best bid and ask
  (ask and offer are interchangeable terms) in the market for a given instrument at any given time.
   At each timestamp it contains, in the following order: bid price, bid quantity, ask price, ask quantity

2. Calculate a `VwMpt` at each timestamp *t* for each instrument's QUOTES series
`VwMpt_t = bid_price_t + (ask_price_t-bid_price_t) * (bid_qty_t / (bid_qty_t+ask_qty_t))`

3. Calculate a rolling correlation `rho` of `VwMpt` returns (first difference, i.e. derivative) sampled
at 1 minute intervals with a lookback of 100 samples

4. On a webpage, display a plot of `VwMpt` substracted from the first sample (so the time series starts at `0`)
of both series on the same line chart, and below it plot the `rho` lined up along the same time axis.
You may use a library like [Flot](http://www.flotcharts.org/) or something similar.

'''

import pandas as pd

# put here your own path to QUOTES.csv files
csv_one = 'data/FVQUOTES.csv'
csv_two = 'data/TYQUOTES.csv'
inst_quotes_one = pd.read_csv(csv_one)
inst_quotes_two = pd.read_csv(csv_two)

# Calculate a VwMpt at each timestamp t for each instrument's QUOTES series
inst_quotes_one['vwmpt_fv'] = (inst_quotes_one['bestBidPrice'] + (inst_quotes_one['bestOfferPrice']-inst_quotes_one['bestBidPrice']))*(inst_quotes_one['bestBidQty'] / (inst_quotes_one['bestBidQty'] + inst_quotes_one['bestOfferQty']))
inst_quotes_two['vwmpt_ty'] = (inst_quotes_two['bestBidPrice'] + (inst_quotes_two['bestOfferPrice']-inst_quotes_two['bestBidPrice']))*(inst_quotes_two['bestBidQty'] / (inst_quotes_two['bestBidQty'] + inst_quotes_two['bestOfferQty']))

inst_quotes_one.vwmpt_fv = inst_quotes_one.vwmpt_fv.round(2)
inst_quotes_two.vwmpt_ty = inst_quotes_two.vwmpt_ty.round(2)

# to prepare data for later plotting we need to merge dataframes and use "nanosec" as common index.
merged = pd.merge(inst_quotes_one, inst_quotes_two, on = "nanosec", how = 'outer', suffixes=('_fv', '_ty'))

# calculate rolling correlation with lookback of 100 samples
merged['rho'] = merged['vwmpt_fv'].rolling(window=100).corr(other=merged['vwmpt_ty'])

# delete columns that we dont need anymore
merged = merged.drop(['bestBidPrice_fv', 'bestBidQty_fv', 'bestOfferPrice_fv', 'bestOfferQty_fv','bestBidPrice_ty','bestBidQty_ty', 'bestOfferPrice_ty', 'bestOfferQty_ty' ], axis=1)

# and convert unix epoch timestmaps in nanoseconds to human-readable form (uncomment, if you need that)
# merged['time'] =  pd.to_datetime(merged['nanosec'], unit='ns')
# merged.set_index("time", inplace=True)
merged['millisec'] = merged['nanosec'].floordiv(1000000)

# For debugging:
# merged['time_millisec'] =  pd.to_datetime(merged['millisec'], unit='ms')
# merged.head()

# delete rows with NaN cells
merged = merged.dropna()
merged = merged.reset_index(drop=True)

# Plot the data (uncomment if you need to look at the visualised data):
# merged.plot(y=['vwmpt_fv', 'vwmpt_ty'])
# merged.plot(y=['rho'])
# plt.show()

# generate JSON data in an expected by client form. for example: [ [[0, 0], [1, 1]] ]
subset_rho = merged[['millisec', 'rho']]

# For debugging:
# print(subset_rho.head())
# subset_rho['time_millisec'] =  pd.to_datetime(subset_rho['millisec'], unit='ms')
# print(subset_rho.head())

rho_out_data = subset_rho.to_json(date_unit = 'ms', orient='values', date_format = 'epoch')
with open('data/rho_out_data.json', 'w') as outfile:
    outfile.write(rho_out_data)

subset_vwmpt_fv = merged[['millisec', 'vwmpt_fv']]
vwmpt_fv_out_data = subset_vwmpt_fv.to_json(date_unit = 'ms', orient='values', date_format = 'epoch')
with open('data/vwmpt_fv_out_data.json', 'w') as outfile:
    outfile.write(vwmpt_fv_out_data)

subset_vwmpt_ty = merged[['millisec', 'vwmpt_ty']]

vwmpt_ty1_out_data = subset_vwmpt_ty[:47138].to_json(date_unit = 'ms', orient='values', date_format = 'epoch')
with open('data/vwmpt_ty1_out_data.json', 'w') as outfile:
    outfile.write(vwmpt_ty1_out_data)

vwmpt_ty2_out_data = subset_vwmpt_ty[47138:].to_json(date_unit = 'ms', orient='values', date_format = 'epoch')
with open('data/vwmpt_ty2_out_data.json', 'w') as outfile:
    outfile.write(vwmpt_ty2_out_data)

