import requests
headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer EkPStIDeOHijeTh19kgSv3hRG7fg'
        }

payload = {
            "BusinessShortCode": 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMxMDE2MTAwNjM1",
            "Timestamp": "20231016100635",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": 254746727592,
            "PartyB": 174379,
            "PhoneNumber": 254708374149,
            "CallBackURL": "https://461d-41-210-145-7.ngrok-free.app/stk",
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X" 
        }
response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
print(response.text.encode('utf8'))