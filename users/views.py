from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView


class RegisterView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'users/register.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)