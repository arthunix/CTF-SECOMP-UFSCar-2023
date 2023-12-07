# Gotta Go Fast

I won't have have to worry about running out of entropy, I'm going to have my OTP generated forever with this new script!

---

`/`:

- methods: POST
- returns: `{"encrypted_flag": "0x627dc942f15204fd5d6999abda043ccb44c7c1294aff5e9e612b858d3105bc7c5958c472e532268c12"}`
- headers: `'Content-Type: application/json'`
- payload:

```json
{
  "action": "get_flag"
}
```

---

`/`:                                       

- methods: POST
- returns: `{"encrypted_data": "0x627dc942f15204fd5d6999abda043ccb44c7c1294aff5e9e612b858d3105bc7c5958c472e532268c12"}`       
- headers: `'Content-Type: application/json'`
- payload:

```json
{                        
  "action": "encrypt_data",
  "data": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
```
