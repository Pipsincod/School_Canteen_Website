from django.contrib import admin

from first_app.models import CommentHistory, ExpHistory

class MyComments(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'create_at')

class MyExp(admin.ModelAdmin):
    list_display = ('id', 'author', 'res', 'solution', 'create_at')

admin.site.register(CommentHistory, MyComments)
admin.site.register(ExpHistory, MyExp)
