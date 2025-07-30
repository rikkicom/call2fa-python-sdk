"""
An SDK to Rikkicom Call2FA service in Python

Requirements:
    pip install requests
"""

import requests


class ClientException(Exception):
    """Custom exception for Client errors."""

    pass


class Client:
    """
    A Python client for the Rikkicom Call2FA API.
    """

    def __init__(self, login: str, password: str):
        """
        Initializes the client, validates credentials, and authenticates to get a JWT.

        Args:
            login (str): The customer's API login.
            password (str): The customer's API password.

        Raises:
            ClientException: If login or password are not provided.
        """
        if not login:
            raise ClientException("The login parameter is empty")
        if not password:
            raise ClientException("The password parameter is empty")

        self._api_login = login
        self._api_password = password
        self._version = "v1"
        self._base_uri = "https://api-call2fa.rikkicom.io"
        self._session = requests.Session()
        self._jwt = None

        # Authenticate and store the JWT upon initialization
        self._receive_jwt()

    def _make_full_uri(self, method: str) -> str:
        """
        Creates a full URI to the specified API method.

        Args:
            method (str): The API endpoint/method.

        Returns:
            str: The complete URL for the API request.
        """
        return f"{self._base_uri}/{self._version}/{method}/"

    def _receive_jwt(self):
        """
        Receives and stores the JSON Web Token from the API.

        Raises:
            ClientException: If the authentication request fails or returns an unexpected status code.
        """
        auth_data = {
            "login": self._api_login,
            "password": self._api_password,
        }
        uri = self._make_full_uri("auth")

        try:
            response = self._session.post(uri, json=auth_data)

            if response.status_code == 200:
                response_json = response.json()
                self._jwt = response_json.get("jwt")
                if not self._jwt:
                    raise ClientException("JWT not found in authentication response.")
            else:
                raise ClientException(
                    f"Incorrect status code: {response.status_code} on authorization step"
                )

        except requests.exceptions.RequestException as e:
            raise ClientException(
                f"Cannot perform a request on authorization step: {e}"
            )

    def call(self, phone_number: str, callback_url: str = "") -> dict:
        """
        Initiates a new call.

        Args:
            phone_number (str): The phone number to call.
            callback_url (str, optional): A URL for status callbacks. Defaults to ''.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ClientException: If the request fails or the API returns an error.
        """
        if not phone_number:
            raise ClientException("The phoneNumber parameter is empty")

        headers = {"Authorization": f"Bearer {self._jwt}"}
        call_data = {
            "phone_number": phone_number,
            "callback_url": callback_url,
        }
        uri = self._make_full_uri("call")

        try:
            response = self._session.post(uri, json=call_data, headers=headers)
            if response.status_code != 201:
                raise ClientException(
                    f"Incorrect status code: {response.status_code} on call step"
                )
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ClientException(f"Cannot perform a request on call step: {e}")

    def call_via_last_digits(
        self, phone_number: str, pool_id: str, use_six_digits: bool = False
    ) -> dict:
        """
        Initiates a new call via the last digits mode.

        Args:
            phone_number (str): The phone number to call.
            pool_id (str): The ID of the number pool to use.
            use_six_digits (bool, optional): Whether to use the six-digit mode. Defaults to False.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ClientException: If the request fails or the API returns an error.
        """
        if not phone_number:
            raise ClientException("The phoneNumber parameter is empty")
        if not pool_id:
            raise ClientException("The poolID parameter is empty")

        headers = {"Authorization": f"Bearer {self._jwt}"}
        call_data = {"phone_number": phone_number}

        method = (
            f"pool/{pool_id}/call/six-digits"
            if use_six_digits
            else f"pool/{pool_id}/call"
        )
        uri = self._make_full_uri(method)

        try:
            response = self._session.post(uri, json=call_data, headers=headers)
            if response.status_code != 201:
                raise ClientException(
                    f"Incorrect status code: {response.status_code} on call step"
                )
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ClientException(f"Cannot perform a request on call step: {e}")

    def call_with_code(self, phone_number: str, code: str, lang: str) -> dict:
        """
        Initiates a new call with a verification code.

        Args:
            phone_number (str): The phone number to call.
            code (str): The verification code to be spoken.
            lang (str): The language for the spoken code.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ClientException: If the request fails or the API returns an error.
        """
        if not phone_number:
            raise ClientException("The phoneNumber parameter is empty")
        if not code:
            raise ClientException("The code parameter is empty")
        if not lang:
            raise ClientException("The lang parameter is empty")

        headers = {"Authorization": f"Bearer {self._jwt}"}
        call_data = {
            "phone_number": phone_number,
            "code": code,
            "lang": lang,
        }
        uri = self._make_full_uri("code/call")

        try:
            response = self._session.post(uri, json=call_data, headers=headers)
            if response.status_code != 201:
                raise ClientException(
                    f"Incorrect status code: {response.status_code} on call step"
                )
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ClientException(f"Cannot perform a request on call step: {e}")

    def info(self, call_id: str) -> dict:
        """
        Gets information about a call by its identifier.

        Args:
            call_id (str): The unique identifier of the call.

        Returns:
            dict: The JSON response from the API containing call information.

        Raises:
            ClientException: If the request fails or the API returns an error.
        """
        if not call_id:
            raise ClientException("The id parameter is empty")

        headers = {"Authorization": f"Bearer {self._jwt}"}
        uri = self._make_full_uri(f"call/{call_id}")

        try:
            response = self._session.get(uri, headers=headers)
            if response.status_code != 200:
                raise ClientException(f"Incorrect status code: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ClientException(f"Cannot perform a request to get the call info: {e}")

    @property
    def version(self) -> str:
        """Returns the current API version."""
        return self._version

    @version.setter
    def version(self, value: str):
        """Sets a different API version."""
        self._version = value
