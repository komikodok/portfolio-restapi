# GET /assistant/

## Response
```json
    {
        "status": "<string>",
        "data": {
            "generation": "<string>",
            "image_url": "<string>"
        }
    }
```

# POST /assistant/

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
        "data": {
            "generation": "<string>",
            "image_url": "<string>"
        }
    }
```

## Error
```json
    {
        "status": "<string>",
        "data": {
            "generation": "<string>",
            "image_url": "<string>"
        }
    }
```