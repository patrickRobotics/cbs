import os
from base64 import b64decode
from spyne import (
    Application, rpc, ServiceBase, Unicode, Integer, Double, DateTime, String)
from spyne import ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

SOAP_USER = os.getenv('USER_NAME')
SOAP_PASS = os.getenv('PASSWORD')

# Authentication credentials
VALID_CREDENTIALS = {
    SOAP_USER: SOAP_PASS
}


def authenticate(environ):
    """Check HTTP Basic Authentication"""
    auth_header = environ.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return False

    try:
        auth_type, auth_string = auth_header.split(None, 1)
        if auth_type.lower() != 'basic':
            return False

        decoded = b64decode(auth_string).decode('utf-8')
        username, password = decoded.split(':', 1)
        return VALID_CREDENTIALS.get(username) == password
    except Exception:
        return False


class AuthenticatedWsgiApplication(WsgiApplication):
    """WSGI middleware that adds authentication measures"""

    def __call__(self, environ, start_response):
        if not authenticate(environ):
            start_response('401 Unauthorized', [
                ('Content-Type', 'text/plain'),
                ('WWW-Authenticate', 'Basic realm="SOAP API"')
            ])
            return [b'Authentication required']

        return super().__call__(environ, start_response)


# ================== COMMON ENUMS ==================
class Gender(Unicode):
    class Values:
        MALE = "MALE"
        FEMALE = "FEMALE"


class IdType(Unicode):
    class Values:
        PASSPORT = "PASSPORT"
        NATIONAL_ID = "NATIONAL_ID"
        DRIVERS_LICENSE = "DRIVERS_LICENSE"
        VOTERS_ID = "VOTERS_ID"


class Status(Unicode):
    class Values:
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"


class Currency(Unicode):
    class Values:
        TZS = "TZS"
        KES = "KES"
        UGX = "UGX"
        USD = "USD"
        GBP = "GBP"
        EURO = "EURO"
        PKR = "PKR"
        NGN = "NGN"
        EGP = "EGP"
        ETB = "ETB"


# ================== KYC SERVICE ==================
class CustomerType(ComplexModel):
    __namespace__ = "http://credable.io/cbs/customer"
    __type_name__ = "customer"

    createdAt = DateTime(min_occurs=0)
    createdDate = DateTime(min_occurs=0)
    customerNumber = Unicode(min_occurs=0)
    dob = DateTime(min_occurs=0)
    email = Unicode(min_occurs=0)
    firstName = Unicode(min_occurs=0)
    gender = Gender(min_occurs=0)
    id = Integer(min_occurs=0)
    idNumber = Unicode(min_occurs=0)
    idType = IdType(min_occurs=0)
    lastName = Unicode(min_occurs=0)
    middleName = Unicode(min_occurs=0)
    mobile = Unicode(min_occurs=0)
    monthlyIncome = Double()
    status = Status(min_occurs=0)
    updatedAt = DateTime(min_occurs=0)


class CustomerRequest(ComplexModel):
    __namespace__ = "http://credable.io/cbs/customer"
    __type_name__ = "CustomerRequest"
    customerNumber = Unicode()


class CustomerResponse(ComplexModel):
    __namespace__ = "http://credable.io/cbs/customer"
    __type_name__ = "CustomerResponse"
    customer = CustomerType


