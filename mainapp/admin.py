from django.forms import ModelForm
from django.contrib import admin
from mainapp.models import Units, Companys, Classifier, Address

class UnitsAdmin(admin.ModelAdmin):
    readonly_fields = ('on_load',)

class CompanysAdmin(admin.ModelAdmin):
    readonly_fields = ('on_load',)

class AddressAdminForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('full_name',)

    def __init__(self, *args, **kwargs):
        super(AddressAdminForm, self).__init__(*args, **kwargs)
        tup = Classifier.type_choices
        for key, _ in self.fields.items():
            result = list(filter(lambda x: x[1]==key, tup))
            if result:
                self.fields[key].queryset = Classifier.objects.filter(typeof=result[0][0])
        #self.fields['zipcode'].queryset = Classifier.objects.filter(typeof=0)
        #self.fields['region'].queryset = Classifier.objects.filter(typeof=1)
        #self.fields['city'].queryset = Classifier.objects.filter(typeof=2)
        #self.fields['street'].queryset = Classifier.objects.filter(typeof=3)
        #self.fields['suite'].queryset = Classifier.objects.filter(typeof=4)

class AddressAdmin(admin.ModelAdmin):
    form = AddressAdminForm

class ClassifierAdmin(admin.ModelAdmin):
    list_filter = ('typeof',)


admin.site.register(Units, UnitsAdmin)
admin.site.register(Companys, CompanysAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Classifier, ClassifierAdmin)