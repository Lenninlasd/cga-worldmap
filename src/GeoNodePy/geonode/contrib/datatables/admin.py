from django.contrib import admin
from geonode.maps.models import LayerAttribute
from .models import DataTable, DataTableAttribute, TableJoin, JoinTarget, JoinTargetFormatType, GeocodeType

class DataTableAdmin(admin.ModelAdmin):
    model = DataTable
    list_display = (
        'id',
        'title',
        'table_name',
        'tablespace')
    list_display_links = ('title',)


class DataTableAttributeAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'attribute_label', 'datatable', 'attribute_type', 'searchable')
    list_filter  = ('datatable', 'searchable', 'attribute_type')


class TableJoinAdmin(admin.ModelAdmin):
    model = TableJoin 


class JoinTargetAdmin(admin.ModelAdmin):
    model = JoinTarget

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'attribute':
            kwargs["queryset"] = LayerAttribute.objects.filter(
                layer=request.GET.get('layer'))
        return super(JoinTargetAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(DataTable, DataTableAdmin)
admin.site.register(DataTableAttribute, DataTableAttributeAdmin)
admin.site.register(TableJoin, TableJoinAdmin)
admin.site.register(JoinTarget, JoinTargetAdmin)
admin.site.register(JoinTargetFormatType)
admin.site.register(GeocodeType)