class CustomerPortService(ServiceBase):
    @rpc(CustomerRequest, _returns=CustomerResponse,
         _body_style="bare", _in_message_name="CustomerRequest", _out_message_name="CustomerResponse")
    def Customer(ctx, request):
        mock_customers = {
            "234774784": {
                "createdAt": datetime.now(),
                "createdDate": datetime.now(),
                "customerNumber": "234774784",
                "dob": datetime(1985, 5, 20),
                "email": "john.doe@example.com",
                "firstName": "John",
                "gender": "MALE",
                "id": 1001,
                "idNumber": "A12345678",
                "idType": "NATIONAL_ID",
                "lastName": "Doe",
                "mobile": "+255123456789",
                "monthlyIncome": 2500.00,
                "status": "ACTIVE",
                "updatedAt": datetime.now()
            },
            "318411216": {
                "createdAt": datetime.now(),
                "createdDate": datetime.now(),
                "customerNumber": "318411216",
                "dob": datetime(2001, 1, 2),
                "email": "john.doe@example.com",
                "firstName": "John",
                "gender": "MALE",
                "id": 1002,
                "idNumber": "318411216",
                "idType": "NATIONAL_ID",
                "lastName": "Doe",
                "mobile": "+255123456789",
                "monthlyIncome": 500.00,
                "status": "ACTIVE",
                "updatedAt": datetime.now()
            },
            "340397370": {
                "createdAt": datetime.now(),
                "createdDate": datetime.now(),
                "customerNumber": "340397370",
                "dob": datetime(1999, 9, 20),
                "email": "john.doe@example.com",
                "firstName": "John",
                "gender": "MALE",
                "id": 1003,
                "idNumber": "340397370",
                "idType": "NATIONAL_ID",
                "lastName": "Doe",
                "mobile": "+255123456789",
                "monthlyIncome": 5000.00,
                "status": "ACTIVE",
                "updatedAt": datetime.now()
            },
            "366585630": {
                "createdAt": datetime.now(),
                "createdDate": datetime.now(),
                "customerNumber": "366585630",
                "dob": datetime(2009, 9, 20),
                "email": "john.doe@example.com",
                "firstName": "John",
                "gender": "MALE",
                "id": 1004,
                "idNumber": "366585630",
                "idType": "NATIONAL_ID",
                "lastName": "Doe",
                "mobile": "+255123456789",
                "monthlyIncome": 2000.00,
                "status": "ACTIVE",
                "updatedAt": datetime.now()
            },
            "397178638": {
                "createdAt": datetime.now(),
                "createdDate": datetime.now(),
                "customerNumber": "397178638",
                "dob": datetime(2000, 3, 20),
                "email": "john.doe@example.com",
                "firstName": "John",
                "gender": "MALE",
                "id": 1005,
                "idNumber": "397178638",
                "idType": "NATIONAL_ID",
                "lastName": "Doe",
                "mobile": "+255123456789",
                "monthlyIncome": 2000.00,
                "status": "ACTIVE",
                "updatedAt": datetime.now()
            }
        }

        customer_number = request.customerNumber
        customer_data = mock_customers.get(customer_number, {})
        return CustomerResponse(customer=CustomerType(**customer_data))


