# POST /contact/

## Body
```json
    { 
        "prompt": "<string>"
    }
```

## Headers
```json
    {
        "Content-Type": "application/json",
        "X-CSRFToken": "<token>"
    }
```

## Response
```json
    {
        "status": "<string>",
    }
```

## Error
```json
    {
        "status": "<string>",
        "error": "<list> | <string>"
    }
```