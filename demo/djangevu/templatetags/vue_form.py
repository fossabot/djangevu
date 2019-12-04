import json

from django import template
from django.template import loader
from django.urls import reverse_lazy, resolve

register = template.Library()

default_template = "djangevu/baseform.html"


@register.simple_tag(takes_context=True)
def vue_form(
    context, urlpattern_name, attrs=None, tag_name=None, template_name=default_template
):
    attrs = attrs or {}
    tag_name = tag_name or urlpattern_name

    # cache_key = urlpattern_name+str(attrs)+tag_name+template_name
    # tpl = cache.get(cache_key)
    tpl = None
    if not tpl:
        if attrs:
            attrs = json.loads(attrs)
        action = reverse_lazy(urlpattern_name)
        # assert issubclass(resolve(action).func, View)
        r = context["request"]
        r.path = action
        view = resolve(action).func.view_class(request=r)

        _template = loader.get_template(template_name)
        tpl = _template.render(
            {
                "form": view.get_form(),
                "tag_name": tag_name,
                "attrs": attrs,
                "action": action,
            }
        )
        # cache.set(cache_key, tpl)

    return tpl
