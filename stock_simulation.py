#!/usr/bin/env python
from __future__ import division

# List of ways to get historical data for stock prices:
# https://www.quantshare.com/sa-620-10-new-ways-to-download-historical-stock-quotes-for-free

# I went with:
# http://markets.financialcontent.com/stocks/action/gethistoricaldata?Month=12&Symbol=[SYMBOL NAME]&Range=300&Year=2017

file = "past_two_years.csv"
#file = "past_16_years.csv"

class fields:
    SYMBOL = 0
    DATE = 1
    OPEN = 2
    HIGH = 3
    LOW = 4
    CLOSE = 5
    VOLUME = 6
    CHANGE = 7
    PERCENT_CHANGE = 8

    INT_VALUES = [6]
    FLOAT_VALUES = [2, 3, 4, 5, 7, 8]
    
stock_data = []
def build_index():
    with open(file) as f:
        for line in f:
            if 'Symbol' in line:
                continue
            line = line[:-2] # strip percent sign and new-line at end
            line = line.split(',')
            try:
                for i in range(len(line)):
                    if i in fields.INT_VALUES:
                        line[i] = int(line[i])
                    elif i in fields.FLOAT_VALUES:
                        line[i] = float(line[i])
                stock_data.append(line)
            except Exception as error:
                print('Failed to parse line: {}'.format(line))
                print(error)
    stock_data.reverse()

upper_bound_as_percent = 1.1
lower_bound_as_percent = 0.9

gains = 0
losses = 0
days = 0
trials = 0

build_index()
end_simulation = False
for i in range(len(stock_data) - 1):
    if end_simulation:
        raise Exception('simulation should have ended')
    trials += 1
    initial_price = stock_data[i][fields.OPEN]
    for j in range(i + 1, len(stock_data)):
        if stock_data[j][fields.OPEN] > initial_price * upper_bound_as_percent:
            gains += 1
            days += j - i
            print('Gain after {0} days. Percentage gains: {1}'.format(j - i, gains / trials * 100))
            break
        if stock_data[j][fields.OPEN] < initial_price * lower_bound_as_percent:
            losses += 1
            days += j - i
            print('Loss after {0} days. Percentage gains: {1}'.format(j - i, gains / trials * 100))
            break
    else:
        # trial did not finish, cancel simulation
        print('Simulation ran from {0} to {1}'.format(stock_data[0][fields.DATE], stock_data[trials][fields.DATE]))
        end_simulation = True
        break

print('Gains: {}'.format(gains))
print('Losses: {}'.format(losses))
print('Total Simulations: {}'.format(gains + losses))
print('Average time: {}'.format(days / trials))
