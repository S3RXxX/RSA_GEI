import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from sympy import mod_inverse, Integer, sqrt, simplify, sympify
from decimal import Decimal, getcontext

# RSA_pseudo
# Fer operacions matemàtiques amb n per treure p i q
# sabent que p = rs i q = sr,
# on s i r són bits

def read_pubkey(filename):
    # Leer la clave pública desde el archivo
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    return public_key.public_numbers().n, public_key.public_numbers().e

def export_privkey(p, q, n, e, private_key_file='sergi.guimera_privkeyRSA_pseudo.pem'):
    
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
    if N_len > 2048:
        raise ValueError("N no es un número de 2048 bits (tiene más)")
    
    # si tiene menos añadimos padding
    padding = '0'*(2048-N_len)
    N_len = 2048
    
    N_bin = padding + N_bin

    # ahora calculamos por donde son las particiones
    split_14 = N_len // 4
    split_24 = 2*N_len // 4
    split_34 = 3*N_len // 4
    for d in range(3):  # d = 0,1,2

        rs_l = N_bin[:split_14]  # Mitad izquierda de rs
        rs_r = N_bin[split_34:]  # Segunda mitad rs
        
        print(f"Trying d={d}")
        # rs_l = rs_l[:-2] + '01' # quitamos el carry
        rs_l = padding + bin(int(rs_l, 2) - d)[2:]  # como es por la derecha podemos restar directamente
        
        rs = int(rs_l+rs_r, 2) # reconstruimos rs
        
        # ahora que tenemos rs podemos buscar r**2+s**2
        # mid = int("10" + N_bin[split_14:split_34], 2)
        mid = int(bin(d)[2:] + N_bin[split_14:split_34], 2)
        # print(rs_l)
        aux = int(rs_r+rs_l, 2)

        r2_s2 = mid - aux
        
        # ahora que tenemos r*s i r**2+s**2 podemos 
        # resolver el sistema para r i s
        k, m = rs, r2_s2


        try:
            insider = m**2-4*k**2
            inner_sqrt = sqrt(insider)
            # print(inner_sqrt)       
            insider2 = m+inner_sqrt
            r = sqrt(insider2//2)    
            s = rs // r
            print(f"Found solution with d={d}")
            
        except:
            continue
    
        # # reconstruir p i q (concatenar)
        # print(r)
        # print(s)
        r = bin(r)[2:]
        s = bin(s)[2:]
        p = r + s
        q = s + r
        p = int(p, 2)
        q = int(q, 2)
        
        # comprovar que p i q son correctos 
        if p * q == N:
            print("Correct solution for p and q")
            return p, q
        else:
            print("p, q INCORRECTOS!!!")
        return None, None
    return None, None

if __name__=="__main__":
    
    sg_file = 'sergi.guimera_pubkeyRSA_pseudo.pem'
    n, e = read_pubkey(sg_file)
    # print(n)

    p, q = recover_factors(N=n)

    if p:
        export_privkey(p, q, n, e)

    # Para descifrad:
    # 1. openssl pkeyutl -decrypt -inkey sergi.guimera_privkeyRSA_pseudo.pem -in sergi.guimera_RSA_pseudo.enc -out sergi.guimera_RSA_pseudo_AES_key.txt
    # 2. openssl enc -d -aes-128-cbc -pbkdf2 -kfile sergi.guimera_RSA_pseudo_AES_key.txt -in sergi.guimera_AES_pseudo.enc -out sergi.guimera_RSA_pseudo_decrypted_file.tiff
