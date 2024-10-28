from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View, DetailView
from .models import Profile, StatusMessage, Image  # Ensure you're importing all necessary models
from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})


class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        sm = form.save()  # Save the status message

        # Handle file uploads
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})


from django.urls import reverse
from django.views.generic.edit import UpdateView
from .models import Profile
from .forms import UpdateProfileForm

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})


from django.views.generic.edit import DeleteView

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect to the profile page of the associated profile after deletion
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


from django.views.generic.edit import UpdateView

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']  # Allow updating only the message text
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect to the profile page of the associated profile after update
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        # Get the two profiles based on the URL parameters
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        
        # Add friend relationship
        profile.add_friend(other_profile)
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile.pk)


class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggestions'] = self.object.get_friend_suggestions()
        return context
    

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context