# ================== TRANSACTION SERVICE ==================
class TransactionDataType(ComplexModel):
    __namespace__ = "http://credable.io/cbs/transaction"
    __type_name__ = "transactionData"

    accountNumber = Unicode(min_occurs=0, max_length=24)
    alternativechanneltrnscrAmount = Double()
    alternativechanneltrnscrNumber = Integer()
    alternativechanneltrnsdebitAmount = Double()
    alternativechanneltrnsdebitNumber = Integer()
    atmTransactionsNumber = Integer()
    atmtransactionsAmount = Double()
    bouncedChequesDebitNumber = Integer()
    bouncedchequescreditNumber = Integer()
    bouncedchequetransactionscrAmount = Double()
    bouncedchequetransactionsdrAmount = Double()
    chequeDebitTransactionsAmount = Double()
    chequeDebitTransactionsNumber = Double()
    createdAt = Unicode(min_occurs=0, max_length=14)
    createdDate = Unicode(min_occurs=0, max_length=14)
    credittransactionsAmount = Double()
    debitcardpostransactionsAmount = Double()
    debitcardpostransactionsNumber = Double()
    fincominglocaltransactioncrAmount = Double()
    id = Integer()
    incominginternationaltrncrAmount = Double()
    incominginternationaltrncrNumber = Integer()
    incominglocaltransactioncrNumber = Integer()
    intrestAmount = Integer()
    lastTransactionDate = Unicode(min_occurs=0, max_length=14)
    lastTransactionType = String()
    lastTransactionValue = Integer()
    maxAtmTransactions = Double()
    maxMonthlyBebitTransactions = Double()
    maxalternativechanneltrnscr = Double()
    maxalternativechanneltrnsdebit = Double()
    maxbouncedchequetransactionscr = Double()
    maxchequedebittransactions = Double()
    maxdebitcardpostransactions = Double()
    maxincominginternationaltrncr = Double()
    maxincominglocaltransactioncr = Double()
    maxmobilemoneycredittrn = Double()
    maxmobilemoneydebittransaction = Double()
    axmonthlycredittransactions = Double()
    maxoutgoinginttrndebit = Double()
    maxoutgoinglocaltrndebit = Double()
    maxoverthecounterwithdrawals = Double()
    minAtmTransactions = Double()
    minMonthlyDebitTransactions = Double()
    minalternativechanneltrnscr = Double()
    minalternativechanneltrnsdebit = Double()
    minbouncedchequetransactionscr = Double()
    minchequedebittransactions = Double()
    mindebitcardpostransactions = Double()
    minincominglocaltransactioncr = Double()
    minincominginternationaltrncr = Double()
    minmobilemoneycredittrn = Double()
    minmobilemoneydebittransaction = Double()
    minmonthlycredittransactions = Double()
    minoutgoinginttrndebit = Double()
    minoutgoinglocaltrndebit = Double()
    minoverthecounterwithdrawals = Double()
    mobilemoneycredittransactionAmount = Double()
    mobilemoneycredittransactionNumber = Integer()
    mobilemoneydebittransactionAmount = Double()
    mobilemoneydebittransactionNumber = Integer()
    monthlyBalance = Double()
    monthlydebittransactionsAmount = Double()
    outgoinginttransactiondebitAmount = Double()
    outgoinginttrndebitNumber = Integer()
    outgoinglocaltransactiondebitAmount = Double()
    outgoinglocaltransactiondebitNumber = Integer()
    overdraftLimit = Double()
    overthecounterwithdrawalsAmount = Double()
    overthecounterwithdrawalsNumber = Integer()
    transactionValue = Double()
    updatedAt = Unicode(min_occurs=0, max_length=14)


class TransactionsRequest(ComplexModel):
    __namespace__ = "http://credable.io/cbs/transaction"
    __type_name__ = "TransactionsRequest"
    customerNumber = Unicode()


class TransactionsResponse(ComplexModel):
    __namespace__ = "http://credable.io/cbs/transaction"
    __type_name__ = "TransactionsResponse"
    transactions = Array(TransactionDataType)


