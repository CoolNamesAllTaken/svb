import numpy as np
from matplotlib import pyplot as plt

HOUR = 3600.0

# Number of people per hour that will create new accounts
people_per_hour = 100.0

# Proportion of people who will return for candy
percent_return = .7

# Static interest rate, per 30 mins
interest_rate = 1.0

# Number of pieces of candy given to children to start with
initial_candy = 2.0

# Total candy reserves
max_candy = 1800.0

time_to_cut = 2 * HOUR
max_candy = 1800.0

time_to_cut = 2 * HOUR

# 4 hours of runtime (starting at 6pm, ending at 10pm)
TOTAL_TIME = 3 * HOUR
TOTAL_TIME = 3 * HOUR

INCREMENT = HOUR / 2

def run_simulation(people_per_hour, percent_return, interest_rate, new_interest, initial_candy, max_candy, candy_left):
    plot_timescale = np.arange(0, TOTAL_TIME, int(HOUR/people_per_hour/percent_return))

    result = []
    start = 0
    old_balances = 0

    for i in range(plot_timescale.shape[0]):
        all_account_balances = initial_candy * np.exp(interest_rate / INCREMENT * (plot_timescale[i] - plot_timescale[start:i]))
        interest = np.sum(np.floor(all_account_balances))
        old_interest = old_balances * np.exp(interest_rate / INCREMENT * (plot_timescale[i] - plot_timescale[start]))
        previous_balances = interest + old_interest
        total_balance = previous_balances + initial_candy * (1 - percent_return) * i / percent_return
        if total_balance > max_candy - candy_left and start == 0:
            old_balances = np.sum(all_account_balances)
            interest_rate = new_interest
            start = i
        result.append(total_balance)
    
    result = np.array(result)
    result = np.where(result > max_candy, max_candy, result)

    return plot_timescale, result

x, y = run_simulation(people_per_hour, percent_return, interest_rate, .27, initial_candy, max_candy, 1000)
plt.plot(x/HOUR, y, label='100%/2')
plt.legend(title='Interest Rate/Initial Pieces of Candy')
plt.xlabel('Hours since start')
plt.ylabel('Total candy reserves')
plt.grid()
plt.show()