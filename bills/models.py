from django.db import models

class Bill(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    amount_due = models.FloatField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} ({self.account_number})"


