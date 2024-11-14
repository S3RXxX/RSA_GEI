# Sergi GR
import random
from math import pow
import hashlib
import sympy as sp

class rsa_key:
    def __init__(self,bits_modulo=2048,e=2**16+1):
        """
        genera una clave RSA (de 2048 bits y exponente público 2**16+1 por defecto)
        """
        self.__modulus_bits = bits_modulo
        self.publicExponent = e
        self.privateExponent = None
        self.modulus = None
        self.primeP, self.primeQ = self.__find_primes()
        self.privateExponentModulusPhiP = self.privateExponent % (self.primeP - 1)
        self.privateExponentModulusPhiQ = self.privateExponent % (self.primeQ - 1)
        self.inverseQModulusP = self.primeQ**(-1) % self.primeP

        self.modulus = self.primeP * self.primeQ

        def __find_primes(self):
            """
            encuentra dos números primeros de longitud self.__modulus_bits/2
            tq ...
            """
            p, q = 0, 0
            while False:
                p = sp.randprime(2^(self.__modulus_bits//2 - 1), 2^(self.__modulus_bits//2));
                # check p
                q = sp.randprime(2^(self.__modulus_bits//2 - 1), 2^(self.__modulus_bits//2));
                # check q 
            return p, q

        def __repr__(self):
            return str(self.__dict__)

        def sign(self,message):
            """
            Salida: un entero que es la firma de "message" hecha con la clave RSA usando el TCR
            """
            m1 = pow(message, self.privateExponentModulusPhiP, self.primeP)
            m2 = pow(message, self.privateExponentModulusPhiQ, self.primeQ)
            h = (self.inverseQModulusP * (m1 - m2)) % self.primeP
            return m2 + h * self.primeQ

        def sign_slow(self,message):
            """
            Salida: un entero que es la firma de "message" hecha con la clave RSA sin usar el TCR
            """
            return pow(message, self.privateExponent, self.modulus)

class rsa_public_key:
    def __init__(self, publicExponent=1, modulus=1):
        """
        genera la clave pública RSA asociada a la clave RSA "rsa_key"
        """
        self.publicExponent = publicExponent
        self.modulus = modulus

    def __repr__(self):
        return str(self.__dict__)

    def verify(self, message, signature):
        """
        Salida: el booleano True si "signature" se corresponde con la
        firma de "message" hecha con la clave RSA asociada a la clave
        pública RSA;
        el booleano False en cualquier otro caso.
        """
        # return signature**self.publicExponent == message % self.modulus
        return pow(signature, self.publicExponent, self.modulus) == message


class transaction:
    def __init__(self, message=0, RSAkey=0):
        """
        genera una transaccion firmando "message" con la clave "RSAkey"
        """
        self.__RSAkey = RSAkey
        self.public_key = rsa_public_key(publicExponent=RSAkey.publicExponent, modulus=RSAkey.modulus)
        self.message = message
        self.signature = RSAkey.sign(message)

    def __repr__(self):
        return str(self.__dict__)

    def verify(self):
        """
        Salida: el booleano True si "signature" se corresponde con la
        firma de "message" hecha con la clave RSA asociada a la clave
        pública RSA;
        el booleano False en cualquier otro caso.
        """
        return self.public_key.verify(self.message, self.signature)

class block:
    def __init__(self):
        """
        crea un bloque (no necesariamente válido)
        """
        
        self.block_hash = None
        self.previous_block_hash = None
        self.transaction = None # transaction(message=, RSAkey=)
        self.seed = random.randint(0, 2**256 -1)



    def __f_hash(self):
        entrada=str(self.previous_block_hash)
        entrada=entrada+str(transaction.public_key.publicExponent)
        entrada=entrada+str(transaction.public_key.modulus)
        entrada=entrada+str(transaction.message)
        entrada=entrada+str(transaction.signature)
        entrada=entrada+str(self.seed)
        self.block_hsh=int(hashlib.sha256(entrada.encode()).hexdigest(),16)
        
    def __repr__(self):
        return str(self.__dict__)

    def genesis(self,transaction):
        """
        genera el primer bloque de una cadena con la transacción "transaction"
        que se caracteriza por:
        - previous_block_hash=0
        - ser válido
        """
        self.previous_block_hash = 0
        self.block_hash = self.__f_hash()

    def next_block(self, transaction):
        """
        genera un bloque válido seguiente al actual con la transacción "transaction"
        """
        block(transaction, previous_block_hash=self.block_hash)

    def verify_block(self):
        """
        Verifica si un bloque es válido:
        -Comprueba que el hash del bloque anterior cumple las condiciones exigidas
        -Comprueba que la transacción del bloque es válida
        -Comprueba que el hash del bloque cumple las condiciones exigidas
        Salida: el booleano True si todas las comprobaciones son correctas;
        el booleano False en cualquier otro caso.
        """
        return self.__verify_previous_hash() and self.__verify_transaction() and self.__verify_previous_hash()
    

    def __verify_previous_hash(self):
        return False
    
    def __verify_transaction(self):
        return False
    
    def __verify_previous_hash(self):
        return False

class block_chain:
    def __init__(self, transaction=0):
        """
        genera una cadena de bloques que es una lista de bloques,
        el primer bloque es un bloque "genesis" generado amb la transacción "transaction"
        """
        self.list_of_blocks = []

    def __repr__(self):
        return str(self.__dict__)

    def add_block(self, transaction):
        """
        añade a la cadena un nuevo bloque válido generado con la transacción "transaction"
        """
    def verify(self):
        """
        verifica si la cadena de bloques es válida:
        - Comprueba que todos los bloques son válidos
        - Comprueba que el primer bloque es un bloque "genesis"
        - Comprueba que para cada bloque de la cadena el siguiente es correcto
        Salida: el booleano True si todas las comprobaciones son correctas;
        en cualquier otro caso, el booleano False y un entero
        correspondiente al último bloque válido
        """

"""
TODO:
    -Prev: mirar Sagemath Aritmética y primalidad y RSA
    -Passar expresions (-1, **,...) a versió correcta (pow(), ...)
    -Acabar RSA
    -Debug RSA
    -RW
    -Pseudo
"""

"""
Ron was wrong, Whit was right
RESUM:
    -weak keys
    -

"""

"""
Pseudo
RESUM:
    -

"""
