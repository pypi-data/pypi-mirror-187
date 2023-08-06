from typing import List
from cpanlp.account.assets.asset import *
from cpanlp.person.person import *
from cpanlp.market.market import *
class Department:
    def __init__(self, name, goals, incentives):
        self.name = name
        self.goals = goals
        self.incentives = incentives
        self.legal_status = "Registered"
class BoardOfDirectors:
    def __init__(self):
        self.responsibility = []
        self.powers =  []
    def call_shareholders_meeting(self):
        pass
    def report_to_shareholders(self):
        """Report on the work of the board to shareholders"""
        pass
    def execute_shareholders_resolutions(self):
        """Execute resolutions passed by shareholders"""
        pass
    def decide_on_business_plan(self):
        """Decide on the company's business plan and investment strategy"""
        pass
    def formulate_annual_budget(self):
        """Formulate the company's annual financial budget"""
        pass
    def formulate_profit_distribution(self):
        """Formulate the company's profit distribution plan and plan to make up for losses"""
        pass
    def formulate_capital_increase_or_decrease(self):
        """Formulate the company's plan for increasing or decreasing registered capital and issuing bonds"""
        pass
    def formulate_merger_plan(self):
        """Formulate the company's plan for merger, separation, dissolution or change of corporate form"""
        pass
    def decide_on_internal_management(self):
        """Decide on the setting of the company's internal management structure"""
        pass
    def hire_or_dismiss_manager(self):
        """Decide on the hiring or dismissal of the company manager and their compensation, and based on the manager's nomination, decide on the hiring or dismissal of the company's vice manager, financial officer and their compensation"""
        pass
    
    def formulate_basic_management_system(self):
        """Formulate the company's basic management system"""
        pass
    def other_responsibilities(self):
        """Other responsibilities as specified in the company's bylaws"""
        pass
class LegalEntity:
    def __init__(self, name, type,capital):
        self.name = name
        self.type = type
        self.name = name
        self.registration_number=""
        self.address=""
        self.capital=capital
        self.employees =[]
        self.assets=[]
        self.partners = []
        self.departments = []
        self.agency_cost = 0.0
        self.market_leader = False
        self.market_share = 0.0
        self.sales = 0.0
        self.liability = None     
        self.business_scope = None
        self.registered_capital = None
        self.shareholders = None
        self.legal_representative = None
    def add_department(self, department):
        self.departments.append(department)
    def add_partner(self, partner):
        self.partners.append(partner)
    def fire_employee(self, employee):
        self.employees.remove(employee)
    def hire_employee(self, employee):
        self.employees.append(employee)
    def totalsalary(self):
        return 0.0 if self.employees is None else sum([member.salary for member in self.employees])
    def merge(self, other_entity):
        """
        Merges the current LLC with another LLC
        """
        # Logic to merge the two LLCs
        self.employees.extend(other_entity.employees)
        self.capital += other_entity.capital
        self.name = f"{self.name}-{other_entity.name}"
    def spin_off(self, spin_off_name:str,spin_off_type:str,spin_off_capital:float):
        """
        Creates a new LLC as a spin-off of the current LLC
        """
        return LegalEntity(spin_off_name,spin_off_type,spin_off_capital)
    def increase_capital(self, amount):
        """
        Increases the capital of the LLC
        """
        self.capital += amount
    def decrease_capital(self, amount):
        """
        Decreases the capital of the LLC
        """
        if self.capital - amount < 0:
            raise ValueError("Capital can not be negative")
        self.capital -= amount
    def enter_market(self, market:Market):
        return market
class LLC(LegalEntity):
    def __init__(self, name,type,capital):
        super().__init__(name,type,capital)
        self.subsidiaries = []
        self.ownership = 0.6
        self.control = 0.1
        self.shareholders = []
        self.board_members = []
        self.board_of_supervisors = []
        self.independent_financial_advisor = None
        self.chairman = None
    def establish_subsidiary(self, subsidiary_name, subsidiary_type, subsidiary_capital):
        """
        Create a new subsidiary LLC 
        """
        subsidiary = LLC(subsidiary_name, subsidiary_type,subsidiary_capital)
        self.subsidiaries.append(subsidiary)
        return subsidiary
    def transfer_assets(self, subsidiary, assets):
        """
        Transfer assets to subsidiary
        """
        if subsidiary not in self.subsidiaries:
            raise ValueError(f"{subsidiary.name} is not a subsidiary of {self.name}")
        for asset in assets:
            if asset not in self.assets:
                raise ValueError(f"{asset} is not an asset of {self.name}")
            self.assets.remove(asset)
            subsidiary.assets.append(asset)
        return f"Assets {assets} are transferred to {subsidiary.name} successfully"
class PublicCompany(LLC):
    def __init__(self,name,type,capital):
        super().__init__(name,type,capital)
        self.shareholders=[]
        self.stock_price = 0.0
class Partnership(LegalEntity):
    def __init__(self, name,type,capital):
        super().__init__(name,type,capital)
        self.partners = []
    def add_partner(self, partner):
        self.partners.append(partner)
    def remove_partner(self, partner):
        self.partners.remove(partner)
    def distribute_profit(self, profit):
        """Distribute the profit among partners in a pre-agreed ratio."""
        pass
    def voting_procedure(self,proposal):
        """Conduct voting procedure for major decisions on a given proposal"""
        print(f"Proposal: {proposal}")
        for partner in self.partners:
            vote = input(f"{partner}, do you approve this proposal (yes/no)")
            if vote.lower() not in ["yes","no"]:
                print("Invalid input")
            else:
                pass
    def list_partners(self):
        """List all the partners of the partnership"""
        print(self.partners)
def main():
    partner1 = LegalEntity("Partner Inc","partner",10)
    partner2 = LegalEntity("Partner Co","partner",100)
    partner3 = LegalEntity("Partner LLC","partner",1000)
    partner1.add_partner(partner2)
    partner1.add_partner(partner3)
    print(len(partner1.partners))  # Output: [partner2, partner3]
    a=LegalEntity("A","LLC",1000)
    a.employees=[Employee("a",25,"22",1000,"dd"),Employee("a",25,"22",1000,"dd")]
    a.hire_employee(Employee("x",25,"11",111,"ss"))
    b=LLC("Partner Inc","partner",10)
    print(b.subsidiaries)
    print(a.totalsalary())
    a=PublicCompany("华为","niu",1000)
if __name__ == '__main__':
    main()