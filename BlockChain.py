# Sergi GR
import random
from math import gcd
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
        self.primeP, self.primeQ = None, None
        self.privateExponentModulusPhiP = None
        self.privateExponentModulusPhiQ = None
        self.inverseQModulusP = None

        self.primeP, self.primeQ = self.__find_primes() # encontramos primos que cumplan la condición
        self.modulus = self.primeP * self.primeQ # calculamos n
        self.privateExponent = sp.mod_inverse(self.publicExponent, self._phi_n) # calculamos d

        # print((self.publicExponent*self.privateExponent) % self._phi_n == 1)

        self.privateExponentModulusPhiP = self.privateExponent % (self.primeP - 1)
        self.privateExponentModulusPhiQ = self.privateExponent % (self.primeQ - 1)
        self.inverseQModulusP = sp.mod_inverse(self.primeQ, self.primeP)

    def __find_primes(self):
        """
        encuentra dos números primeros de longitud self.__modulus_bits/2
        tq ...
        """
        lim_inf, lim_sup = 2**(self.__modulus_bits//2 - 1), 2**(self.__modulus_bits//2)-1
        
        p = sp.randprime(lim_inf, lim_sup)
        while gcd(p, self.publicExponent)!=1:
            p = sp.randprime(lim_inf, lim_sup)

        q = sp.randprime(lim_inf, lim_sup)
        while gcd(q, self.publicExponent)!=1 or p==q:
            q = sp.randprime(lim_inf, lim_sup)

        self._phi_n = (p-1)*(q-1) # calculamos phi(n)
        
        while sp.gcd(self.publicExponent, self._phi_n) != 1:
            
            # do while para generar primos p tq gcd(p, e) = 1
            p = sp.randprime(lim_inf, lim_sup)
            while gcd(p, self.publicExponent)!=1:
                p = sp.randprime(lim_inf, lim_sup)

            q = sp.randprime(lim_inf, lim_sup)
            while gcd(q, self.publicExponent)!=1 or p==q:
                q = sp.randprime(lim_inf, lim_sup)

            self._phi_n = (p-1)*(q-1) # calculamos phi(n)
            
        
        return p, q
    
    def __repr__(self):
        return str(self.__dict__)

    def sign(self,message):
        """
        Salida: un entero que es la firma de "message" hecha con la clave RSA usando el TCR
        """
        Mp = pow(message, self.privateExponentModulusPhiP, self.primeP)
        Mq = pow(message, self.privateExponentModulusPhiQ, self.primeQ)
        h = (self.inverseQModulusP * (Mp - Mq)) % self.primeP
        m = (Mq + h * self.primeQ) % self.modulus
        return m

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
    def from_dictionary(self, transaccion):
        """
        transaccion = {
        'public_key': {
            'publicExponent': 65537,
            'modulus': 77268792373531530874859775898227231886721361866344308896457165466217957463548},
        'message': 1111111,
        'signature': 4848031355983687005831589412107814535662119655983142282793959266002525538316655}
        """
        self.public_key = rsa_public_key(publicExponent = transaccion['public_key']['publicExponent'],
                                                modulus = transaccion['public_key']['modulus']
                                        )
        self.message = transaccion['message']
        self.signature = transaccion['signature']

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
        self.block_hash=int(hashlib.sha256(entrada.encode()).hexdigest(),16)
        
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
        self.transaction = transaction
        self.block_hash = self.__f_hash()

    def next_block(self, transaction):
        """
        genera un bloque válido seguiente al actual con la transacción "transaction"
        """
        b = block()
        self.transaction = transaction
        return 

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
        return self.transaction.verify()
    
    def __verify_previous_hash(self):
        return False
    
    def from_dictionary(self, bloque):
        """
        bloque = {
        'block_hash': 611227525515763553892040764593246705224095844323849655584941894507859918,
        'previous_block_hash': 860009111636437550099323966792787928396638877763118311905514989098990,
        'transaction': {
            'public_key': {
                'publicExponent': 65537,
                'modulus': 8630046192387106941807604362020441904807683470496793476434516960168353410},
            'message': 1111111111111111111111111111111111111,
            'signature': 356837000610140335661652832488149719307360962608450865619567471410525725851},
        'seed': 15788038037054404536350655987002785795816312452536967153872713568114538152952}
        """
        self.block_hash = bloque['block_hash']
        self.previous_block_hash = bloque['previous_block_hash']
        transaccion_aux = transaction()
        transaccion_aux.from_dictionary(bloque['transaction'])
        self.transaction = transaccion_aux
        self.seed = bloque['seed']


class block_chain:
    def __init__(self, transaction=0):
        """
        genera una cadena de bloques que es una lista de bloques,
        el primer bloque es un bloque "genesis" generado con la transacción "transaction"
        """
        self.list_of_blocks = []
        self.list_of_blocks.append() # primer bloque es genesis

    def __repr__(self):
        return str(self.__dict__)

    def add_block(self, transaction):
        """
        añade a la cadena un nuevo bloque válido generado con la transacción "transaction"
        """
        last_block = self.list_of_blocks[-1]
        new_block = last_block.next_block(transaction)
        self.list_of_blocks.append(new_block)
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
        self.list_of_blocks[0]
        for i in range(1, len(self.list_of_blocks)):
            block_i = self.list_of_blocks[i]
            if not block_i.verify_block():
                return False, i
            if False:  # 
                return False, i
        return True
    
    def from_dictionary(self, lista_de_bloques):
        """
        lista_de_bloques={
            'list_of_blocks':
            [
            {’block_hash’: 438706950606371822348686247462944262134905088999967426,
            'previous_block_hash': 0,
            'transaction': {'public_key': {'publicExponent': 65537,
            'modulus': 3508702911114772477700098583160780159},
            'message': 1111111111111111111111111111111111111,
            'signature': 332227860166626417010520625676972266506588923498746
            },
            'seed': 30375809828338577849000370815876946005956863228327241857747841325460539099376
            },
            {'block_hash': 118937117756121245414585385816047931576536827076435985509379583936567275586,
            {'block_hash': 435041778968092905364474619022589453690222734303800866991470949446770182979,
            {'block_hash': 278792726160560451158678572042505587638954710660454744060308266170299446132,
            {'block_hash': 250872889707793976966219660933458705965282691125212532154197547013416918695,
            ...
            ]
        }
        """
        aux = []
        for i in lista_de_bloques['list_of_blocks']:
            bloque = block()
            bloque.from_dictionary(i)
            aux.append(bloque)
        self.list_of_blocks = aux

"""
TODO:
    -Acabar RSA
    -Debug RSA
    -BlockChain
"""
"""
QUESTIONS:
    - phi(n) ?= (p-1)(q-1)
    - mcm?
    - comprovar?: (e*d) % phi(n) == 1
"""
if __name__=="__main__":
    pass
