from django.contrib import admin

from sales.models import Organization, Product


@admin.action(
    description="Очистить задолженность перед поставщиком у выбранных объектов"
)
def delete_debt(modeladmin, request, queryset):
    queryset.update(debt=0.0)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "provider", "debt")
    list_filter = ("city",)
    actions = [delete_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
