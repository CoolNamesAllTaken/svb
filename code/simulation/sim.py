import numpy as np
from matplotlib import pyplot as plt

HOUR = 3600.0

# Number of people per hour that will create new accounts
people_per_hour = 100.0

# Proportion of people who will return for candy
percent_return = .5

# Static interest rate, per 30 mins
interest_rate = .5

# Number of pieces of candy given to children to start with
initial_candy = 2.0

# Total candy reserves
max_candy = 1800.0

time_to_cut = 2 * HOUR

# 4 hours of runtime (starting at 6pm, ending at 10pm)
TOTAL_TIME = 3 * HOUR

INCREMENT = HOUR / 2

def run_simulation(people_per_hour, percent_return, interest_rate, initial_candy, max_candy, time_to_cut):
    plot_timescale = np.arange(0, TOTAL_TIME, int(HOUR/people_per_hour/percent_return))

    result = []

    for i in range(plot_timescale.shape[0]):
        # change interest rate
        interest = np.sum(np.floor(initial_candy * np.exp(interest_rate / INCREMENT * (plot_timescale[i] - plot_timescale[:i]))))
        total_balance = interest + initial_candy * (1 - percent_return) * i / percent_return
        result.append(total_balance)
    
    result = np.array(result)
    result = np.where(result > max_candy, max_candy, result)

    return plot_timescale, result

x, y = run_simulation(people_per_hour, percent_return, 1, 2, max_candy, time_to_cut)
plt.plot(x/HOUR, y, label='100%/2')
x, y = run_simulation(people_per_hour, percent_return, 1, 3, max_candy, time_to_cut)
plt.plot(x/HOUR, y, label='100%/3')
x, y = run_simulation(people_per_hour, percent_return, 1, 4, max_candy, time_to_cut)
plt.plot(x/HOUR, y, label='100%/4')
plt.legend(title='Interest Rate/Initial Pieces of Candy')
plt.xlabel('Hours since start')
plt.ylabel('Total candy reserves')
plt.grid()
plt.show()