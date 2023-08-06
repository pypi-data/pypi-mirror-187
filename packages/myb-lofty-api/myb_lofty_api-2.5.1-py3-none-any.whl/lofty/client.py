from datetime import date
from typing import Optional

import requests
from dateutil.relativedelta import relativedelta

from lofty.client_auth import ClientAuth
from .constants import LoftyApi
from .date_functions import DateFunctions
from .pagination_options import PaginationOptions
from .requests.withdrawal import Withdrawal
from .responses import ApiResponse, ApiListResponse, BankData, CountryList, Transaction, TransactionSummary, \
    AwsCredentials, UserStatusSummary, VerificationToken, User, PaymentMethodsList, StatsSummary, TransactionsByUser, \
    PropertyOrderbook, PendingOrders, PropertyInfo, ExchangeUserInfo


class LoftyAiApi:
    def __init__(
            self,
            verbose: bool = False,
            api_host_override: str = None
    ):
        """
        Initializes the API client.

        Parameters:
        verbose (bool): Whether to print messages to the console verbosely.
        api_host_override (str): An override for the API Host defined in API Constants - only override for testing.
        """
        self._credentials = None
        self._verbose: bool = verbose

        self._api_constants: LoftyApi = LoftyApi(api_host_override)
        self._client_auth: ClientAuth = ClientAuth(
            verbose,
            api_host_override
        )

    def _request(self, method: str, path: str, params: dict = None, body: dict = None):
        url = self._api_constants.api_endpoint + path
        if self._verbose:
            print(method, url)

        s = requests.Session()
        response = s.request(
            method,
            url,
            auth=self._client_auth,
            headers={
                'Cache-Control': 'no-cache'
            },
            params=params,
            data=body
        )

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    # Returns a token if properly authenticated
    def login(self, username: str, password: str) -> AwsCredentials:
        credentials = self._client_auth.login(username, password)
        self._credentials = credentials
        return credentials

    @property
    def is_authenticated(self):
        return self._credentials is not None

    def get_user_info(self) -> Optional[User]:
        response = self._request('GET', '/users/v2/get')
        api_response = ApiResponse(response)
        if api_response.data:
            user = User(api_response.data)
            return user

        if self._verbose:
            print(f'Failed to get user. Raw response: {response}')

        return None

    def get_user_bank_data(self) -> Optional[BankData]:
        response = self._request('GET', '/users/v2/getbdata')
        api_response = ApiResponse(response)
        if api_response.data:
            bank_data = BankData(api_response.data)
            return bank_data

        if self._verbose:
            print(f'Failed to get user bank data. Raw response: {response}')

        return None

    def get_user_countries(self) -> Optional[CountryList]:
        response = self._request('GET', '/users/v2/countries')
        api_response = ApiResponse(response)
        if api_response.data:
            country_list = CountryList(api_response.data)
            return country_list

        if self._verbose:
            print(f'Failed to get country list. Raw response: {response}')

        return None

    # def update_user(self, body: dict) -> dict:
    #     return self._request('POST', '/users/v2/update', body=body)

    # def create_user(self, body: dict) -> dict:
    #     return self._request('POST', '/users/v2/create', body=body)

    # def sign_dao_agreement(self, body: dict) -> dict:
    #     return self._request('GET', '/users/v2/sign-dao-agreement', body=body)

    def get_user_status_summary(self) -> Optional[UserStatusSummary]:
        response = self._request('GET', '/users/v2/status-summary')
        api_response = ApiResponse(response)
        if api_response.data:
            status_summary = UserStatusSummary(api_response.data)
            return status_summary

        if self._verbose:
            print(f'Failed to get status summary. Raw response: {response}')

        return None

    # def submit_kyc(self, body: dict) -> dict:
    #     return self._request('POST', '/verifications/v2/submit-kyc', body=body)

    # def poll_kyc(self) -> dict:
    #     return self._request('POST', '/verifications/v2/poll-kyc', body={})

    def get_verification_tokens(self) -> Optional[VerificationToken]:
        response = self._request('GET', '/verifications/v2/getTokens')
        api_response = ApiResponse(response)
        if api_response.data:
            verification_token = VerificationToken(api_response.data)
            return verification_token

        if self._verbose:
            print(f'Failed to get verification tokens. Raw response: {response}')

        return None

    # def retry_verification(self) -> dict:
    #     return self._request('GET', '/verifications/v2/retry')

    # def get_aml_questions(self) -> dict:
    #     return self._request('POST', '/verifications/v2/submit-kyc', body={})

    def get_payment_methods(self) -> Optional[PaymentMethodsList]:
        response = self._request('GET', '/payments/v2/list-payment-methods')
        api_response = ApiListResponse(response)
        if api_response.data:
            payment_methods = PaymentMethodsList(api_response.data)
            return payment_methods

        if self._verbose:
            print(f'Failed to get payment methods. Raw response: {response}')

        return None

    def get_success_statistics_summary(self) -> Optional[StatsSummary]:
        response = self._request('GET', '/transactions/v2/stats-summary')
        api_response = ApiResponse(response)
        if api_response.data:
            stats_summary = StatsSummary(api_response.data)
            return stats_summary

        if self._verbose:
            print(f'Failed to get stats summary. Raw response: {response}')

        return None

    def get_transactions(self, pagination_options: PaginationOptions) -> Optional[TransactionsByUser]:
        if pagination_options is None:
            # Create options with sane defaults
            pagination_options = PaginationOptions()

        response = self._request('GET', '/transactions/v2/getbyuser', params=pagination_options.to_params())
        api_response = ApiResponse(response)
        if api_response.data:
            transactions = TransactionsByUser(api_response.data)
            return transactions

        if self._verbose:
            print(f'Failed to get user transactions. Raw response: {response}')

        return None

    def get_transactions_summary(self) -> Optional[TransactionSummary]:
        response = self._request('GET', '/transactions/v2/getusersummary')
        api_response = ApiResponse(response)
        if api_response.data:
            transaction_summary = TransactionSummary(api_response.data)
            return transaction_summary

        if self._verbose:
            print(f'Failed to get user transaction status summary. Raw response: {response}')

        return None

    def create_withdrawal(self, withdrawal: Withdrawal) -> dict:
        # TODO: getting 502 errors with this - may be some requirement to update user data immediately before a request
        return self._request('POST', '/transactions/v2/createwithdrawal', body=withdrawal.to_dict())

    def get_transaction_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """
        If a transaction was not found for the specified ID, the following message will be observed
        and an exception will be thrown:
            500: Internal Server Error: b'{"success":false,"status":"error","error":"Transaction not found","code":"not_found"}'
        """
        response = self._request('GET', '/transactions/v2/getTransactionById', params={
            'txnId': transaction_id
        })
        api_response = ApiResponse(response)
        if api_response.data:
            transaction = Transaction(api_response.data)
            return transaction

        if self._verbose:
            print(f'Failed to get transaction by id: {transaction_id}. Raw response: {response}')

        return None

    # def watch_transaction(self, property_id: str, transaction_id: str, order_id: str, watch_type: str):
    #     response = self._request('POST', '/exchange/v2/watchtransaction', body={
    #         'txnId': transaction_id,
    #         'orderId': order_id,
    #         'propertyId': property_id,
    #         'watchType': watch_type,
    #     })
    #     api_response = ApiResponse(response)
    #     return api_response.data

    def get_property_order_book(self, property_id: str) -> Optional[PropertyOrderbook]:
        response = self._request('GET', '/exchange/v2/getpropertyorderbook', params={
            'propertyId': property_id
        })
        api_response = ApiResponse(response)
        if api_response.data:
            orderbook = PropertyOrderbook(api_response.data)
            return orderbook

        if self._verbose:
            print(f'Failed to get orderbook by property id: {property_id}. Raw response: {response}')

        return None

    def get_pending_orders(self, property_id: str) -> Optional[PendingOrders]:
        response = self._request('GET', '/exchange/v2/getpendingorders', params={
            'propertyId': property_id
        })
        api_response = ApiResponse(response)
        if api_response.data:
            orderbook = PendingOrders(api_response.data)
            return orderbook

        if self._verbose:
            print(f'Failed to get pending orders by property id: {property_id}. Raw response: {response}')

        return None

    def get_property_info(self, property_id: str, start_date: date = None) -> Optional[PropertyInfo]:
        if start_date is None:
            start_date = date.today() - relativedelta(months=1)

        start_time = DateFunctions.date_to_unix_millis(start_date)
        response = self._request('GET', '/exchange/v2/getpropertyinfo', params={
            'propertyId': property_id,
            'startTime': start_time
        })
        api_response = ApiResponse(response)
        if api_response.data:
            orderbook = PropertyInfo(api_response.data)
            return orderbook

        if self._verbose:
            print(f'Failed to get property info by property id: {property_id}. Raw response: {response}')

        return None

    def get_exchange_user_info(self, property_id: Optional[str], all_info: bool = False) -> Optional[ExchangeUserInfo]:
        """
        Specifying 'None' for the property_id, and 'True' for all_info will return results for all properties
        """
        response = self._request('GET', '/exchange/v2/getuserinfo', params={
            'propertyId': property_id,
            'all': all_info
        })
        api_response = ApiResponse(response)
        if api_response.data:
            orderbook = ExchangeUserInfo(api_response.data)
            return orderbook

        if self._verbose:
            print(f'Failed to get exchange user info by property id: {property_id}. Raw response: {response}')

        return None

    # def get_watched_escrows(self, property_id: str) -> Optional[object]:
    #     response = self._request('GET', '/exchange/v2/getwatchedescrows', params={
    #         'propertyId': property_id
    #     })
    #     api_response = ApiResponse(response)
    #     return api_response.data

    # Many more endpoints to come! Stay tuned!
