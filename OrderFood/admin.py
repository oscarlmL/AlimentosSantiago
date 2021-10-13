from django.contrib import admin
from .models import *

# Register your models here.
class AdminNCconvenio(admin.ModelAdmin):
    list_display = ['nom_enc_conv','rut_enc_conv']


class AdminNCempresa(admin.ModelAdmin):
    list_display = ['rut_emp','nom_emp', 'nom_gerente', 'cant_trabajadores','enc_convenio_id_enc_conv']

admin.site.register(Empresa,AdminNCempresa)
admin.site.register(EncConvenio,AdminNCconvenio)

