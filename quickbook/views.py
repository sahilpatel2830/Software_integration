from http.client import responses

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer, NestedInvoiceSerializer, EmployeeSerializer, TimeactivitySerializer
from .token_auth import QuickbookAuth
from decouple import config
import requests


class QuickBookBaseView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth = QuickbookAuth()
        self.access_token = config('ACCESS_TOKEN')
        self.realm_id = config('REALM_ID')

    def get_header(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def send_request(self, url, method, data=None, params=None):
        headers = self.get_header()
        try:
            response = requests.request(method, url, json=data, headers=headers, params=params)
            if response.status_code == 401:
                self.access_token = self.auth.get_new_access_token()
                if not self.access_token:
                    return Response({"error": "Unable to get access token."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                headers = self.get_header()
                response = requests.request(method, url, json=data, headers=headers, params=params)
            return response
        except requests.exceptions.RequestException as e:
            error_message = response if isinstance(response, str) else response.json()

            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeCreateView(QuickBookBaseView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        employee_data = serializer.data

        query = (
            f"SELECT * FROM Employee WHERE GivenName = '{employee_data['GivenName']}' "
            f"AND FamilyName = '{employee_data['FamilyName']}'"
        )
        quickbooks_query_url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/query?minorversion=73'
        query_response = self.send_request(quickbooks_query_url, 'get', params={'query': query})

        if query_response.status_code == 200:
            data = query_response.data
            if data.get('QueryResponse', {}).get('Employee'):
                return Response({"message": f"Employee with the GivenName {employee_data['GivenName']} and FamilyName {employee_data['FamilyName']} is already exists."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Somthing went wrong.Please try again later."}, status=status.HTTP_400_BAD_REQUEST)

        quickbooks_url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/employee?minorversion=73'
        create_emp_response = self.send_request(quickbooks_url, 'post', data=employee_data)

        if create_emp_response.status_code == 200:
            return create_emp_response
        else:
            return Response({"message": "Somthing went wrong. Please try again later.","error": create_emp_response.text}, status=status.HTTP_400_BAD_REQUEST)


class QuickBooksInvoiceCreateView(QuickBookBaseView):
    def post(self, request):
        serializer = NestedInvoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        invoice_data = serializer.data
        url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/invoice?minorversion=40'
        return self.send_request(url, 'post', invoice_data)

        # if create_invoice_response.status_code == 200:
        #     return create_invoice_response
        # else:
        #     return Response({"message": "Somthing went wrong. Please try again later.","error": create_invoice_response.text}, status=status.HTTP_400_BAD_REQUEST)
        #

class QuickBooksCustomerCreateView(QuickBookBaseView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        customer_data = serializer.data
        url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/customer?minorversion=73'
        create_customer_response =  self.send_request(url, 'post', customer_data)

        if create_customer_response.status_code == 200:
            return create_customer_response

        elif create_customer_response.status_code >= 400 and create_customer_response.status_code < 500:
            return Response({"message": "Bad request.","error": create_customer_response.json()}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Somthing went wrong. Please try again later.","error": create_customer_response.text}, status=status.HTTP_400_BAD_REQUEST)


class QuickBookTimeActivity(QuickBookBaseView):
    def post(self, request):
        serializer = TimeactivitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        timeactivity_Data = serializer.data
        url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/9341452978640153/timeactivity?minorversion=73'
        create_timeactivity_response = self.send_request(url, 'post', timeactivity_Data)

        if create_timeactivity_response.status_code == 200:
            return create_timeactivity_response
        else:
            return Response(
                {"message": "Somthing went wrong. Please try again later.", "error": create_timeactivity_response.text},
                status=status.HTTP_400_BAD_REQUEST)


