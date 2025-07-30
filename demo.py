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
