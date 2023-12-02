# My Secure MongoDB API

---

`/login`:

- methods: POST
- returns: `{"authorization-token": "ABC-TOKEN-1H-EXPIRATION"}`
- headers: `'Content-Type: application/json'`
- payload:

```json
{
  "username": "John Doe",
  "password": "my difficult pass"
}
```

---

`/get-info`:

- methods: GET
- returns: `{"userData": $USER_INFO}`
- header:

```json
{
  "authorization-token": "ABC-TOKEN-1H-EXPIRATION"
}
```
