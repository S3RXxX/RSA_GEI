import os
from math import gcd
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from sympy import mod_inverse

# RSA_RW
# Buscar les claus públiques que el MCD amb la meva sigui diferent de 0

def find_prime(file, path, criteria):
    n1, _ = read_pubkey(file)
    names = []
    primes = []
    for f in os.listdir(path):
        if f[-len(criteria):] == criteria:
            n2, _ = read_pubkey(os.path.join(path, f))
            mcd = gcd(n1, n2)
            if mcd != 1:
                # print(mcd)
                names.append(f)
                primes.append(mcd)
    return names, primes

def read_pubkey(filename):
    # Leer la clave pública desde el archivo
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    return public_key.public_numbers().n, public_key.public_numbers().e

def export_privkey(p, q, n, e, private_key_file='sergi.guimera_privkeyRSA_RW.pem'):
    
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)

    private_numbers = rsa.RSAPrivateNumbers(
    p=p,
    q=q,
    d=d,
    dmp1=d % (p - 1),  # d mod (p-1)
    dmq1=d % (q - 1),  # d mod (q-1)
    iqmp=mod_inverse(q, p),  # q^(-1) mod p
    public_numbers=rsa.RSAPublicNumbers(e=e, n=n)
    )
    
    private_key = private_numbers.private_key(backend=default_backend())

    # Exportar la clave privada a un archivo en formato PEM
    with open(private_key_file, "wb") as pem_out:
        pem_out.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()  # Sin contraseña
            )
        )

    print(f"Clave privada exportada exitosamente a {private_key_file}")

if __name__=="__main__":
    file = "sergi.guimera_pubkeyRSA_RW.pem"
    path = "RSA_RW"
    criteria = ".pem"
    names, primes = find_prime(file, path, criteria)
    
    p = primes[0]
    q = primes[1]

    n, e = read_pubkey(file)

    export_privkey(p, q, n, e)

    # Se cifró usando:
    # 1. openssl enc -e -aes-128-cbc -pbkdf2 -kfile fichero.key -in fichero.txt -out fichero.enc
    # 2. openssl pkeyutl -encrypt -inkey pubkeyRSA.pem -pubin -in fichero.txt -out fichero.enc
    
    # Para descifrad:
    # 1. openssl pkeyutl -decrypt -inkey sergi.guimera_privkeyRSA_RW.pem -in sergi.guimera_RSA_RW.enc -out sergi.guimera_AES_key.txt
    # 2. openssl enc -d -aes-128-cbc -pbkdf2 -kfile sergi.guimera_AES_key.txt -in sergi.guimera_AES_RW.enc -out sergi.guimera_decrypted_file.png
