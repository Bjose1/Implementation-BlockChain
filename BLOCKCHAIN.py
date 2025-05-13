import hashlib
import json
import tkinter

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
        return hashlib.sha256(block_string.encode()).hexdigest()

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

# Ejemplo de uso
if __name__ == "__main__":
    # Creamos transacciones (la primera es coinbase)
    tx0 = Transaction("network", "miner1", 10)  # coinbase
    tx1 = Transaction("Alice", "Bob", 5)
    tx2 = Transaction("Charlie", "Dave", 3)

    block1 = Block(index=1, prev_hash="0000abc123", transactions=[tx0, tx1, tx2], nonce=1234)

    tx3 = Transaction("network", "miner2", 15)  
    tx4 = Transaction("Claudia", "Bett", 4)
    tx5 = Transaction("Fabian", "Mafe", 4)
    block2 = Block(index=2, prev_hash=block1.hash, transactions=[tx3, tx4, tx5], nonce=1234)

    tx6 = Transaction("Samuel", "Jose", 10)  
    tx7 = Transaction("Ernest", "Sam", 7)
    tx8 = Transaction("Carlos", "Tina", 1)
    block3 = Block(index=3, prev_hash=block2.hash, transactions=[tx6, tx7, tx8], nonce=1234)

    # Simular un hash que cumpla dificultad (empezar con 0000)
    while not block1.hash.startswith("0000"):
        block1.nonce += 1
        block1.hash = block1.compute_hash()

    print("Hash del bloque minado:", block1.hash)
    block1.is_valid(expected_prev_hash="0000abc123")

    