class TransactionDataPortService(ServiceBase):
    @rpc(TransactionsRequest, _returns=TransactionsResponse,
         _body_style="bare",
         _in_message_name="TransactionsRequest",
         _out_message_name="TransactionsResponse")
    def Transactions(ctx, request):
        mock_transactions = {
            "234774784": [
                {
                    "accountNumber": "332216783322167555621628",
                    "alternativechanneltrnscrAmount": 27665.6889301,
                    "alternativechanneltrnscrNumber": 0,
                    "alternativechanneltrnsdebitAmount": 2.9997265951905E7,
                    "alternativechanneltrnsdebitNumber": 114,
                    "atmTransactionsNumber": 36934417,
                    "atmtransactionsAmount": 192538.94,
                    "bouncedChequesDebitNumber": 535,
                    "bouncedchequescreditNumber": 0,
                    "bouncedchequetransactionscrAmount": 1.37,
                    "bouncedchequetransactionsdrAmount": 2602.4,
                    "chequeDebitTransactionsAmount": 2765.57,
                    "chequeDebitTransactionsNumber": 6,
                    "createdAt": "1401263420000",
                    "createdDate": "1350538588000",
                    "credittransactionsAmount": 0.0,
                    "debitcardpostransactionsAmount": 117347.063,
                    "debitcardpostransactionsNumber": 931309756,
                    "fincominglocaltransactioncrAmount": 2552389.4,
                    "id": 5,
                    "incominginternationaltrncrAmount": 76.160425,
                    "incominginternationaltrncrNumber": 285700400,
                    "incominglocaltransactioncrNumber": 1,
                    "intrestAmount": 22,
                    "lastTransactionDate": "554704439000",
                    "lastTransactionType": "Null",
                    "lastTransactionValue": 1,
                    "maxAtmTransactions": 0.0,
                    "maxMonthlyBebitTransactions": 7.8272009E7,
                    "maxalternativechanneltrnscr": 0.0,
                    "maxalternativechanneltrnsdebit": 0.0,
                    "maxbouncedchequetransactionscr": 0.0,
                    "maxchequedebittransactions": 0.0,
                    "maxdebitcardpostransactions": 5.468080253826023E15,
                    "maxincominginternationaltrncr": 0.0,
                    "maxincominglocaltransactioncr": 0.0,
                    "maxmobilemoneycredittrn": 0.0,
                    "maxmobilemoneydebittransaction": 0.0,
                    "axmonthlycredittransactions": 0.0,
                    "maxoutgoinginttrndebit": 0.0,
                    "axoutgoinglocaltrndebit": 0.0,
                    "maxoverthecounterwithdrawals": 6.09866462E8,
                    "minAtmTransactions": 0.0,
                    "minMonthlyDebitTransactions": 0.0,
                    "minalternativechanneltrnscr": 0.0,
                    "minalternativechanneltrnsdebit": 0.0,
                    "minbouncedchequetransactionscr": 0.0,
                    "minchequedebittransactions": 0.0,
                    "mindebitcardpostransactions": 4.716295906413E12,
                    "minincominginternationaltrncr": 0.0,
                    "minincominglocaltransactioncr": 0.0,
                    "minmobilemoneycredittrn": 0.0,
                    "maxoutgoinglocaltrndebit": 0.0,
                    "minmobilemoneydebittransaction": 0.0,
                    "minmonthlycredittransactions": 29624.78,
                    "minoutgoinginttrndebit": 0.0,
                    "minoutgoinglocaltrndebit": 0.0,
                    "minoverthecounterwithdrawals": 1.00927826E8,
                    "mobilemoneycredittransactionAmount": 349693.8071922,
                    "mobilemoneycredittransactionNumber": 4092,
                    "mobilemoneydebittransactionAmount": 1.87382823746E7,
                    "mobilemoneydebittransactionNumber": 0,
                    "monthlyBalance": 2205.0,
                    "monthlydebittransactionsAmount": 295.6677,
                    "outgoinginttransactiondebitAmount": 9.561730814,
                    "outgoinginttrndebitNumber": 0,
                    "outgoinglocaltransactiondebitAmount": 56.03,
                    "outgoinglocaltransactiondebitNumber": 0,
                    "overdraftLimit": 7.0,
                    "overthecounterwithdrawalsAmount": 3.72849038239E8,
                    "overthecounterwithdrawalsNumber": 546382904,
                    "transactionValue": 3500.0,
                    "upDatedAt": "773556430000"
                }
            ]
        }

        customer_number = request.customerNumber
        transactions = mock_transactions.get(customer_number, [])
        return TransactionsResponse(transactions=transactions)


# ================== APPLICATION SETUP ==================
kyc_app = Application(
    [CustomerPortService],
    'http://credable.io/cbs/customer',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
    name='CustomerPortService'
)

transaction_app = Application(
    [TransactionDataPortService],
    'http://credable.io/cbs/transaction',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
    name='TransactionDataPortService'
)


# ================== WSGI DISPATCHER WITH AUTH ==================
def soap_dispatcher(environ, start_response):
    path = environ['PATH_INFO']

    if path == '/service/customer' or path == '/service/customer?wsdl':
        return AuthenticatedWsgiApplication(kyc_app)(environ, start_response)
    elif path == '/service/transaction-data' or path == '/service/transaction-data?wsdl':
        return AuthenticatedWsgiApplication(transaction_app)(environ, start_response)

    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'404 Not Found']


# ================== MAIN SERVER ==================
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8001, soap_dispatcher)
    print(" - KYC Service: http://localhost:8001/service/customer")
    print(" - Transaction Service: http://localhost:8001/service/transaction-data")
    server.serve_forever()
