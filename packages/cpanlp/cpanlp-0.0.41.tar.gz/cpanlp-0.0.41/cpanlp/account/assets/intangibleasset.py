from cpanlp.account.assets.asset import *
from sklearn.linear_model import LinearRegression
import random
import matplotlib.pyplot as plt
#The most important attribute of an intangible asset is its ability to generate revenue or create a competitive advantage for the company. Examples of intangible assets include patents, trademarks, copyrights, trade secrets, and brand recognition. Other important attributes include the asset's uniqueness, its ability to be protected legally, and the duration of its useful life. Additionally, the company's ability to effectively utilize the asset to generate revenue or create a competitive advantage is also an important factor to consider when evaluating an intangible asset.
class IntangibleAsset(Asset):
    def __init__(self,account,debit, date,amortization_rate):
        super().__init__(account, debit, date)
        self.amortization_rate = amortization_rate
        self.amortization_history = []
        self.model = LinearRegression()
        self.market_value = None
        self.competitive_advantage=None
    def train(self):
        pass
    def predict(self, num_steps):
        pass
    def amortize(self, period: int):
        self.debit -= self.debit * self.amortization_rate * period
        self.amortization_history.append((period, self.debit))
    def simulate_volatility(self, volatility, num_steps):
        prices = [self.debit]
        for i in range(num_steps):
            prices.append(prices[-1] * (1 + volatility * random.uniform(-1, 1)))
        plt.plot(prices)
        plt.show()
class Goodwill(IntangibleAsset):
    def __init__(self,account,debit, date,amortization_rate):
        super().__init__(account,debit, date,amortization_rate)
class IntellectualProperty(IntangibleAsset):
    def __init__(self, account,debit, date,amortization_rate, owner):
        super().__init__(account,debit, date,amortization_rate)
        self.owner = owner
    def register_with_government(self):
        print(f"{self.owner} is registered with the government.")
class LandUseRight(IntangibleAsset):
    def __init__(self, account,debit, date,amortization_rate, land_location):
        super().__init__(account,debit, date,amortization_rate)
        self.land_location = land_location
        

def main():
    print(11)
    a=IntangibleAsset("a",3000,"2022-01-01",0.3)
    print(a.model)
    c=Goodwill("a",3000,"2022-01-01",0.3)
    print(c.debit)
if __name__ == '__main__':
    main()