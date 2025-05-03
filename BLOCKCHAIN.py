import hashlib

class NeuralCoinBlock:
    def __init__(self,previous_block_hash, transaction_list):
        self.previous_block_hash=previous_block_hash
        self.transaction_list=transaction_list
        
        self.block_data = "-".join(transaction_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

t1 = "Paola envia 2 NC a Hernand"
t2 = "Paola envia 1.1 NC a Alfredo"
t3 = "Mike envia 5.2 NC a Isabel"
t4 = "Isabel envia 0.7 NC a Hernand"
t5 = "Isabel envia 2.9 NC a Paola"
t6 = "Jesus envia 7.9 NC a Mike"

initial_block = NeuralCoinBlock("", [t1,t2])
print("Block 1")
print(initial_block.block_data)
print(initial_block.block_hash)
print("\n")

second_block = NeuralCoinBlock(initial_block.block_hash,[t3,t4])
print("Block 2")
print(second_block.previous_block_hash)
print(second_block.block_data)
print(second_block.block_hash)
print("\n")

third_block = NeuralCoinBlock(second_block.block_hash,[t5,t6])
print("Block 3")
print(third_block.previous_block_hash)
print(third_block.block_data)
print(third_block.block_hash)