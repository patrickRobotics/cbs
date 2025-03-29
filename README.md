# CORE Banking Service

## Introduction and Setup
This service mocks a Core Banking Service (CBS) that exposes 2 endpoints to get customerKyc and get customer's 
transactions. The Mock responses and requests were developed from the WSDL endpoints:

KYC: https://kycapitest.credable.io/service/customerWsdl.wsdl
Transactions: https://trxapitest.credable.io/service/transactionWsdl.wsdl

For testing purposes, only one customer number has been used across the other services; `234774784`

### Create a **.env** file to store secret variables for your environment and populate values for the keys listed below:
```
USER_NAME=              # Username for uthentication against the CBS Soap service
PASSWORD=               # Password for users accessing this middleware
```

### Create virtual environment
`python3 -m venv .venv`

`source .venv/bin/activate`
### Install dependencies
`pip install -r requirements.txt`

### Start the service
`flask run --host=0.0.0.0 --port=8003`

## Testing this middleware transactions API
POST `<HOST_URL>/service/customer` including Basic Auth credentials.

Body:
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:cust="http://credable.io/cbs/customer">
   <soapenv:Header/>
   <soapenv:Body>
      <cust:CustomerRequest>
         <cust:customerNumber>234774784</cust:customerNumber>
      </cust:CustomerRequest>
   </soapenv:Body>
</soapenv:Envelope>
```

Response:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://credable.io/cbs/customer">
    <soap11env:Body>
        <tns:CustomerResponse>
            <tns:customer>
                <tns:createdAt>2025-03-29T05:33:24.240449</tns:createdAt>
                <tns:createdDate>2025-03-29T05:33:24.240459</tns:createdDate>
                <tns:customerNumber>234774784</tns:customerNumber>
                <tns:dob>1985-05-20T00:00:00</tns:dob>
                <tns:email>john.doe@example.com</tns:email>
                <tns:firstName>John</tns:firstName>
                <tns:gender>MALE</tns:gender>
                <tns:id>1001</tns:id>
                <tns:idNumber>A12345678</tns:idNumber>
                <tns:idType>NATIONAL_ID</tns:idType>
                <tns:lastName>Doe</tns:lastName>
                <tns:mobile>+255123456789</tns:mobile>
                <tns:monthlyIncome>2500.0</tns:monthlyIncome>
                <tns:status>ACTIVE</tns:status>
                <tns:updatedAt>2025-03-29T05:33:24.240464</tns:updatedAt>
            </tns:customer>
        </tns:CustomerResponse>
    </soap11env:Body>
</soap11env:Envelope>
```


POST `<HOST_URL>/service/transaction-data` including Basic Auth credentials

Body: 
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tran="http://credable.io/cbs/transaction">
    <soapenv:Header/>
    <soapenv:Body>
        <tran:TransactionsRequest>
            <tran:customerNumber>234774784</tran:customerNumber>
        </tran:TransactionsRequest>
    </soapenv:Body>
