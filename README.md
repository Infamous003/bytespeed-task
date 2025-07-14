# bytespeed-task

This is a FastAPI implementation of a backend service that exposes an `/identify` endpoint to handle identification for users/contacts. It links contacts if there are any similarities(email or phone number) or creates a new record in SQLite database.

The response contains with it, all the emails, phone numbers, secondary contacts, etc if any.

You can test it here: https://bytespeed-task.onrender.com/docs

## Endpoint
### `POST /identify`

#### Request body of type JSON:
```json
{
    "phoneNumber": "123456",
    "email": "lorraine@hillvalley.edu"
}
```

#### Response
Initially the DB is empty, so a new contact is created
```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": [
      "lorraine@hillvalley.edu"
    ],
    "phoneNumbers": [
      "123456"
    ],
    "secondaryContactIds": []
  }
}
```

#### Second request
```json
{
  "phoneNumber": "123456",
  "email": "mcfly@hillvalley.edu"
}
```
A new email ID with an exsiting phone number

#### Response
```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": [
      "lorraine@hillvalley.edu",
      "mcfly@hillvalley.edu"
    ],
    "phoneNumbers": [
      "123456"
    ],
    "secondaryContactIds": [
      2
    ]
  }
}
```
Notice the emails, phone numbers, and secondary IDs list. There are two emails, the first one being the primary email, followed by secondary emails, and so on. The same follows for phone numbers and secondary ids.

This contact is labelled `secondary` since a record with the same phone number already exists which happens to be `primary`.

You can futher test it at the endpoint provided.

