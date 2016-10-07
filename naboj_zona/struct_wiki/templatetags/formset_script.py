from django import template

register = template.Library()


def create_formset_id_filter(selector):
    return lambda formset: 'id_%s-%s' % (formset.prefix, selector)

for selector in ['body', 'add_button', 'template']:
    register.filter(
        'formset_%s_id' % selector,
        create_formset_id_filter(selector),
    )


@register.inclusion_tag('struct_wiki/parts/formset_script.html')
def formset_script(formset):
    return {
        'prefix': formset.prefix,
    }
