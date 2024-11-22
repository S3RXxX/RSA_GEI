from BlockChain import rsa_key #, rsa_public_key, transaction, block, block_chain
import sympy as sp

# testing file for BlockChain.py
def check_primes_length(k=20, bitsN=2048):
    c = 0
    for _ in range(k):
        rsa = rsa_key(bits_modulo=bitsN)
        if len(bin(rsa.primeP)[2:]) != bitsN//2:
            print("INCORRECT length p")
            c+=1

        if len(bin(rsa.primeQ)[2:]) != bitsN//2:
            print("INCORRECT length q")
            c+=1
    return c

def check_gcd_primes(k=20, bitsN=2048):
    c = 0
    for _ in range(k):
        rsa = rsa_key(bits_modulo=bitsN)
        if sp.gcd(rsa.primeP, rsa.publicExponent) != 1:
            print("INCORRECT p (gcd != 1)")
            c+=1

        if sp.gcd(rsa.primeQ, rsa.publicExponent) != 1:
            print("INCORRECT q (gcd != 1)")
            c+=1
    return c

def check_gcd_exp(k=20, bitsN=2048):
    
    c = 0
    for _ in range(k):
        rsa = rsa_key(bits_modulo=bitsN)
        if sp.gcd(rsa.publicExponent, rsa._phi_n) != 1:
            print("INCORRECT phi(n) (gcd != 1)")
            c+=1

    return c

if __name__=="__main__":
    cs = 0
    # cs += check_primes_length()
    # cs += check_gcd_primes()
    # cs += check_gcd_exp()
    # print(f"Total number of ERRORS={cs}!!!")

    