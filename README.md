## Limits REST API

## Table of content

1. [Running](#launch)
3. [API](#apies)
4. [Credits](#credits)

## Running the app <a name="launch"></a>

```bash
$ docker-compose up -d --build
```

## API <a name="apies"></a>

1) 
    Get request with url - localhost:8080/limits
   
    Return all limits
    
    Format:
    ```json
    [
      {
         "user_id": int,
         "country": str,
         "currency": str,
         "amount": int
      }
   ]
    ```
    With status 200


2) 
    Post request with url - localhost:8080/limits
   
    Create new limit

    Format body:
    ```json
   {
      "user_id": int,
      "country": str,
      "currency": str,
      "amount": int
   }
    ```
    If body valid, return response with 200 status in format:
   ```json
   {
      "user_id": int,
      "country": str,
      "currency": str,
      "amount": int
   }
   ```
   If body invalid, return response with 400 status with format:
   ```json
   {
      "error": "invalid body"
   }
   ```
   If you try to create object, using already exists id, return response with 400 status with format:
   ```json
   {
      "error": "object with this user id exists"
   }
   ```
3) 
    Put request with url - localhost:8080/limit/{user_id}
   
    Change limit

    Format body:
    ```json
   {
      "country": str,
      "currency": str,
      "amount": int
   }
    ```
    If body valid, return response with 200 status in format:
   ```json
   {
      "user_id": int,
      "country": str,
      "currency": str,
      "amount": int
   }
   ```
   If body invalid, return response with 400 status with format:
   ```json
   {
      "error": "invalid body"
   }
   ```
   If object with given id not found , return response with 404 status with format:
   ```json
   {
      "error": "not found"
   }
   ```

4) 
    Delete request with url - localhost:8080/limit/{user_id}
   
    Delete limit

    If limit exists, return response with 200 status in format:
   ```json
   {
      "user_id": int,
      "country": str,
      "currency": str,
      "amount": int
   }
   ```
   If object with given id not found , return response with 404 status with format:
   ```json
   {
      "error": "not found"
   }
   ```

5) 
    Get request with url - localhost:8080/limit/{user_id}
    
    With optional params [year, month]   

    View limit with transactions

    If limit exists and requests made without params, return response with 200 status in format:
   ```json
   {
      "user_id": int,
      "country": str,
      "currency": str,
      "amount": int,
      "transactions": []
   }
   ```
   If limit exists and requests made wit params, return response with 200 status in format:
   ```json
   {
      "user_id": int,
      "country": str,
      "currency": str,
      "amount": int,
      "transactions": [ all transactions for selected month]
   }
   ```
   If object with given id not found , return response with 404 status with format:
   ```json
   {
      "error": "not found"
   }
   ```

6) 
    Post request with url - localhost:8080/transaction

    View for create transaction

    If limit exists and requests made without params, return response with 200 status in format:
   ```json
   {
      "user_id": int,
      "date": "yyyy-mm-dd hh:mm:ss",
      "country": str,
      "currency": str,
      "amount": int,
   }
   ```
   If transaction created, return response with 200 status in format:
   ```json
   {
      "user_id": int,
      "date": "yyyy-mm-dd hh:mm:ss",
      "country": str,
      "currency": str,
      "amount": int,
   }
   ```
   If body contains invalid amount(bad value or overlimit) , return response with 400 status with format:
   ```json
   {
    "error": "unavailable amount"
   }
   ```

## Credits <a name="credits"></a>

- Author - Yury Ledovsky
- [Telegram](https://t.me/lannoyy)
- [Github](https://github.com/lannoyy)