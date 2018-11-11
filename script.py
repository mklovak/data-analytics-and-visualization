'''

- to run this script you need to have pandas and json library installed on your system
- if you want to see plotted data even before sending it to client-side, install matplotlib.pyplot and uncomment related strings (see below)

'''

import pandas as pd
import ast
import json
import matplotlib.pyplot as plt


# put here your own path to QUOTES.csv files
csv_one = 'data/FVQUOTES.csv'
csv_two = 'data/TYQUOTES.csv'
inst_quotes_one = pd.read_csv(csv_one)
inst_quotes_two = pd.read_csv(csv_two)

# Calculate a VwMpt at each timestamp t for each instrument's QUOTES series
inst_quotes_one['vwmpt_fv'] = (inst_quotes_one['bestBidPrice'] + (inst_quotes_one['bestOfferPrice']-inst_quotes_one['bestBidPrice']))*(inst_quotes_one['bestBidQty'] / (inst_quotes_one['bestBidQty'] + inst_quotes_one['bestOfferQty']))
inst_quotes_two['vwmpt_ty'] = (inst_quotes_two['bestBidPrice'] + (inst_quotes_two['bestOfferPrice']-inst_quotes_two['bestBidPrice']))*(inst_quotes_two['bestBidQty'] / (inst_quotes_two['bestBidQty'] + inst_quotes_two['bestOfferQty']))

# round calculated vwmpt id you need that
# inst_quotes_one.vwmpt_fv = inst_quotes_one.vwmpt_fv.round(2)
# inst_quotes_two.vwmpt_ty = inst_quotes_two.vwmpt_ty.round(2)

# to prepare data for later plotting we need to merge dataframes and use "nanosec" as common index.
merged = pd.merge(inst_quotes_one, inst_quotes_two, on = "nanosec", how = 'outer', suffixes=('_fv', '_ty'))

# delete columns that we dont need anymore
merged = merged.drop(['bestBidPrice_fv', 'bestBidQty_fv', 'bestOfferPrice_fv', 'bestOfferQty_fv','bestBidPrice_ty','bestBidQty_ty', 'bestOfferPrice_ty', 'bestOfferQty_ty' ], axis=1)

# calculate rolling correlation with lookback of 100 samples
merged['rho'] = merged['vwmpt_fv'].rolling(window=100).corr(other=merged['vwmpt_ty'])

# convert unix epoch timestmaps in nanoseconds to human-readable form (used for debugging. uncomment, if you will need that):
# merged['time'] =  pd.to_datetime(merged['nanosec'], unit='ns')
# merged.set_index("time", inplace=True)

# convert unix epoch timestmaps in nanoseconds to nix epoch timestmaps in milliseconds.
# we will need them in milliseconds because it's JSON format expected by Flot jQuery library
merged['millisec'] = merged['nanosec'].floordiv(1000000)

# Used for debugging (uncomment, if you will need that):
# merged['time_millisec'] =  pd.to_datetime(merged['millisec'], unit='ms')
# merged.head()

# delete rows with NaN cells
merged = merged.dropna()
merged = merged.reset_index(drop=True)

# Plot the data (uncomment if you need to look now at the visualised data):
# merged.plot(y=['vwmpt_fv', 'vwmpt_ty'])
# merged.plot(y=['rho'])
# plt.show()

# generate JSON data in an expected by client form (Flot jQuery library). for example:
''' 
{ "label": "Europe (EU27)",
"data": [[1999, 3.0], [2000, 3.9], [2001, 2.0], [2002, 1.2], [2003, 1.3], [2004, 2.5], [2005, 2.0], [2006, 3.1], [2007, 2.9], [2008, 0.9]]
}
'''
subset_vwmpt_fv = merged[['millisec', 'vwmpt_fv']]
vwmpt_fv_out_data = {
    "label": "vwmpt_fv",
    # https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary
    "data": ast.literal_eval(subset_vwmpt_fv.to_json(date_unit = 'ms', orient='values', date_format = 'epoch'))
}
with open('data/vwmpt_fv_out_data.json', 'w') as outfile:
    json.dump(vwmpt_fv_out_data, outfile)


subset_vwmpt_ty = merged[['millisec', 'vwmpt_ty']]
vwmpt_ty_out_data = {
    "label": "vwmpt_ty",
    "data": ast.literal_eval(subset_vwmpt_ty.to_json(date_unit = 'ms', orient='values', date_format = 'epoch'))
}
with open('data/vwmpt_ty_out_data.json', 'w') as outfile:
    json.dump(vwmpt_ty_out_data, outfile)


subset_rho = merged[['millisec', 'rho']]
rho_out_data = {
    "label": "rho",
    "data": ast.literal_eval(subset_rho.to_json(date_unit = 'ms', orient='values', date_format = 'epoch'))
}
with open('data/rho_out_data.json', 'w') as outfile:
    json.dump(rho_out_data, outfile)

# Used for debugging (uncomment, if you will need that):
# print(subset_rho.head())
# subset_rho['time_millisec'] =  pd.to_datetime(subset_rho['millisec'], unit='ms')
# print(subset_rho.head())
