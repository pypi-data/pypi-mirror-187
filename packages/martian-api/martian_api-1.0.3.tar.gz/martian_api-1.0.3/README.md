# Martian Node.js Library
The martian python library allows developers to easily access the martian api.

This package should only be used server-side. Using this package client-side would expose your secret key.

## Installation
```pip install martian_api```

## Usage
Martian allows you to easily access AI models and to log the outputs from AI models.

Logging values:
```python
from martian_api import log_to_martian

inputs = ["The", "inputs", "to", "your", "function"]
outputs = "Your outputs"
logToMartian(
  {"api_key": YOUR_MARTIAN_API_KEY},
  inputs,
  outputs,
  {"martian_name": "your_function"}
)
```

Logging a function:
```python
from martian_api import with_martian

@with_martian({"api_key": YOUR_MARTIAN_API_KEY})
def your_function(args){
  // your function definition
}
```

[//]: # (Maybe add logging for functions belonging to objects)