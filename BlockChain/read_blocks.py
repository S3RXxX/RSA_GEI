import json
from BlockChain import rsa_key , rsa_public_key, transaction, block, block_chain

if __name__ == "__main__":
    # created blocks
    # fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_1.block"
    # fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_2.block"
    # fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_X_block_hash.block"
    # fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_X_previous_block_hash.block"
    # fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_X_seed.block"
    # fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_X_transaction.block"
    fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_X_.block"

    # demo files
    # fichero_de_salida = "Blockchain/demo_blocks/Cadena_bloques_valida.block"
    # fichero_de_salida = "Blockchain/demo_blocks/Cadena_bloques_bloque_falso.block" # 27?
    # fichero_de_salida = "Blockchain/demo_blocks/Cadena_bloques_seed_falsa.block" # 32?
    # fichero_de_salida = "Blockchain/demo_blocks/Cadena_bloques_transaccion_falsa.block" # 6?

    with open(fichero_de_salida, 'r') as f:
        cadena_de_bloques_diccionario = eval(json.loads(f.read()))
    cadena_de_bloques = block_chain()
    cadena_de_bloques.from_dictionary(cadena_de_bloques_diccionario)

    print(cadena_de_bloques.verify())


