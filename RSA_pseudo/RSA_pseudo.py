import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from sympy import mod_inverse, Integer, sqrt

# RSA_pseudo
# Fer operacions matemàtiques amb n per treure p i q
# sabent que p = rs i q = sr,
# on s i r són bits

def read_pubkey(filename):
    # Leer la clave pública desde el archivo
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    return public_key.public_numbers().n, public_key.public_numbers().e

def export_privkey(p, q, n, e, private_key_file='private_key.pem'):
    
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

def recover_factors(N):
    
    # Convertir n a bin
    N_bin = bin(N)[2:]
    
    N_len = len(N_bin)
    if N_len != 2048:
        raise ValueError("N no es un número de 2048b bits")

    mid = N_len // 2
    m1 = int(N_bin[:mid], 2)  # Primera mitad (2rs)
    m2 = int(N_bin[mid:], 2)  # Segunda mitad (r^2 + s^2)
    
    print(sqrt(m2**2-m1))
    r = sqrt(m2 + sqrt(m2**2-m1)//2)
    s = m1//2*r
    
    print(r)
    print()
    print(s)
    print()

    # reconstruir p i q
    p = r + s
    q = s + r
    
    # comprovar que p i qu son correctos 
    if p * q == N:
        return p, q
    else:
        print("p i q incorrectos")
        return None, None

if __name__=="__main__":
    
    sg_file = 'sergi.guimera_pubkeyRSA_pseudo.pem'
    n, e = read_pubkey(sg_file)
    # print(n)

    p, q = recover_factors(N=n)

    # export_privkey(p, q, n, e)

    # Para descifrad:
    # 1. openssl pkeyutl -decrypt -inkey private_key.pem -in sergi.guimera_RSA_pseudo.enc -out AES_key.txt
    # 2. openssl enc -d -aes-128-cbc -pbkdf2 -kfile AES_key.txt -in sergi.guimera_AES_pseudo.enc -out decrypted_file.txt
