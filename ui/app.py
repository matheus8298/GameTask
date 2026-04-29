import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
import json
from core.player import Player
from core.task import Task

player = None
tasks = []

# JSON - SALVAR
# =========================
def salvar_dados():
    if player is None:
        return

    data = {
        "player": {
            "nome": player.nome,
            "xp": player.xp,
            "level": player.level
        },
        "tasks": []
    }

    for task in tasks:
        data["tasks"].append({
            "titulo": task.titulo,
            "xp": task.xp,
            "completed": task.completed
        })

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


# JSON - CARREGAR
# =========================
def carregar_dados():
    global player, tasks

    try:
        with open("data.json", "r") as f:
            data = json.load(f)

        player = Player(data["player"]["nome"])
        player.xp = data["player"]["xp"]
        player.level = data["player"]["level"]

        tasks = []
        for t in data["tasks"]:
            task = Task(t["titulo"], t["xp"])
            task.completed = t["completed"]
            tasks.append(task)

        return True

    except:
        return False


# JSON - EXCLUIR
# =========================
def excluir_dados():
    global player, tasks

    if os.path.exists("data.json"):
        os.remove("data.json")

    player = None
    tasks = []

    tela_login()


# TELA LOGIN
# =========================
def tela_login():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Bem-vindo!", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Digite seu Nick:").pack()
    entry_nome = tk.Entry(root)
    entry_nome.pack(pady=5)

    def criar_player():
        global player
        nome = entry_nome.get()
        if not nome:
            return
        
        player = Player(nome)
        salvar_dados()
        tela_app()

    tk.Button(root, text="Criar Player", command=criar_player).pack(pady=10)


# TELA PRINCIPAL
# =========================
def tela_app():
    for widget in root.winfo_children():
        widget.destroy()

    # Frames principais
    frame_esquerda = tk.Frame(root)
    frame_meio = tk.Frame(root)
    frame_direita = tk.Frame(root)

    frame_esquerda.pack(side="left", padx=10, pady=10, fill="y")
    frame_meio.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    frame_direita.pack(side="right", padx=10, pady=10, fill="y")

    # ESQUERDA - CRIAR TASK
    # =========================
    tk.Label(frame_esquerda, text="Nova Task").pack(anchor="w")

    entry_task = tk.Entry(frame_esquerda)
    entry_task.pack(anchor="w", pady=5)

    entry_xp = tk.Entry(frame_esquerda)
    entry_xp.pack(anchor="w", pady=5)

    def adicionar_task():
        nome = entry_task.get()

        try:
            xp = int(entry_xp.get())
        except:
            return

        task = Task(nome, xp)
        tasks.append(task)

        salvar_dados()
        atualizar_lista()

        entry_task.delete(0, tk.END)
        entry_xp.delete(0, tk.END)

    tk.Button(frame_esquerda, text="Adicionar", command=adicionar_task).pack(anchor="w", pady=5)

    # 🔥 BOTÃO EXCLUIR PLAYER (CANTO INFERIOR ESQUERDO)
    tk.Button(
        frame_esquerda,
        text="Excluir Player",
        fg="red",
        command=excluir_dados
    ).pack(side="bottom", anchor="w", pady=10)

    # MEIO - LISTA COM BORDA
    # =========================
    frame_tasks = tk.LabelFrame(
        frame_meio,
        text="Suas Tasks",
        padx=10,
        pady=10,
        bd=2,
        relief="groove"
    )
    frame_tasks.pack(fill="both", expand=True)

    def atualizar_lista():
        for widget in frame_tasks.winfo_children():
            widget.destroy()

        for task in tasks:
            var = tk.BooleanVar(value=task.completed)

            def concluir(t=task, v=var):
                if v.get():
                    if t.complete():
                        player.gain_xp(t.xp)
                        salvar_dados()
                        atualizar_player()

            cb = tk.Checkbutton(
                frame_tasks,
                text=f"{task}",
                variable=var,
                command=concluir
            )

            if task.completed:
                cb.config(state="disabled")

            cb.pack(anchor="w")

    # DIREITA - PLAYER INFO
    # =========================
    tk.Label(frame_direita, text="Player Info", font=("Arial", 12)).pack(anchor="n")

    label_nome = tk.Label(frame_direita, text=f"Player: {player.nome}")
    label_nome.pack(anchor="n", pady=5)

    label_xp = tk.Label(frame_direita, text=f"XP: {player.xp}")
    label_xp.pack(anchor="n", pady=5)

    label_level = tk.Label(frame_direita, text=f"Level: {player.level}")
    label_level.pack(anchor="n", pady=5)

    def atualizar_player():
        label_xp.config(text=f"XP: {player.xp}")
        label_level.config(text=f"Level: {player.level}")

    atualizar_lista()


# AO FECHAR
# =========================
def ao_fechar():
    salvar_dados()
    root.destroy()


# APP
# =========================
root = tk.Tk()
root.title("GameTask")
root.geometry("650x350")

root.protocol("WM_DELETE_WINDOW", ao_fechar)

# Carregar ou iniciar
if carregar_dados():
    tela_app()
else:
    tela_login()

root.mainloop()