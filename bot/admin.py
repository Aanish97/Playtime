from django.contrib import admin

from bot.models import User, ChatMessage


model_admin = admin.ModelAdmin


@admin.register(User)
class UserAdmin(model_admin):
    list_display = ['username', 'facebook_id', 'first_name', 'last_name', 'date_joined']
    list_display_links = ('username', 'facebook_id')
    readonly_fields = ('facebook_id', 'first_name', 'last_name')


@admin.register(ChatMessage)
class ChatMessageAdmin(model_admin):
    list_display = ['get_time', 'get_name', 'message', 'bot_message']
    readonly_fields = ('get_name', 'message', 'bot_message')

    def get_name(self, obj):
        return obj.user.get_full_name()

    def get_time(self, obj):
        return f"{obj.updated.date()}, {obj.updated.time()}"

    get_name.short_description = 'Name'
    get_time.short_description = 'Time'

