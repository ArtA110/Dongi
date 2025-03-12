from rest_framework import serializers
from expense.models import Expense, ExpenseShare, Payment
from user.serializers import GroupSerializer, UserSerializer

class ExpenseSerializer(serializers.ModelSerializer):
    group = GroupSerializer(context={'limited': True})
    class Meta:
        model = Expense
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'group', 'amount', 'bought_at']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)

class ExpenseShareSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer(context={'limited': True})
    user = UserSerializer(context={'limited': True})
    class Meta:
        model = ExpenseShare
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'expense', 'user', 'amount']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)

class PaymentSerializer(serializers.ModelSerializer):
    payer = UserSerializer(context={'limited': True})
    payee = UserSerializer(context={'limited': True})
    expense = ExpenseSerializer(context={'limited': True})
    class Meta:
        model = Payment
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'payer', 'payee', 'expense', 'amount', 'paid_at']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)


class ExpenseSplitSerializer(serializers.Serializer):
    split_type = serializers.ChoiceField(choices=['equally', 'percentage', 'custom'])
    data = serializers.JSONField()
    
    def validate(self, data):
        if data['split_type'] == 'equally':
            if data['data']:
                raise serializers.ValidationError("data should be empty for equally split")
        elif data['split_type'] == 'percentage':
            if sum(data['data'].values()) != 100:
                raise serializers.ValidationError("percentages should sum up to 100")
        return data
