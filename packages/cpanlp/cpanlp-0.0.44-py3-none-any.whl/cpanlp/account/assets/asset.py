import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
#The most important attribute of an asset is its ability to generate cash flow or appreciate in value. This allows the asset to provide a return on investment or to be sold at a profit in the future. Additionally, the reliability and predictability of cash flow and appreciation are also important factors to consider when evaluating an asset.
class Asset:
    def __init__(self, account, debit,date):
        self.account = account
        self.debit = debit
        self.date = date
        self.assets=[]
        self.roa = np.random.pareto(1)*self.debit
        self.cashflows=[]
        self.is_measurable = True
        self.likely_economic_benefit = True
        self.potential_use=""
        self.market_value = debit
        self.bubble=self.is_asset_bubble(self.market_value)
        self.target_value = None
        self.uniqueness= None
    def __repr__(self):
        return f"Asset({self.account}, {self.debit}, {self.date})"
    def add_asset(self, account, debit,date):
        self.assets.append(Asset(account, debit,date))
    def straight_line_depreciation(self,salvage_value, life):
        annual_depreciation = (self.debit - salvage_value) / life
        return annual_depreciation
    def get_amortization_schedule(self,salvage_value, life,rate):
        schedule = []
        annual_depreciation = self.straight_line_depreciation(salvage_value, life)
        for year in range(1, life + 1):
            amortization = self.debit * rate
            depreciation = annual_depreciation
            self.debit -= (amortization + depreciation)
            schedule.append((year, amortization, depreciation))
        return schedule
    def is_asset_bubble(self, price) -> bool:
        return price > (3*self.debit)
    def set_target(self, target_value):
        self.target_value = np.array(target_value)
    def check_target(self):
        if self.target_value is not None:
            if np.all(self.debit > self.target_value):
                print(f"{self.account} has exceeded its target value")
            elif np.all(self.debit < self.target_value):
                print(f"{self.account} has not yet reached its target value")
            else:
                print(f"{self.account} has reached its target value")
        else:
            print(f"{self.account} has no target value set")

    def sum(self,assets):
        assets_data = [[asset.account, asset.date, asset.debit] for asset in assets]
        assets_df = pd.DataFrame(assets_data, columns=['账户类别', '日期', '借方金额'])
        return assets_df
class Bankdeposit(Asset):
    def __init__(self, account,debit, date, interest_rate=0.03):
        super().__init__(account, debit, date)
        self.interest_rate = interest_rate

    def get_interest_earned(self, end_date: str) -> float:
        end_date1 = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_date1 = datetime.strptime(self.date, "%Y-%m-%d").date()
        return (end_date1 - start_date1).days * self.interest_rate * self.debit
#金融资产的交易性金融资产是指具有流动性和可转移性的金融资产，如股票、债券、期货和外汇等。

class FinancialAsset(Asset):
     def __init__(self, account, debit,date,market_values):
         super().__init__(account, debit,date)
         self.accumulated_impairment = 0
         self.market_values = np.array(market_values)
         self.investment_return = 0
         self.cash_flow = 0
         self.cash_flows=np.array(0)
     def calculate_impairment(self):
            # 假设减值准备的计算方式为财务资产的净值减去其市场价值
         net_value = self.debit  # 假设财务资产的净值为其当前价值
         impairment = net_value - self.market_value
         if impairment > 0:
             self.accumulated_impairment += impairment
     def __str__(self):
         return f"{self.account}: {self.debit} (Accumulated Impairment: {self.accumulated_impairment})"
     def roi(self):
         return (self.market_values[-1] - self.debit) / self.debit
     def investment_cfar(self):
         cfar = (self.investment_return/self.cash_flow) * np.std(self.cash_flows)
         return cfar
     def plot_market_trend(self):
            plt.plot(self.market_values)
            plt.xlabel('time')
            plt.ylabel('price')
            plt.title(f'{self.account} market trend')
            plt.show()
#计提减值准备是指企业在报告期内根据财务报表计算，为了体现财务资产减值而发生的费用。减值准备通常是在财务资产出现损失时进行计提。
class Stock(FinancialAsset):
    def __init__(self, account, debit, date,market_values,symbol):
        super().__init__(account, debit,date,market_values)
        self.symbol = symbol
    def sell(self, amount):
        if amount > self.debit:
            raise ValueError("Cannot sell more than the current value of the asset.")
        self.debit -= amount
    def buy(self, amount):
        self.debit += amount
    def __str__(self):
        return f"Stock(account='{self.account}', value={self.debit}, symbol='{self.symbol}', market='{self.market_value}')"
