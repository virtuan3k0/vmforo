from django.contrib import admin
from .models import Section, Category, Thread, Post, PrivateMessage

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('section',)

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('thread',)

@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'get_recipients', 'get_content', 'timestamp', 'read')
    readonly_fields = ('get_content',)

    def get_recipients(self, obj):
        return ", ".join([user.username for user in obj.recipients.all()])
    get_recipients.short_description = 'Recipients'

    def get_content(self, obj):
        request = self.request
        if request and request.user.is_superuser:
            try:
                return obj.decrypt()  # Call the decrypt method on the PrivateMessage instance
            except Exception as e:
                return f"Error decrypting message: {e}"
        else:
            return "Content hidden (requires superuser privileges)"

    get_content.short_description = 'Message Content'

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)
