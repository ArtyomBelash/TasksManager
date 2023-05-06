from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.contrib import messages

from .forms import ProfileUpdateForm, UserUpdateForm, TaskCreateAndUpdateForm
from .models import Tasks, Profile
from django.contrib.auth.models import User


class ShowTasks(ListView):
    context_object_name = 'tasks'
    template_name = 'tasks/index.html'
    model = Tasks

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(user=self.request.user, finished=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['history_of_tasks'] = Tasks.objects.filter(user=self.request.user, finished=True)
            return context


class AddTask(CreateView):
    model = Tasks
    template_name = 'tasks/addtask.html'
    # fields = ['title', 'description', 'date']
    success_url = ''
    form_class = TaskCreateAndUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailTask(DetailView):
    model = Tasks
    template_name = 'tasks/task.html'
    pk_url_kwarg = 'tasks_id'
    context_object_name = 'task'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['tasks_id'])


class UpdateTasks(SuccessMessageMixin, UpdateView):
    model = Tasks
    template_name = 'tasks/update_tasks.html'
    success_url = reverse_lazy('showtasks')
    fields = ['title', 'description', 'date', 'finished']
    # form_class = TaskCreateAndUpdateForm
    pk_url_kwarg = 'tasks_id'
    context_object_name = 'task'
    success_message = 'Ваша задача обновлена!'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['tasks_id'])

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteTask(SuccessMessageMixin, DeleteView):
    model = Tasks
    success_url = reverse_lazy('showtasks')
    pk_url_kwarg = 'tasks_id'
    template_name = 'tasks/confirm_delete.html'
    success_message = 'Ваша задача успешно удалена!'

    def get_object(self, queryset=None):
        return super().get_object(queryset=queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_id'] = self.kwargs['tasks_id']
        return context


class MyProfile(DetailView, UpdateView):
    model = Profile
    template_name = 'profile/profile.html'
    context_object_name = 'profile'
    fields = ['image', ]
    # form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile')
    http_method_names = ['post', 'get', ]
    slug_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            slug = self.request.user.profile.slug
            return super().get_queryset().filter(slug=slug)
        return super().get_queryset().none()
        # return super().get_queryset().filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = self.get_queryset()[0].friends.all()
        context['tasks'] = Tasks.objects.filter(user=self.request.user, finished=False)
        context['u_form'] = UserUpdateForm()
        context['p_form'] = ProfileUpdateForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated')
                return redirect('profile', self.get_queryset()[0].slug)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        cont = {
            'u_form': u_form,
            'p_form': p_form,
        }
        return render(request, 'profile/profile.html', cont)


class ShowProfile(DetailView):
    model = Profile
    template_name = 'profile/show_profile.html'
    context_object_name = 'profile'

    def get_queryset(self):
        return super().get_queryset().filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['friend'] = self.request.user.profile.friends.all()
            print(context['friend'])
        return context


class AddFriend(UpdateView):
    model = Profile
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        prof = get_object_or_404(Profile, slug=self.kwargs['slug'])
        user.profile.friends.add(prof.user)
        prof.added_by = user
        prof.save()
        messages.success(request, f'Вы подписались на {prof.user.username} ')
        return redirect('show_profile', slug=prof.slug)


class RemoveFriend(UpdateView):
    model = Profile
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        prof = get_object_or_404(Profile, slug=self.kwargs['slug'])
        user.profile.friends.remove(prof.user)
        prof.added_by = None
        prof.save()
        messages.success(request, f'Вы отписались от {prof.user.username} ')
        return redirect('show_profile', slug=prof.slug)


class NewFollowers(ListView):
    model = Profile
    template_name = 'tasks/new_followers.html'
    context_object_name = 'new_followers'

    def get_queryset(self):
        return super().get_queryset().filter(slug=self.kwargs['slug'])[0].added_by


def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        profiles = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
        return render(request, 'profile/find_profile.html', context={'profiles': profiles})


def search_task(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_task')
        if search_query and request.user.is_authenticated:
            tasks = Tasks.objects.filter(title__icontains=search_query, user=request.user.id)
            return render(request, 'tasks/find_task.html', context={'tasks': tasks})
    return render(request, 'tasks/find_task.html')
