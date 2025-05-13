import hashlib
import json
import tkinter as tk
import tkinter as ttk

# Simula una transacción válida con firma simple (solo como texto)
class Transaction:
    def __init__(self, sender, recipient, amount, signature="valid"):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature  # en la vida real, sería criptográfica

    def is_valid(self):
        if self.amount <= 0:
            return False
        if self.signature != "valid":
            return False
        return True

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature
        }

# Bloque con estructura básica
class Block:
    def __init__(self, index, prev_hash, transactions, nonce=0):
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = transactions  # lista de transacciones (primera debe ser coinbase)
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        first_hash = hashlib.sha256(block_string.encode()).digest()  # bytes
        return hashlib.sha256(first_hash).hexdigest()

    def is_valid(self, expected_prev_hash, reward_limit=10):
        # 1. Verificar conexión
        if self.prev_hash != expected_prev_hash:
            print("❌ Hash anterior incorrecto")
            return False

        # 2. Verificar coinbase
        coinbase = self.transactions[0]
        if coinbase.sender != "network":
            print("❌ Coinbase debe venir del 'network'")
            return False
        if coinbase.amount > reward_limit:
            print("❌ Recompensa de coinbase excede el límite")
            return False

        # 3. Verificar todas las transacciones
        for i, tx in enumerate(self.transactions[1:], start=1):
            if not tx.is_valid():
                print(f"❌ Transacción inválida en posición {i}")
                return False

        # 4. Verificar hash
        if not self.hash.startswith("0000"):
            print("❌ Hash del bloque no cumple dificultad")
            return False

        print("✅ Bloque válido")
        return True
        
    def mine_block(block):
        while not block.hash.startswith("0000"):
            block.nonce += 1
            block.hash = block.compute_hash()

# Ejemplo de uso
if __name__ == "__main__":
    # Creamos transacciones (la primera es coinbase)
    tx0 = Transaction("network", "miner1", 10)  # coinbase
    tx1 = Transaction("Alice", "Bob", 5)
    tx2 = Transaction("Charlie", "Dave", 3)
    block1 = Block(index=1, prev_hash="-", transactions=[tx0, tx1, tx2], nonce=0)
    Block.mine_block(block1)
    print("Hash del bloque minado:", block1.hash)
    block1.is_valid(expected_prev_hash="-")

    tx3 = Transaction("network", "miner2", 10)  
    tx4 = Transaction("Claudia", "Bett", 4)
    tx5 = Transaction("Fabian", "Mafe", 4)
    block2 = Block(index=2, prev_hash=block1.hash, transactions=[tx3, tx4, tx5], nonce=0)
    Block.mine_block(block2)
    print("Hash del bloque minado:", block2.hash)
    block2.is_valid(expected_prev_hash=str(block1.hash))

    tx6 = Transaction("network", "miner3", 10)  
    tx7 = Transaction("Ernest", "Sam", 7)
    tx8 = Transaction("Carlos", "Tina", 1)
    block3 = Block(index=3, prev_hash=block2.hash, transactions=[tx6, tx7, tx8], nonce=0)
    Block.mine_block(block3)
    print("Hash del bloque minado:", block3.hash)
    block3.is_valid(expected_prev_hash=str(block2.hash))


blockchain = [block1, block2, block3]

# INTERFAZ GRÁFICA
def show_blocks_gui(blocks):
    root = tk.Tk()
    root.title("Visualizador de Blockchain")
    root.geometry("700x200")
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    for i, block in enumerate(blocks):
        # Crear el marco para el bloque
        frame = ttk.LabelFrame(scrollable_frame, text=f"🧱 Bloque {block.index}")
        frame.grid(row=0, column=i*2, padx=10, pady=10, sticky="n")

        # Agregar detalles del bloque
        ttk.Label(frame, text=f"Hash: {block.hash[:12]}...").pack(anchor="w", padx=5)
        ttk.Label(frame, text=f"Prev: {block.prev_hash[:12]}...").pack(anchor="w", padx=5)
        ttk.Label(frame, text=f"Nonce: {block.nonce}").pack(anchor="w", padx=5)
        ttk.Label(frame, text="Tx:").pack(anchor="w", padx=5)

        for tx in block.transactions:
            tx_str = f"• {tx.sender} → {tx.recipient}: {tx.amount}"
            ttk.Label(frame, text=tx_str).pack(anchor="w", padx=15)

        # Flecha hacia el bloque anterior (izquierda)
        if i > 0:
            arrow = ttk.Label(scrollable_frame, text="⬅️", font=("Arial", 20))
            arrow.grid(row=0, column=i*2 - 1, padx=5)

    root.mainloop()

# Ejecutar interfaz
if __name__ == "__main__":
    show_blocks_gui(blockchain)