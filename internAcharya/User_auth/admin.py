from django.contrib import admin

# Register your models here. 
from .models import custom_user, user_profile, Application 


class custom_userAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')  # Fields to display
    search_fields = ('username', 'email')  # Enable search by username and email
    list_filter = ('is_active',)  # Filter users by active status
    ordering = ('date_joined',)  # Order by newest users first

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'internship_role', 'status', 'applied_on', 'user')  # Show user
    list_filter = ('status', 'internship_role')
    search_fields = ('full_name', 'internship_role', 'email')
    ordering = ('-applied_on',)
    list_editable = ('status',)

    def save_model(self, request, obj, form, change):
        """Override save_model to ensure updates reflect in the profile."""
        if change:  # If the application is being updated
            obj.save()
        else:
            obj.user = request.user  # Ensure user is linked on application creation
            obj.save()

# Register models
admin.site.register(custom_user, custom_userAdmin)
admin.site.register(user_profile)
admin.site.register(Application, ApplicationAdmin)

from .models import InternshipList

# @admin.register(InternshipList)
# class InternshipListAdmin(admin.ModelAdmin):
#     list_display = ('internship_role', 'company_name', 'location', 'working_hours', 'created_at')
#     

# from .models import InternshipList

class InternshipListAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'location', 'work_hours', 'created_at')  # 👈 match model field names
    search_fields = ('internship_role', 'company_name', 'location')
admin.site.register(InternshipList, InternshipListAdmin)