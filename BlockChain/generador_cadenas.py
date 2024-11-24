# generar cadena de bloques
from BlockChain import rsa_key , rsa_public_key, transaction, block, block_chain
import sympy as sp
import random
import json
def modify(bc, i=33):
    bc.list_of_blocks[i].block_hash=2**256

if __name__ == "__main__":
    # BlockChain_nombre1.apellido1.block
    # FalseBlockChain_nombre1.apellido1.block
    fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_2.block"
    n = 2048
    modify_bool = True
    rsa = rsa_key(bits_modulo=n)
    message = random.randint(2**(n-1), 2**n - 1)
    cadena_de_bloques = block_chain()
    for i in range(100):
        print(i)
        cadena_de_bloques.add_block(transaction(message, rsa))

    if modify_bool:
        modify(cadena_de_bloques)
    
    with open(fichero_de_salida, 'w') as f:
        f.write(json.dumps(repr(cadena_de_bloques)))
