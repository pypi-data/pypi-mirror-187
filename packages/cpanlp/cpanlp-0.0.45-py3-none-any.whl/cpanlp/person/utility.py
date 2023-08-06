import math
def log_utility(good_utility, price, consumer_income):
    return math.log(good_utility - price / consumer_income)