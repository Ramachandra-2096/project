# your_app/admin.py

from django.contrib import admin
from .models import event_registration, Event, PurchasedTicket,Gallery


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'description', 'price', 'event_photo')

@admin.register(PurchasedTicket)
class PurchasedTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'purchase_date', 'token', 'is_valid')
    list_filter = ('event__event_name', 'is_valid')
    ordering = ('-purchase_date',)
    #list_editable = ('is_valid',)
    actions = ['mark_as_valid', 'mark_as_invalid']

    def mark_as_valid(modeladmin, request, queryset):
        queryset.update(is_valid=True)

    def mark_as_invalid(modeladmin, request, queryset):
        queryset.update(is_valid=False)



@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('year', 'photo')
    
@admin.register(event_registration)
class event_registrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event','usn','payment_photo','payment_status')
    list_filter = ('event__event_name', 'payment_status')
    list_editable = ('payment_status',)
    actions = ['mark_as_valid', 'mark_as_invalid']

    def mark_as_valid(modeladmin, request, queryset):
        queryset.update(payment_status=True)

    def mark_as_invalid(modeladmin, request, queryset):
        queryset.update(payment_status=False)
