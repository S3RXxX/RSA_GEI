import os
from math import gcd
from cryptography.hazmat.primitives import serialization

# RSA_RW
# Buscar les claus públiques que el MCD amb la meva sigui diferent de 0

def find_prime(file, path, criteria):
    n1 = read_pubkey(file)
    names = []
    primes = []
    for f in os.listdir(path):
        if f[-4:] == criteria:
            n2 = read_pubkey(os.path.join(path, f))
            mcd = gcd(n1, n2)
            if mcd != 1:
                print(mcd)
                names.append(f)
                primes.append(mcd)
    return names, primes

def read_pubkey(filename):
    # Leer la clave pública desde el archivo
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    return public_key.public_numbers().n

if __name__=="__main__":
    file = "sergi.guimera_pubkeyRSA_RW.pem"
    path = "RSA_RW"
    criteria = ".pem"
    names, primes = find_prime(file, path, criteria)
    
    p = primes[0]
    q = primes[1]
    n = read_pubkey(file)
    
    # print(n == p*q)
    # print(p)
    # print(q)

    

