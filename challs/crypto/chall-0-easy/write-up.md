# Gotta Go Fast

## Passos
1. A criptografia desse challenge pode-se observar que se baseia na função `time.time()` do python, o que nos faz pensar que, se duas mensagens forem criptografadas ao "mesmo tempo", a chave usada para criptografia das duas seria a mesma.
2. Portanto, o primeiro passo essencial para completar esse desafio é **conseguir enviar duas mensagens ao mesmo tempo para serem criptografadas**. 
3. Isso pode ser feito manualmente, enviando dois JSONs ao mesmo tempo para o arquivo, ou através que scripts que mandem e recebam respostas desse algoritmo.

Exemplo de trecho possível de código:
```python3
# ...

og_data = 0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# print (og_data)
# print (hex(og_data))

enc_data = 0x9bb2008736a8f919c5f04860029dc911cf090cb0d03b876badb55c53a8dd49a29bb2008736a8f919c5
# print (enc_data)
# print (hex(enc_data))

key = int(enc_data ^ og_data)
# print (key)
# print (hex(key))

enc_flag = 0x627dc942f15204fd5d6999abda043ccb44c7c1294aff5e9e612b858d3105bc7c5958c472e532268c12

decoded = bytes.fromhex(hex(key ^ enc_flag).removeprefix('0x'))
print(decoded)
```
