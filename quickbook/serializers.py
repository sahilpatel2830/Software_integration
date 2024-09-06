from rest_framework import serializers

class SalesItemLineDetailSerializer(serializers.Serializer):
    ServiceDate = serializers.CharField(required=False)
    Qty = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    UnitPrice = serializers.DecimalField(max_digits=15, decimal_places=2, required=False, allow_null=True)


class LineSerializer(serializers.Serializer):
    DetailType = serializers.CharField(max_length=100,required=True)
    Amount = serializers.DecimalField(max_digits=15, decimal_places=2, required=True)
    SalesItemLineDetail = SalesItemLineDetailSerializer(required=True)


class CustomerRefSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)


class CurrencyRefSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)
    name = serializers.CharField(required=False, max_length=100)

class LinkedTxnSerializer(serializers.Serializer):
    TxnId = serializers.CharField(max_length=50)
    TxnType = serializers.CharField(max_length=50)

class NestedInvoiceSerializer(serializers.Serializer):
    Line = LineSerializer(many=True)
    CustomerRef = CustomerRefSerializer(required=True)
    CurrencyRef = CurrencyRefSerializer(required=True)
    LinkedTxn = serializers.ListField(
        child=LinkedTxnSerializer(),
        required=False
    )

# Employee Serializer

class PrimaryAddSerializer(serializers.Serializer):
    CountrySubDivisionCode = serializers.CharField(max_length=255, required=False)
    City = serializers.CharField(max_length=255, required=False)
    PostalCode = serializers.CharField(max_length=30, required=False)
    Id = serializers.CharField(max_length=30, required=False)
    Line1 = serializers.CharField(max_length=30, required=False)
    Line2 = serializers.CharField(max_length=30, required=False)


class PrimaryPhoneSerializer(serializers.Serializer):
    FreeFormNumber = serializers.CharField(max_length=20, required=False)

class PrimaryEmailAddSerializer(serializers.Serializer):
    Address = serializers.EmailField(required=False, max_length=100)


class EmployeeSerializer(serializers.Serializer):
    GivenName = serializers.CharField(max_length=100, required=False)
    Gender = serializers.CharField(max_length=30, required=False)
    BirthDate = serializers.DateField(required=False, format='%Y-%m-%d')
    PrimaryAddr = PrimaryAddSerializer(required=False)
    PrimaryEmailAddr = PrimaryEmailAddSerializer(required=False)
    PrimaryPhone = PrimaryPhoneSerializer(required=False)
    FamilyName = serializers.CharField(max_length=100, required=False)

    def validate(self, data):
        given_name = data.get('GivenName')
        family_name = data.get('FamilyName')

        if not given_name and not family_name:
            raise serializers.ValidationError("At least one of GivenName or FamilyName must be provided.")
        return data

# Customer

class PrimaryPhoneSerializer(serializers.Serializer):
    FreeFormNumber = serializers.CharField(required=False, max_length=30)


class CustomerSerializer(   serializers.Serializer):
    FullyQualifiedName = serializers.CharField(required=False, max_length=100)
    PrimaryEmailAddr = PrimaryEmailAddSerializer(required=False)
    DisplayName = serializers.CharField(required=False, max_length=100)
    Suffix = serializers.CharField(required=False, max_length=10)
    Title = serializers.CharField(required=False, max_length=10)
    MiddleName = serializers.CharField(required=False, max_length=100)
    Notes = serializers.CharField(required=False)
    FamilyName = serializers.CharField(required=False, max_length=100)
    PrimaryPhone = PrimaryPhoneSerializer(required=False)
    GivenName = serializers.CharField(required=False, max_length=100)

    def validate(self, data):
        display_name = data.get('DisplayName')
        fully_qualified_name = data.get('FullyQualifiedName')
        title = data.get('Title')
        given_name = data.get('GivenName')
        middle_name = data.get('MiddleName')
        family_name = data.get('FamilyName')
        suffix = data.get('Suffix')

        if not display_name and not (title or given_name or fully_qualified_name or middle_name or family_name or suffix):
            raise serializers.ValidationError(
                "DisplayName or at least one of Title, GivenName, FamilyName, Suffix, or FullyQualifiedName must be provided."
            )
        return data

#TimeActivity

class VendorRefSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)
    name = serializers.CharField(required=False, max_length=100)


class EmployeeRefSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)
    name = serializers.CharField(required=False, max_length=100)


class TimeactivitySerializer(serializers.Serializer):
    TxnDate = serializers.DateField(format='%Y-%m-%d', required=False)
    EmployeeRef = EmployeeRefSerializer(required=False)
    CustomerRef = EmployeeRefSerializer(required=False)
    VendorRef = VendorRefSerializer(required=False)
    StartTime = serializers.TimeField(format='%H:%M:%S', required=False)
    EndTime = serializers.TimeField(format='%H:%M:%S', required=False)
    NameOf = serializers.CharField(max_length=50, required=True)
    CostRate = serializers.DecimalField(max_digits=30,decimal_places=2, required=False)
    HourlyRate = serializers.DecimalField(max_digits=12, decimal_places=2,required=False)
    BillableStatus: serializers.CharField(max_length=50, required=False)

    def validate_NameOf(self, value):
        valid_values = ['Vendor', 'Employee']
        if value not in valid_values:
            raise serializers.ValidationError(
                f"Invalid value for NameOf. Must be one of {valid_values}."
            )
        return value

    def validate(self, data):
        name_of = data.get('NameOf')

        if name_of == 'Employee':
            if not data.get('EmployeeRef'):
                raise serializers.ValidationError({
                    'EmployeeRef': 'EmployeeRef is required when NameOf is Employee.'
                })

        elif name_of == 'Vendor':
            if not data.get('VendorRef'):
                raise serializers.ValidationError({
                    'VendorRef': 'VendorRef is required when NameOf is Vendor.'
                })

        return data