</soapenv:Envelope>
```

Response:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://credable.io/cbs/transaction">
    <soap11env:Body>
        <tns:TransactionsResponse>
            <tns:transactions>
                <tns:transactionData>
                    <tns:accountNumber>332216783322167555621628</tns:accountNumber>
                    <tns:alternativechanneltrnscrAmount>27665.6889301</tns:alternativechanneltrnscrAmount>
                    <tns:alternativechanneltrnscrNumber>0</tns:alternativechanneltrnscrNumber>
                    <tns:alternativechanneltrnsdebitAmount>29997265.951905</tns:alternativechanneltrnsdebitAmount>
                    <tns:alternativechanneltrnsdebitNumber>114</tns:alternativechanneltrnsdebitNumber>
                    <tns:atmTransactionsNumber>36934417</tns:atmTransactionsNumber>
                    <tns:atmtransactionsAmount>192538.94</tns:atmtransactionsAmount>
                    <tns:bouncedChequesDebitNumber>535</tns:bouncedChequesDebitNumber>
                    <tns:bouncedchequescreditNumber>0</tns:bouncedchequescreditNumber>
                    <tns:bouncedchequetransactionscrAmount>1.37</tns:bouncedchequetransactionscrAmount>
                    <tns:bouncedchequetransactionsdrAmount>2602.4</tns:bouncedchequetransactionsdrAmount>
                    <tns:chequeDebitTransactionsAmount>2765.57</tns:chequeDebitTransactionsAmount>
                    <tns:chequeDebitTransactionsNumber>6</tns:chequeDebitTransactionsNumber>
                    <tns:createdAt>1401263420000</tns:createdAt>
                    <tns:createdDate>1350538588000</tns:createdDate>
                    <tns:credittransactionsAmount>0.0</tns:credittransactionsAmount>
                    <tns:debitcardpostransactionsAmount>117347.063</tns:debitcardpostransactionsAmount>
                    <tns:debitcardpostransactionsNumber>931309756</tns:debitcardpostransactionsNumber>
                    <tns:fincominglocaltransactioncrAmount>2552389.4</tns:fincominglocaltransactioncrAmount>
                    <tns:id>5</tns:id>
                    <tns:incominginternationaltrncrAmount>76.160425</tns:incominginternationaltrncrAmount>
                    <tns:incominginternationaltrncrNumber>285700400</tns:incominginternationaltrncrNumber>
                    <tns:incominglocaltransactioncrNumber>1</tns:incominglocaltransactioncrNumber>
                    <tns:intrestAmount>22</tns:intrestAmount>
                    <tns:lastTransactionDate>554704439000</tns:lastTransactionDate>
                    <tns:lastTransactionType>Null</tns:lastTransactionType>
                    <tns:lastTransactionValue>1</tns:lastTransactionValue>
                    <tns:maxAtmTransactions>0.0</tns:maxAtmTransactions>
                    <tns:maxMonthlyBebitTransactions>78272009.0</tns:maxMonthlyBebitTransactions>
                    <tns:maxalternativechanneltrnscr>0.0</tns:maxalternativechanneltrnscr>
                    <tns:maxalternativechanneltrnsdebit>0.0</tns:maxalternativechanneltrnsdebit>
                    <tns:maxbouncedchequetransactionscr>0.0</tns:maxbouncedchequetransactionscr>
                    <tns:maxchequedebittransactions>0.0</tns:maxchequedebittransactions>
                    <tns:maxdebitcardpostransactions>5468080253826023.0</tns:maxdebitcardpostransactions>
                    <tns:maxincominginternationaltrncr>0.0</tns:maxincominginternationaltrncr>
                    <tns:maxincominglocaltransactioncr>0.0</tns:maxincominglocaltransactioncr>
                    <tns:maxmobilemoneycredittrn>0.0</tns:maxmobilemoneycredittrn>
                    <tns:maxmobilemoneydebittransaction>0.0</tns:maxmobilemoneydebittransaction>
                    <tns:axmonthlycredittransactions>0.0</tns:axmonthlycredittransactions>
                    <tns:maxoutgoinginttrndebit>0.0</tns:maxoutgoinginttrndebit>
                    <tns:maxoutgoinglocaltrndebit>0.0</tns:maxoutgoinglocaltrndebit>
                    <tns:maxoverthecounterwithdrawals>609866462.0</tns:maxoverthecounterwithdrawals>
                    <tns:minAtmTransactions>0.0</tns:minAtmTransactions>
                    <tns:minMonthlyDebitTransactions>0.0</tns:minMonthlyDebitTransactions>
                    <tns:minalternativechanneltrnscr>0.0</tns:minalternativechanneltrnscr>
                    <tns:minalternativechanneltrnsdebit>0.0</tns:minalternativechanneltrnsdebit>
                    <tns:minbouncedchequetransactionscr>0.0</tns:minbouncedchequetransactionscr>
                    <tns:minchequedebittransactions>0.0</tns:minchequedebittransactions>
                    <tns:mindebitcardpostransactions>4716295906413.0</tns:mindebitcardpostransactions>
                    <tns:minincominglocaltransactioncr>0.0</tns:minincominglocaltransactioncr>
                    <tns:minincominginternationaltrncr>0.0</tns:minincominginternationaltrncr>
                    <tns:minmobilemoneycredittrn>0.0</tns:minmobilemoneycredittrn>
                    <tns:minmobilemoneydebittransaction>0.0</tns:minmobilemoneydebittransaction>
                    <tns:minmonthlycredittransactions>29624.78</tns:minmonthlycredittransactions>
                    <tns:minoutgoinginttrndebit>0.0</tns:minoutgoinginttrndebit>
                    <tns:minoutgoinglocaltrndebit>0.0</tns:minoutgoinglocaltrndebit>
                    <tns:minoverthecounterwithdrawals>100927826.0</tns:minoverthecounterwithdrawals>
                    <tns:mobilemoneycredittransactionAmount>349693.8071922</tns:mobilemoneycredittransactionAmount>
                    <tns:mobilemoneycredittransactionNumber>4092</tns:mobilemoneycredittransactionNumber>
                    <tns:mobilemoneydebittransactionAmount>18738282.3746</tns:mobilemoneydebittransactionAmount>
                    <tns:mobilemoneydebittransactionNumber>0</tns:mobilemoneydebittransactionNumber>
                    <tns:monthlyBalance>2205.0</tns:monthlyBalance>
                    <tns:monthlydebittransactionsAmount>295.6677</tns:monthlydebittransactionsAmount>
                    <tns:outgoinginttransactiondebitAmount>9.561730814</tns:outgoinginttransactiondebitAmount>
                    <tns:outgoinginttrndebitNumber>0</tns:outgoinginttrndebitNumber>
                    <tns:outgoinglocaltransactiondebitAmount>56.03</tns:outgoinglocaltransactiondebitAmount>
                    <tns:outgoinglocaltransactiondebitNumber>0</tns:outgoinglocaltransactiondebitNumber>
                    <tns:overdraftLimit>7.0</tns:overdraftLimit>
                    <tns:overthecounterwithdrawalsAmount>372849038.239</tns:overthecounterwithdrawalsAmount>
                    <tns:overthecounterwithdrawalsNumber>546382904</tns:overthecounterwithdrawalsNumber>
                    <tns:transactionValue>3500.0</tns:transactionValue>
                </tns:transactionData>
            </tns:transactions>
        </tns:TransactionsResponse>
    </soap11env:Body>
</soap11env:Envelope>
```