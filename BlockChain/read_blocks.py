import json
from BlockChain import rsa_key , rsa_public_key, transaction, block, block_chain

if __name__ == "__main__":
    # fichero_de_salida = "Blockchain/created_blocks/Cadena_bloques_1.block"
    fichero_de_salida = "Blockchain/demo_blocks/Cadena_bloques_valida.block"

    with open(fichero_de_salida, 'r') as f:
        cadena_de_bloques_diccionario = eval(json.loads(f.read()))
    cadena_de_bloques = block_chain()
    cadena_de_bloques.from_dictionary(cadena_de_bloques_diccionario)

    print(cadena_de_bloques.verify())


