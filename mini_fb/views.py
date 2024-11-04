from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Show all profiles view
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

# Show profile page view, with get_object based on logged-in user
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Return the profile based on the provided primary key
        pk = self.kwargs.get('pk')
        return get_object_or_404(Profile, pk=pk)

# Create profile view, linking profile to logged-in user
class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


    def get_success_url(self):
        # Redirect to the user's profile page
        return reverse('show_profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

# Create status message view, linking message to logged-in user's profile
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        # Get the profile of the logged-in user
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile  # Link status message to profile
        sm = form.save()  # Save status message

        # Handle image uploads, if any
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the profile page
        return reverse('show_profile')

# Update profile view, updating profile of logged-in user
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        # Get the profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        # Redirect to the user's profile page
        return reverse('show_profile')

# Delete status message view
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect to the profile page of the associated profile after deletion
        return reverse('show_profile')

# Update status message view, allowing logged-in user to edit their messages
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    fields = ['message']  # Only the message text is editable
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect to the profile page of the associated profile after update
        return reverse('show_profile')

# Create friend view, allowing logged-in user to add a friend
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Get the profile of the logged-in user
        profile = Profile.objects.get(user=self.request.user)
        # Get the profile to be added as a friend
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        
        # Add friend relationship
        profile.add_friend(other_profile)
        
        return redirect('show_profile')

# Show friend suggestions view
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        # Get the profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add friend suggestions to the context
        context['suggestions'] = self.object.get_friend_suggestions()
        return context

# Show news feed view
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        # Get the profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add news feed data to the context
        context['news_feed'] = self.object.get_news_feed()
        return context
