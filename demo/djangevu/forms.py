from copy import deepcopy

from django.http import HttpRequest


class AjaxFormMixin:
    """
    Provide methods allowing data serialization
    into Ajax compatible format which is Json.
    """

    def __init__(self, *args, **kwargs):
        """
        Requires HttpRequest as kwarg.
        """
        self.request = kwargs.pop("request", None) or getattr(self, "request", None)

        if not isinstance(self.request, HttpRequest):
            raise ValueError(
                "%s received %s as request kwarg." % (self.__class__, self.request)
            )

        super().__init__(*args, **kwargs)

    @property
    def sensitive_fields(self) -> list:
        """
        Fields names that are deleted
        from data that client receives
        after ``form.save()`` is called.
        """
        return ["password", "recaptcha", "new_password", "old_password", "token"]

    def get_success_data(self) -> dict:
        """
        Data sent to client after
        ``form.save()`` is called in view.
        example status_code: 200 OK
        """
        r = deepcopy(self.cleaned_data)

        for field in self.sensitive_fields:
            if field in r.keys():
                del r[field]

        return r

    def get_errors_data(self) -> dict:
        """
        Data sent to client after
        ``form.is_valid()`` returns ``False``
        example status_code: 422 Unprocessable Entity
        """
        return self.errors.get_json_data()
