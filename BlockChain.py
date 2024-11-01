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
        self.privateExponentModulusPhiP = self.privateExponent % self.primeP-1
        self.privateExponentModulusPhiQ = self.privateExponent % self.primeQ-1
        self.inverseQModulusP = self.primeQ**(-1) % self.primeP

        self.n = self.primeP * self.primeQ

        def __find_primes(self):
            """
            encuentra dos números primeros de longitud self.__modulus_bits/2
            tq ...
            """
            pass

        def __repr__(self):
            return str(self.__dict__)
        def sign(self,message):
            """
            Salida: un entero que es la firma de "message" hecha con la clave RSA usando el TCR
            """
            pass
        def sign_slow(self,message):
            """
            Salida: un entero que es la firma de "message" hecha con la clave RSA sin usar el TCR
            """
            return pow(message, self.privateExponent, self.n)

class rsa_public_key:
    def __init__(self, rsa_key):
        """
        genera la clave pública RSA asociada a la clave RSA "rsa_key"
        """
        self.publicExponent = rsa_key.publicExponent
        self.modulus = rsa_key.modulus
    def __repr__(self):
        return str(self.__dict__)
    def verify(self, message, signature):
        """
        Salida: el booleano True si "signature" se corresponde con la
        firma de "message" hecha con la clave RSA asociada a la clave
        pública RSA;
        el booleano False en cualquier otro caso.
        """
        return signature**self.publicExponent == message % self.modulus
class transaction:
    def __init__(self, message, RSAkey):
        """
        genera una transaccion firmando "message" con la clave "RSAkey"
        """
        self.public_key = rsa_public_key(rsa_key=RSAkey)
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

class block:
    def __init__(self):
        """
        crea un bloque (no necesariamente válido)
        """
        
        self.block_hash = None
        self.previous_block_hash = None
        self.transaction = transaction(message=, RSAkey=)
        self.seed = random.randint(0, 2**256 -1)



    """def __f_hash(self):
        entrada=str(self.previous_block_hash)
        entrada=entrada+str(transaction.public_key.publicExponent)
        entrada=entrada+str(transaction.public_key.modulus)
        entrada=entrada+str(transaction.message)
        entrada=entrada+str(transaction.signature)
        entrada=entrada+str(self.seed)
        self.block_hsh=int(hashlib.sha256(entrada.encode()).hexdigest(),16)"""
        
    def __repr__(self):
        return str(self.__dict__)

    def genesis(self,transaction):
        """
        genera el primer bloque de una cadena con la transacción "transaction"
        que se caracteriza por:
        - previous_block_hash=0
        - ser válido
        """
    def next_block(self, transaction):
        """
        genera un bloque válido seguiente al actual con la transacción "transaction"
        """

    def verify_block(self):
        """
        Verifica si un bloque es válido:
        -Comprueba que el hash del bloque anterior cumple las condiciones exigidas
        -Comprueba que la transacción del bloque es válida
        -Comprueba que el hash del bloque cumple las condiciones exigidas
        Salida: el booleano True si todas las comprobaciones son correctas;
        el booleano False en cualquier otro caso.
        """

class block_chain:
    def __init__(self,transaction):
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
    -Passar expresions (-1, **,...) a versió correcta (pow(), ...)
    -
"""
