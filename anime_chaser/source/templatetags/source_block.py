from django import template

from source.forms import SourceForm
from source.models import Source

register = template.Library()


@register.inclusion_tag('source/block.html')
def source_block(target):
    return {
        'target': target,
        'source_form':  SourceForm(),
        'source_list': Source.get_by_target(target)
    }
