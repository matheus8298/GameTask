from core.player import Player
from core.task import Task

# Escolha de Nick
name = input("Escolha seu Nick: ")
player = Player(name)

tasks = []

# =========================
# Criar tarefas
# =========================
while True:
    nome = input("Qual a sua Task?\n")
    
    try:
        xp = int(input("Quanto XP ela vai dar?\n"))
    except ValueError:
        print("Digite apenas números para o XP!")
        continue

    task = Task(nome, xp)
    tasks.append(task)

    opcao = input("Deseja criar mais uma Task? (s/n)\n")

    if opcao.lower() != "s":
        break

# =========================
# Completar tarefas (LOOP)
# =========================
while True:
    print("\nSuas Tasks são:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i} - {task}")

    try:
        escolha = int(input("\nQual tarefa você concluiu? (0 para sair) "))
    except ValueError:
        print("Digite um número válido!")
        continue

    if escolha == 0:
        break

    if escolha < 1 or escolha > len(tasks):
        print("Escolha inválida!")
        continue

    task_escolhida = tasks[escolha - 1]

    if task_escolhida.complete():
        player.gain_xp(task_escolhida.xp)
    else:
        print("Essa tarefa já foi concluída!")

    print(f"XP atual: {player.xp} | Nível: {player.level}")

# =========================
# Resultado final
# =========================
print("\nResumo final:")
print(f"XP: {player.xp}")
print(f"Level: {player.level}")