from rest_framework import serializers
from expense.models import Expense, ExpenseShare, Payment
from user.serializers import GroupSerializer, UserSerializer
from user.models import Group, User


class ExpenseSerializer(serializers.ModelSerializer):
    group = GroupSerializer(context={'limited': True}, read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,
        source='group'
    )
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'split_data']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'group', 'amount', 'bought_at']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)

class ExpenseShareSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer(context={'limited': True}, read_only=True)
    expense_id = serializers.PrimaryKeyRelatedField(
        queryset=Expense.objects.all(),
        write_only=True,
        source='expense'
    )
    user = UserSerializer(context={'limited': True}, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )
    class Meta:
        model = ExpenseShare
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'expense', 'user', 'amount']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)

    def validate(self, attrs):
        expense = attrs.get('expense')
        if expense:
            group = expense.group
            self.fields['user_id'].queryset = group.users.all()
            if attrs.get('user') not in group.users.all():
                raise serializers.ValidationError("User is not part of the expense")
        return attrs

class PaymentSerializer(serializers.ModelSerializer):
    payer = UserSerializer(context={'limited': True}, read_only=True)
    payee = UserSerializer(context={'limited': True}, read_only=True)
    expense = ExpenseSerializer(context={'limited': True}, read_only=True)
    payer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='payer'
    )
    payee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='payee'
    )
    expense_id = serializers.PrimaryKeyRelatedField(
        queryset=Expense.objects.all(),
        write_only=True,
        source='expense'
    )
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'payer', 'payee', 'expense', 'amount', 'paid_at']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)
    
    def validate(self, attrs):
        expense = attrs.get('expense')
        if expense:
            group = expense.group
            self.fields['payer_id'].queryset = group.users.all()
            self.fields['payee_id'].queryset = group.users.all()
            if attrs.get('payer') not in group.users.all():
                raise serializers.ValidationError("Payer is not part of the expense")
            if attrs.get('payee') not in group.users.all():
                raise serializers.ValidationError("Payee is not part of the expense")
            if attrs.get('payer') == attrs.get('payee'):
                raise serializers.ValidationError("Payer and Payee cannot be the same")
            if attrs.get('amount') <= 0:
                raise serializers.ValidationError("You must pay a positive amount")
        return attrs


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
    
    
class ExpenseSharingSerializer(serializers.Serializer):
    debtor = UserSerializer(read_only=True, context={'limited': True})
    creditor = UserSerializer(read_only=True, context={'limited': True})
    amount = serializers.IntegerField()
