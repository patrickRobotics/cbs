from spyne import Application, rpc, ServiceBase, Unicode, Integer, Double, DateTime
from spyne import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from datetime import datetime


# Define enums matching the WSDL
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


# Define complex types with proper namespace and element names
class CustomerType(ComplexModel):
    __namespace__ = "http://credable.io/cbs/customer"

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


# Define request/response as top-level elements
class CustomerRequest(ComplexModel):
    __namespace__ = "http://credable.io/cbs/customer"
    __type_name__ = "CustomerRequest"  # Explicitly set to match WSDL
    customerNumber = Unicode()


class CustomerResponse(ComplexModel):
    __namespace__ = "http://credable.io/cbs/customer"
    __type_name__ = "CustomerResponse"  # Explicitly set to match WSDL
    customer = CustomerType


# Create the service with exact WSDL matching
class CustomerPortService(ServiceBase):
    @rpc(CustomerRequest, _returns=CustomerResponse, _body_style="bare",
         _in_message_name="CustomerRequest", _out_message_name="CustomerResponse")
    def Customer(ctx, request):
        mock_customers = {
            "234774784": {
                "createdAt": datetime.now(),
                "createdDate": datetime.now(),
                "customerNumber": "CUST1001",
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
        customer_data = mock_customers.get(customer_number)

        if customer_data:
            return CustomerResponse(customer=CustomerType(**customer_data))
        else:
            return CustomerResponse(customer=CustomerType(customerNumber=customer_number))


# Create the application with proper configuration
application = Application(
    [CustomerPortService],
    'http://credable.io/cbs/customer',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
    name="CustomerPortService"
)


# WSGI application with proper routing
def soap_application(environ, start_response):
    path = environ['PATH_INFO']
    if path in ['/service/customer', '/service/customer?wsdl']:
        return WsgiApplication(application)(environ, start_response)
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'404 Not Found']


if __name__ == '__main__':
    server = make_server('0.0.0.0', 8093, soap_application)
    print("SOAP Service running at: http://localhost:8093/service/customer")
    print("WSDL available at: http://localhost:8093/service/customer?wsdl")
    server.serve_forever()