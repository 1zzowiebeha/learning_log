from django.contrib import admin

from .models import Topic, Entry

# Register your models here.

class EntryAdmin(admin.ModelAdmin):
    def sortable_str(self, obj):
        """Allows us to click the table column heading
        in the admin menu to sort by Entry.__str__().
        We display this function in the item table via list_display."""
        return obj.__str__()

    sortable_str.short_description = 'Entry'
    sortable_str.admin_order_field = 'content'

    list_display = ["sortable_str", "topic", "created_on", "modified_on"]


admin.site.register(Topic)
admin.site.register(Entry, EntryAdmin)