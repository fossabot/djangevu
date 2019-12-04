from djangevu.views import AjaxFormView
from .forms import NameForm

class BaseView(AjaxFormView):
    form_class = NameForm
    url_name = 'basic-form'
