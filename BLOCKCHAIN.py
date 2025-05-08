import hashlib
import tkinter as tk

# --- Clase del bloque ---
class NeuralCoinBlock:
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        self.block_data = "-".join(transaction_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

# --- Crear bloques ---
t1 = "Paola envia 2 NC a Jose"
t2 = "Paola envia 1.1 NC a Alfredo"
t3 = "Mike envia 5.2 NC a Isabel"
t4 = "Isabel envia 0.7 NC a Hernand"
t5 = "Isabel envia 2.9 NC a Paola"
t6 = "Jesus envia 7.9 NC a Mike"

blockchain = []
b1 = NeuralCoinBlock("", [t1, t2])
blockchain.append(b1)
b2 = NeuralCoinBlock(b1.block_hash, [t3, t4])
blockchain.append(b2)
b3 = NeuralCoinBlock(b2.block_hash, [t5, t6])
blockchain.append(b3)

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("Blockchain Visual")
root.geometry("1400x550")  # Ajusté el tamaño de la ventana
root.configure(bg="white")

canvas = tk.Canvas(root, width=1400, height=550, bg="white", highlightthickness=0)  # Ajusté el tamaño del canvas
canvas.pack()

block_width = 200
block_height = 80
start_x = 100
y_block = 50
spacing = 400  # Aumenté la separación entre bloques

# --- Dibujar bloques e info debajo ---
for i, block in enumerate(blockchain):
    x = start_x + i * spacing

    # Dibujar bloque (rectángulo)
    canvas.create_rectangle(x, y_block, x + block_width, y_block + block_height,
                            fill="#1e90ff", outline="black", width=2)

    # Número del bloque
    canvas.create_text(x + block_width / 2, y_block + block_height / 2,
                       text=f"Bloque #{i + 1}", fill="white", font=("Arial", 12, "bold"))

    # Mostrar info debajo de cada bloque
    info_y_start = y_block + block_height + 10
    canvas.create_text(x + 10, info_y_start,
                       text=f"Prev Hash:", anchor="nw", font=("Arial", 9, "bold"), fill="gray")
    canvas.create_text(x + 10, info_y_start + 15,
                       text=f"{block.previous_block_hash}", anchor="nw", font=("Consolas", 8), fill="gray")

    canvas.create_text(x + 10, info_y_start + 40,
                       text=f"Hash:", anchor="nw", font=("Arial", 9, "bold"), fill="green")
    canvas.create_text(x + 10, info_y_start + 55,
                       text=f"{block.block_hash}", anchor="nw", font=("Consolas", 8), fill="green")

    canvas.create_text(x + 10, info_y_start + 80,
                       text=f"Data:", anchor="nw", font=("Arial", 9, "bold"), fill="black")
    canvas.create_text(x + 10, info_y_start + 95,
                       text=f"{block.block_data}", anchor="nw", font=("Consolas", 8), fill="black", width=block_width - 20)

    # Dibujar flechas entre los bloques en la secuencia correcta: de 3 a 2, de 2 a 1
    if i > 0:
        prev_block_x = start_x + (i - 1) * spacing
        # Flecha de izquierda del bloque actual (x) a la derecha del bloque anterior (prev_block_x + block_width)
        canvas.create_line(x, y_block + block_height / 2,
                           prev_block_x + block_width, y_block + block_height / 2,
                           arrow=tk.LAST, width=2, fill="black")

root.mainloop()