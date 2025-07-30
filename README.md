# Python SDK for Call2FA

This is a library you can use for Rikkicom's service named as Call2FA (a phone call as the second factor in an authorization pipeline).

## Installation

Just copy `call2fa/client.py` to your code base:

## Example

This simple code makes a new call to the +380631010121 number:

```python
from call2fa.sdk import Client, ClientException

if __name__ == "__main__":
    # API credentials
    login = "***"
    password = "***"

    # Configuration for this call
    call_to = "+380631010121"
    callback_url = "https://httpbin.org/post"

    try:
        # Create the Call2FA client
        client = Client(login, password)

        # Make a call
        response = client.call(call_to, callback_url)
        print(response)
    except ClientException as e:
        print("Something went wrong:")
        print(e)

    # Result looks like the following:
    # {'call_id': '95818344'}
```

- Documentation: https://api.rikkicom.io/docs/en/call2fa/
- Documentation (in Ukrainian): https://api.rikkicom.io/docs/uk/call2fa/
- Documentation (in Russian): https://api.rikkicom.io/docs/ru/call2fa/
