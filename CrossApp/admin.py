from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MyUser,Create_Ad,Comments


# Register your models here.
@admin.register(MyUser)
class User(admin.ModelAdmin):
    list_display = (
        "email",
        'username',
        'is_active'
    )

@admin.register(Create_Ad)
class Ad(admin.ModelAdmin):
    list_display = (
        "titre",
        "price_on_sale",
        "price_for_rent",
        "author",
        "date_created",
    )
@admin.register(Comments)
class Comments(admin.ModelAdmin):
    list_display = (
        "ad_comments",
        "comment",
        "author_comment",
        "date_created",
    )
