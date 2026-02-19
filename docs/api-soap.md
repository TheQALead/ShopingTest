# SOAP API

Endpoint: `/soap/v1/TrainingShopService`
WSDL: `/soap/v1/TrainingShopService?wsdl`

Операции:
- Login(email, password)
- GetProducts(accessToken, page, search)
- GetCart(accessToken)
- CreateOrder(accessToken)
- PayOrder(accessToken, orderId, cardToken, paymentScenario)

При отсутствии токена сервис возвращает SOAP Fault `AuthRequired`.

Пример запроса для SoapUI:
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <GetProducts>
      <accessToken>...</accessToken>
      <page>1</page>
      <search>phone</search>
    </GetProducts>
  </soapenv:Body>
</soapenv:Envelope>
```
