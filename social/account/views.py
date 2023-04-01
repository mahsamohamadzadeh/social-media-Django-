from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistratonForm, UserLoginForm, EditUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation


# Create your views here.

class UserRegisterView(View):
    form_class = UserRegistratonForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post:posts')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        user = User.objects.all()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], password=cd['password1'], email=cd['email'])
            messages.success(request, 'you registerd successfully', 'success')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post:posts')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('post:posts')
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    # login_url = 'account/login/'

    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('post:posts')


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        # posts = Post.objects.filter(user=user)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'account/profile.html', {'user': user, 'posts': posts, 'is_following': is_following})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password-reset-done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password-reset-complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'you are already following this user', 'danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, 'you followed this user', 'success')
        return redirect('account:user-profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('account:user-profile', user.id)


class UserEditView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        return render(request, 'account/edit_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'profile edited successfully', 'success')
        return redirect('account:user-profile', request.user.id)
