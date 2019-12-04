from typing import Type

from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.views.generic.edit import BaseFormView

from djangevu.forms import AjaxFormMixin


class AjaxFormView(BaseFormView):
    form_class: Type[AjaxFormMixin] = None
    url_name: str = None

    @classmethod
    def get_django_urlpattern(cls, url_path=None, **initkwargs) -> path:
        """
        Return django ``path`` for urlpatterns for this view.
        """
        if not cls.url_name:
            raise ValueError("Url name for view %s is not set" % cls.__name__)
        d = dict(view=cls.as_view(**initkwargs), name=cls.url_name)
        return path(url_path or d["name"], **d)

    @property
    def is_autocomplete(self) -> bool:
        return "Auto-Complete" in self.request.headers.keys()

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return HttpResponse(status=405)

    def get_form_kwargs(self) -> dict:
        """
        Avoid adding auto_id (duplicates ids in html).
        Add request because AjaxForm requires it as
        first argument to __init__.
        """
        kwargs = super().get_form_kwargs()
        kwargs["auto_id"] = False
        kwargs["request"] = self.request
        return kwargs

    def form_invalid(self, form):
        """
        Form invalid, return status=422 and errors.
        """
        return JsonResponse(form.get_errors_data(), safe=False, status=422)

    def form_valid(self, form):
        """
        If autocomplete header is present, form won't be saved
        and status=204 is returned. Otherwise save the form
        and return status=200.
        """
        if self.is_autocomplete:
            return HttpResponse(status=204)
        else:
            self.save_form(form)
            return JsonResponse(form.get_success_data(), safe=False, status=200)

    def save_form(self, form):
        form.save()
