import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate

HOUR = 3600.0

# Number of people per hour that will create new accounts
people_per_hour = 100.0

# Proportion of people who will return for candy
percent_return = .5

# Interest rate to start before the new interest rate
interest_rate = 1

# Number of pieces of candy given to children to start with
initial_candy = 2.0

# Total candy reserves
max_candy = 1800.0

time_to_cut = 2 * HOUR

# 4 hours of runtime (starting at 6pm, ending at 10pm)
TOTAL_TIME = 4 * HOUR

INCREMENT = HOUR / 2

def run_simulation(people_per_hour, percent_return, interest_rate, new_interest, initial_candy, max_candy, candy_left):
    plot_timescale = np.arange(0, TOTAL_TIME, int(HOUR/people_per_hour/percent_return))

    result = []
    start = 0
    old_balances = 0

    for i in range(plot_timescale.shape[0]):
        # change interest rate
        interest = np.sum(np.floor(initial_candy * np.exp(interest_rate / INCREMENT * (plot_timescale[i] - plot_timescale[start:i]))))
        old_interest = old_balances * np.exp(interest_rate / INCREMENT * (plot_timescale[i] - plot_timescale[start]))
        total_balance = interest + old_interest + initial_candy * (1 - percent_return) * i / percent_return
        if total_balance > max_candy - candy_left and start == 0:
            start = i
            interest_rate = new_interest
            old_balances = interest
        if total_balance > max_candy:
            return (plot_timescale[i]-plot_timescale[start])/60
    
    return TOTAL_TIME/60

def get_interest_rate(candy_left, time_left, people_per_hour, percent_return, interest_rate, initial_candy, max_candy):
    # selects an exact interest rate (to within 1%, in the range 0 to 2048%) for given assumptions
    interest = 10.24
    step = interest / 2
    for i in range(10):
        result = run_simulation(people_per_hour, percent_return, interest_rate, interest, initial_candy, max_candy, candy_left)
        if result > time_left:
            interest += step
        else:
            interest -= step
        step /= 2
    return interest

candy_left = np.arange(100, max_candy, 150)
time_left = np.arange(10, 120, 10)
table = [[""]]
for i in candy_left:
    table[0].append(i)

for i in time_left:
    row = [i]
    for j in candy_left:
        interest = get_interest_rate(j, i, people_per_hour, percent_return, interest_rate, initial_candy, max_candy)
        row.append(f"{interest*100:.0f}%")
    table.append(row)

print(tabulate(table, headers='firstrow', tablefmt='plain'))