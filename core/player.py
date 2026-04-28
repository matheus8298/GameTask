class Player:
    def __init__(self, nome):
        self.nome = nome
        self.xp = 0
        self.level = 1

    def gain_xp(self, amount):
        self.xp += amount
        print(self.nome, "Ganhou ",amount, "XP!")
        
        if self.xp >= self.level * 100: #Analisa se o XP acumulado é igual o nível multiplicado por 100
            self.level += 1
            print("LEVEL UP!")