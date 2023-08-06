class Spirit:
    def __init__(self):
        self.determination = None
        self.passion = None
    def display(self):
        print(f'Determination: {self.determination}')
        print(f'Passion: {self.passion}')
class EntrepreneurialSpirit(Spirit):
    def __init__(self):
        super().__init__()
        self.vision = None
        self.risk_taking = None
        self.innovation = None
        self.perseverance = None
        self.leadership = None
    def display(self):
        super().display()
        print(f'Vision: {self.vision}')
        print(f'Risk Taking: {self.risk_taking}')
        print(f'Innovation: {self.innovation}')
        print(f'Perseverance: {self.perseverance}')
        print(f'Leadership: {self.leadership}')
def main():
    print(11)
if __name__ == '__main__':
    main()