class transaction:
    def __init__(self, item: str, cost: float, quantity: int):
        self.item = item
        self.cost = cost
        self.quantity = quantity
class costaccounting:
    def __init__(self):
        self.transactions = []
    def add_transaction(self, transaction: transaction):
        self.transactions.append(transaction)
    def get_cost(self, item: str) -> float:
        cost = 0
        for transaction in self.transactions:
            if transaction.item == item:
                cost += transaction.cost * transaction.quantity
        return cost
class investment:
    def __init__(self, date: str, value: float):
        self.date = date
        self.value = value

class equityinvestmentaccounting:
    def __init__(self):
        self.investments = []

    def add_investment(self, investment: investment):
        self.investments.append(investment)

    def get_value(self, date) -> float:
        value = 0
        for investment in self.investments:
            if investment.date <= date:
                value += investment.value
        return value
    def get_return(self, start_date, end_date) -> float:
        start_value = self.get_value(start_date)
        end_value = self.get_value(end_date)
        return (end_value - start_value) / start_value
class financialassetaccounting:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset: FinancialAsset):
        self.assets.append(asset)
class fairvaluefinancialasset(FinancialAsset):
    def update_value(self, value):
        self.value = value
class DividendReceivable(FinancialAsset):
    def __init__(self, account,debit, date,market_value,company, amount):
         super().__init__(account, debit,date,market_value)
         self.company = company
         self.amount = amount
#在会计领域，炒作通常指的是刻意提高某一财务指标或会计概念的价值，以达到获利的目的。这种行为通常会对公司的财务信息的真实性造成负面影响，并可能导致公司遭受监管机构的处罚。在Python中，可以通过定义类来模拟会计概念炒作的情况。例如，可以定义一个名为"AccountingConcept"的类，包括一个名为"manipulate"的方法，用于模拟会计概念炒作的行为    """concept: 会计概念value: 提高的价值
class AccountingConcept:
    def manipulate(self, concept, value):
        pass
class MarketValueManipulation:
  def manipulate(self, asset, value):
      pass
class BalancedScorecard:
      def __init__(self, financial, customer, internal, learning):
            self.financial = financial
            self.customer = customer
            self.internal = internal
            self.learning = learning

#在Python中，可以通过定义类来模拟语法学的情况。例如，可以定义一个名为"Grammar"的类，包含一些属性（例如语言名称、语言类型等）和方法（例如语法分析、句法树构建等）。
def total_asset_value(assets):
    """Calculates the total value of a list of assets."""
    total = 0
    for asset in assets:
        total += asset.debit
    return total
def generate__asset_report(assets):
    """Generates a report with information about a list of assets."""
    report = "ASSET REPORT\n"
    for i in assets:
        report += f"{i.account} ({i.debit}): ${i.date}\n"
    report += f"Total value: ${total_asset_value(assets)}"
    return report
def main():
    a=Bankdeposit("cunkuan",32,"2011-12-12",0.2)
    b=a.get_interest_earned(end_date="2025-02-03")
    print(a.roa)
    print(a.bubble)
    d=a.get_amortization_schedule(0.2,6,0.1)
    print(d)
    ww=a.is_asset_bubble(30)
    print(ww)
    a12 = FinancialAsset("shanghai",100,"2022-12-15",
    [20,30])
    a2 = FinancialAsset("shanghai1",200,"2022-12-15",
    [20,30])
    c=a12.roi()
    b=generate__asset_report([Asset("黄金",199,"2022-01-12"),Asset
    ("股票",102,"2022-01-11")])
    print(b)
    a1 = Asset("a1",  100,"2022-01-02")
    a2 = Asset("a2",  200,"2023-01-02")
    a3 = Asset("a3",  300,"2024-01-02")
    assets_list = [a1,a2,a3]
    print(a.sum(assets_list))
    stock = Asset("a1",  300,"2022-01-02")
    stock.set_target([120,210,160])
    stock.check_target()
    print(a12.roi())
    a12.plot_market_trend()
if __name__ == '__main__':
    main()