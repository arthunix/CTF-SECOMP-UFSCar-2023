import os
import json

# -------------------------- Esse trecho é o conteúdo do desafio -----------------------------

# 2^128 collision protection!
BLOCK_SIZE = 32


# Nothing up my sleeve numbers (ref: Dual_EC_DRBG P-256 coordinates)
W = [0x6b17d1f2, 0xe12c4247, 0xf8bce6e5, 0x63a440f2, 0x77037d81, 0x2deb33a0, 0xf4a13945, 0xd898c296]
X = [0x4fe342e2, 0xfe1a7f9b, 0x8ee7eb4a, 0x7c0f9e16, 0x2bce3357, 0x6b315ece, 0xcbb64068, 0x37bf51f5]
Y = [0xc97445f4, 0x5cdef9f0, 0xd3e05e1e, 0x585fc297, 0x235b82b5, 0xbe8ff3ef, 0xca67c598, 0x52018192]
Z = [0xb28ef557, 0xba31dfcb, 0xdd21ac46, 0xe2a91e3c, 0x304f44cb, 0x87058ada, 0x2cb81515, 0x1e610046]

# Lets work with bytes instead!
W_bytes = b''.join([x.to_bytes(4,'big') for x in W])
X_bytes = b''.join([x.to_bytes(4,'big') for x in X])
Y_bytes = b''.join([x.to_bytes(4,'big') for x in Y])
Z_bytes = b''.join([x.to_bytes(4,'big') for x in Z])

def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len]*padding_len)

def blocks(data):
    return [data[i:(i+BLOCK_SIZE)] for i in range(0,len(data),BLOCK_SIZE)]

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def rotate_left(data, x):
    x = x % BLOCK_SIZE
    return data[x:] + data[:x]

def rotate_right(data, x):
    x = x % BLOCK_SIZE
    return  data[-x:] + data[:-x]

def scramble_block(block):
    for _ in range(40):
        block = xor(W_bytes, block)
        block = rotate_left(block, 6)
        block = xor(X_bytes, block)
        block = rotate_right(block, 17)
    return block

def cryptohash(msg):
    initial_state = xor(Y_bytes, Z_bytes)
    msg_padded = pad(msg)
    msg_blocks = blocks(msg_padded)

    for i,b in enumerate(msg_blocks):
        mix_in = scramble_block(b)
        for _ in range(i):
            mix_in = rotate_right(mix_in, i+11)
            mix_in = xor(mix_in, X_bytes)
            mix_in = rotate_left(mix_in, i+6)
        initial_state = xor(initial_state,mix_in)
    return initial_state.hex()

# -------------------------- Agora fazemos a solução -----------------------------

SIZE = 32

def unscramble_block(block):
    for _ in range(40):
        block = rotate_left(block,17) # Reverso de block = rotate_right(block, 17)
        block = xor(X_bytes, block) # Reverso de xor(X_bytes, block)
        block = rotate_right(block, 6) # Reverso de rotate_right(block, 6) 
        block = xor(W_bytes, block) # Reverso de xor(W_bytes, block) 
    return block


def explicar_padding():
    
    # A função que adiciona padding é vulnerável porque o total de bytes adicionados para uma mensagem de mesmo tamanho
    # do bloco é 0. Veja:

    #padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE -> Aqui, fica (32 - 32) % 32 = 0
    #return data + bytes([padding_len]*padding_len)
    
    data = os.urandom(SIZE) 
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    devolver = data + bytes([padding_len]*padding_len)

    print("Antes : " + bytes.hex(data))
    print("Depois: " + bytes.hex(devolver) + " com " + str(padding_len) + " bytes adicionados.")
    print("------------------------------------------------------------------------------------------")

def explicar_reverso():

    # O algoritmo de hash se baseia em operações reversíveis sendo realizadas 40 vezes.
    
    # A primeira delas é um XOR com a seed W_bytes. Veja que:
    
    pre = os.urandom(SIZE)
    pre_xor = xor(W_bytes, pre)
    pre_back = xor(W_bytes, pre_xor)

    if pre == pre_back:
        print("A operação XOR é reversível!")

    # A segunda é um Rotate Left com 6 posições. Veja que:
        
    pre = os.urandom(SIZE)
    pre_rotate_left = rotate_left(pre, 6)
    pre_back = rotate_right(pre_rotate_left, 6)

    if pre == pre_back:
        print("A operação Rotate Left é reversível!")

    # Analogamente, a operaçãço Rotate Right com 17 posições também é reversível. Veja que:

    pre = os.urandom(SIZE)
    pre_rotate_right = rotate_right(pre, 17)
    pre_back = rotate_left(pre_rotate_right, 17)

    if pre == pre_back:
        print("A operação Rotate Right é reversível!")     

    # Assim, podemos fazer uma função unscramble, que desfazer o procedimento da função scramble. Veja que isso prova
    # que a função scramble é reversivel.
    
    pre = os.urandom(SIZE)
    pre_scrambled = scramble_block(pre)
    pre_unscrambled = unscramble_block(pre_scrambled)

    if pre == pre_unscrambled:
        print("A operação scramble é reversível!")

    print("------------------------------------------------------------------------------------------")

def solucao():

    # Uma mensagem com 32 caracteres possui apenas 1 bloco. Portanto, a etapa abaixo é executada apenas uma vez.

    #for i,b in enumerate(msg_blocks):
    #    mix_in = scramble_block(b)
    #    for _ in range(i):                              -> i = 1, portanto temos apenas uma única execução disso
    #        mix_in = rotate_right(mix_in, i+11)           |
    #        mix_in = xor(mix_in, X_bytes)                 |
    #        mix_in = rotate_left(mix_in, i+6)             |
    #    initial_state = xor(initial_state,mix_in)       
    #return initial_state.hex()

    # Assim, a criptografia acaba sendo somente:

    #mix_in = scramble_block(b)
    #mix_in = rotate_right(mix_in, 12)
    #mix_in = xor(mix_in, X_bytes)
    #mix_in = rotate_left(mix_in, 7)

    # E, assim, podemos criar um reverso disso.

    primeira_entrada = b"\x00" * 32

    ext = rotate_right(primeira_entrada, 1 + 6)
    ext = xor(ext, X_bytes)
    ext = rotate_left(ext, 1 + 11)
    ext = unscramble_block(ext)

    # Esse processo produz uma extensão que pode ser concatenada à uma mensagem arbitrária para produzir uma hash
    # idêntica à hash produzida na mensagem arbitrária. 

    #print(cryptohash(primeira_entrada))
    #print(bytes.hex(ext))

    # A variável ext contém um texto que, quando jogado no algoritmo de criptografia, devolve 0000...0000.
    # Veja:

    teste = scramble_block(ext)
    teste = rotate_right(teste, 12)
    teste = xor(teste, X_bytes)
    teste = rotate_left(teste, 7)

    print("O resultado é: " + bytes.hex(teste))

    # Isso significa que, partindo de uma mensagem arbitrária com 32 bits, podemos simplesmente
    # concatenar a variável ext, para obter exatramente a mesma hash que a mensagem arbitrária produziria.
    # Assim, a tarefa de encontrar a colisão está cumprida.


    print("------------------------------------------------------------------------------------------")
    msg = os.urandom(32)
    
    print("A mensagem original é " + str(bytes.hex(msg)) + " e sua hash é " + cryptohash(msg))
    print("A mensagem concatenada é " + str(bytes.hex(msg+ext)) + " e sua hash é " + cryptohash(msg + ext))
    

explicar_padding()
explicar_reverso()
solucao()