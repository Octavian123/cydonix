from django.contrib import admin

from .models import Sensors, SensorData, PermissionType, Permission



class SensorDataAdmin(admin.ModelAdmin):
    fieldsets = [('Sensor', {'fields':['sensor']}),
		 ('Value' , {'fields':['value']}),
		]
    list_display=('sensor', 'value', 'timestamp') 
    list_filter=['timestamp']
    search_fields = ['sensor__sensor_type']


class PermissionAdmin(admin.ModelAdmin):
    fieldsets = [('User', {'fields':['user']}),
		 ('type', {'fields':['type']}),
		 ('sensor',{'fields':['sensor']})
		]
    list_display=('user', 'sensor', 'type')
    search_fields = ['user__username']

admin.site.register(Sensors)
admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(Permission, PermissionAdmin)
