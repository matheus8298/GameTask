class Task:
    def __init__(self, titulo, xp):
        self.titulo = titulo
        self.xp = xp
        self.completed = False

    def complete(self):
        if not self.completed:
            self.completed = True
            return True
        return False

    #Fazer o python ler como String
    def __str__(self):
        return f"{self.titulo} ({self.xp} XP)"