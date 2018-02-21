from django.contrib import admin
from Liga import models
from django import forms


class AdicionalStacked(admin.StackedInline):
    model = models.Adicional

class AdicionalAdminForm(forms.ModelForm):
    def clean_nombre(self):
        if len(self.cleaned_data['nombre'])<3:
            raise forms.ValidationError("El nombre es muy corto")
        else:
            return self.cleaned_data['nombre']

    def clean_numero_cuenta(self):
        if self.cleaned_data['numero_cuenta'][0:2]!="ES":
            raise forms.ValidationError("El numero de cuenta debe empezar por ES")
        elif self.cleaned_data['numero_cuenta'][2:10].isdigit()==False:
            raise forms.ValidationError("El numero de cuenta debe empezar por ES, seguido de 8 numeros")
        elif len(self.cleaned_data['numero_cuenta'])<10:
            raise forms.ValidationError("La longitud del numero de cuentas es de 8 Digitos")
        return self.cleaned_data['numero_cuenta']

class AdicionalAdmin(admin.ModelAdmin):
    raw_id_fields = ("skin",)
    form = AdicionalAdminForm


class SkinAdmin(admin.ModelAdmin):
    list_filter = ['coleccion']
    ordering = ["tipo"]
    list_per_page = 1
    inlines = [AdicionalStacked, ]
    search_fields = ['nombre']

admin.site.register(models.Skin, SkinAdmin)
admin.site.register(models.Adicional, AdicionalAdmin)
admin.site.register(models.Liga)
admin.site.register(models.Inscriben)
# Register your models here.
