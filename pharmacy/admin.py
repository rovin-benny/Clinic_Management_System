from django.contrib import admin
from .models import Medicine, PharmacyBill, PharmacyBillItem

# Register your models here.
admin.site.register(Medicine)
admin.site.register(PharmacyBill)
admin.site.register(PharmacyBillItem)