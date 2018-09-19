from django import template
from mainapp.models import Units, Companys
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()
field_names_dict = {'units':list(Units.get_field_names_gen()),
                    'companys':list(Companys.get_field_names_gen())
                    }

@register.simple_tag(name='get_fields_from_row')
def get_fields_from_row(row):
    field_names = field_names_dict[row._meta.model_name]
    result = list()
    for item in field_names:
        try:
            new_item = getattr(row,item)
        except AttributeError:
            new_item = None
        result.append(new_item)
    return result
