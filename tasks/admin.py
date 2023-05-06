from django.contrib import admin
from .models import Tasks, Profile


class TasksAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'date', 'finished', 'user']
    list_editable = ['finished', ]


# class ProfileAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': (Profile.user.username,)}

# class ProfileAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('user',)}

    # def save_model(self, request, obj, form, change):
    #     obj.slug = obj.user.username
    #     super().save_model(request, obj, form, change)


admin.site.register(Tasks, TasksAdmin)
admin.site.register(Profile)
