from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import SourceForm


class SourceView(TemplateView):
    http_method_names = ['post']
    template_name = 'source/result.html'

    def post(self, request, *args, **kwargs):
        source_form = SourceForm(request.POST)
        target = request.POST.get('target')

        if source_form.is_valid():
            instance = source_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': source_form,
            'target': target
        }

        return self.render_to_response(context)
