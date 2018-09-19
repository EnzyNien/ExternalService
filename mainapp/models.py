from django.db import models
from django.core.validators import RegexValidator

###BASE CLASS
class GetTypeChoices():

    @property
    def get_type_choices_str(self):
        result = list(filter(lambda x: x[0] == self.typeof, self.type_choices))
        if result:
            return result[0][1]
        else:
            return ''

    @classmethod
    def get_type_choices(cls):
        return cls.type_choices

    @classmethod
    def get_field_names_gen(cls):
        return filter(lambda x: x != 'id',[item.name for item in cls._meta.get_fields()])

class Classifier(models.Model,GetTypeChoices):

    type_choices = (
        (0, 'zipcode'),
        (1, 'region'),
        (2, 'city'),
        (3, 'street'),
        (4, 'suite'),)

    name = models.CharField(
        verbose_name = 'name', 
        max_length=150, 
        blank=False,
        null=False)

    typeof = models.PositiveIntegerField(
        verbose_name = 'address type',
        choices=type_choices,
        blank=True,
        null=True)

    def __str__(self):
        return self.get_type_choices_str + ' - ' + self.name

    class Meta:
        ordering = ['typeof']
        verbose_name = 'Address Classifier'
        verbose_name_plural = 'Addresses Classifiers'

class Address(models.Model):

    zipcode = models.ForeignKey(
        Classifier,
        on_delete=models.SET_NULL,
        related_name="zipcode_set",
        blank=True,
        null=True)
    region = models.ForeignKey(
        Classifier,
        on_delete=models.SET_NULL,
        related_name="region_set",
        blank=True,
        null=True)
    city = models.ForeignKey(
        Classifier,
        on_delete=models.SET_NULL,
        related_name="city_set",
        blank=True,
        null=True)
    street = models.ForeignKey(
        Classifier,
        on_delete=models.SET_NULL,
        related_name="street_set",
        blank=True,
        null=True)
    suite = models.ForeignKey(
        Classifier,
        on_delete=models.SET_NULL,
        related_name="suite_set",
        blank=True,
        null=True)

    lat = models.DecimalField(
        verbose_name = 'latitude',
        max_digits=10, 
        decimal_places=4,
        blank=True,
        null=True)

    lng = models.DecimalField(
        verbose_name = 'longitude',
        max_digits=10, 
        decimal_places=4,
        blank=True,
        null=True)

    full_name = models.CharField(
        verbose_name = 'full_name',
        max_length=250, 
        blank=True,
        null=False)

    def save(self, *args, **kwargs):
        self.full_name=self.__str__()
        super(Address, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Address item'
        verbose_name_plural = 'Addresses items'

    def __str__(self):
        field_list = [self.zipcode,self.region,self.city,self.street,self.suite]
        field_list = [i.name if i is not None else '' for i in field_list]
        return ' '.join(field_list)

class Companys(models.Model, GetTypeChoices):

    name = models.CharField(
        verbose_name = 'Company',
        max_length=100, 
        blank=False,
        null=False)

    address = models.ForeignKey(
        Address,
        related_name="CompanyAdress",
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    on_load = models.BooleanField(
        verbose_name = 'load form json',
        default = False,
        blank=True,
        null=False)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companys'

    def __str__(self):
        return self.name


class Units(models.Model, GetTypeChoices):

    name = models.CharField(
        verbose_name = 'Name', 
        max_length=100, 
        blank=False,
        null=False)
    username = models.CharField(
        verbose_name = 'Username', 
        max_length=100, 
        blank=False,
        null=False)
    email = models.EmailField(
        verbose_name = 'Email', 
        blank=True,
        null=True)
    phone = models.CharField(
        verbose_name = 'Phone', 
        max_length=30, 
        blank=True,
        null=True)
    website = models.URLField(
        verbose_name = 'Website', 
        blank=True,
        null=True)
    company = models.ForeignKey(
        Companys,
        related_name='+',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    address = models.ForeignKey(
        Address,
        related_name='+',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    on_load = models.BooleanField(
        verbose_name = 'load form json',
        default = False,
        blank=True,
        null=False)
    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __str__(self):
        return self.name
