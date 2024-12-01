# generar cadena de bloques
from BlockChain import rsa_key , rsa_public_key, transaction, block, block_chain
import sympy as sp
import random
import json
def modify(bc, i=33, modification="block_hash"):
    if modification == "block_hash":
        bc.list_of_blocks[i].block_hash=2**256
    elif modification == "previous_block_hash":
        bc.list_of_blocks[i].previous_block_hash = 2**256
    elif modification == "seed":
        seed = bc.list_of_blocks[i].seed 
        if seed == 0:
            bc.list_of_blocks[i].seed += 1
        else:
            bc.list_of_blocks[i].seed -= 1
    elif modification == "transaction":
        bc.list_of_blocks[i].transaction = transaction(message=0, RSAkey=rsa_key())
    elif modification == "":
        pass
    else:
        print(f"Modification {modification} not in considered, try: ['block_hash', 'previous_block_hash', ...]")

if __name__ == "__main__":
    # BlockChain_nombre1.apellido1.block
    # FalseBlockChain_nombre1.apellido1.block
    
    n = 2048
    # modifications = ["block_hash", "previous_block_hash", "seed", "transaction", ""]
    modifications = ["block_hash"]
    # modifications = [""]
    for modification in modifications:
        # fichero_de_salida = "Cadena_bloques_X_" + modification + ".block"
        # fichero_de_salida = "BlockChain_sergi.guimera.block"
        fichero_de_salida = "FalseBlockChain_sergi.guimera.block"
        rsa = rsa_key(bits_modulo=n)
        message = random.randint(2**(n-1), 2**n - 1)
        cadena_de_bloques = block_chain()
        for i in range(100):
            print(i)
            # rsa = rsa_key(bits_modulo=n)
            # message = random.randint(2**(n-1), 2**n - 1)
            cadena_de_bloques.add_block(transaction(message, rsa))


        modify(cadena_de_bloques, modification=modification)
        
        with open(fichero_de_salida, 'w') as f:
            f.write(json.dumps(repr(cadena_de_bloques)))
