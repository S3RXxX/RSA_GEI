# generar cadena de bloques
from BlockChain import rsa_key , rsa_public_key, transaction, block, block_chain
import sympy as sp
import random
import json

if __name__ == "__main__":
    fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_1.block"
    n = 2048
    rsa = rsa_key(bits_modulo=n)
    message = random.randint(2**(n-1), 2**n - 1)
    cadena_de_bloques = block_chain(transaction(message, rsa))
    for i in range(3):
        print(i)
        cadena_de_bloques.add_block(transaction(message, rsa))
    
    with open(fichero_de_salida, 'w') as f:
        f.write(json.dumps(repr(cadena_de_bloques)))
