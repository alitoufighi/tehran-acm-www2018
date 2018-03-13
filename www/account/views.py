from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, logout, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView
from django.contrib.auth.views import LoginView, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, TemplateView

from account.form import RegisterForm
from account.models import UserProfile, Notification
from account.tokens import account_activation_token
from blog.models import Post, ReportPost


class Register(FormView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.is_active = False
        user.save()

        profile = UserProfile(student_id=form.cleaned_data['student_id'], user=user,
                              field=form.cleaned_data['field'])
        profile.save()
        self.send_activate_mail(user, form)
        messages.success(self.request, _("You registered."))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Invalid register."))
        return super().form_invalid(form)

    def send_activate_mail(self, user, form):
        mail_subject = _('Activate your account')
        context = {
            'user': user,
            'uid': force_text(urlsafe_base64_encode(force_bytes(user.id))),
            'token': str(account_activation_token.make_token(user)),
        }

        url = reverse('account:activate', args=[context['uid'], context['token']])
        # message = render_to_string('account/mails/verification.html', context,
        #                            request=self.request)

        # to_email = form.cleaned_data.get('email')
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()

        send_mail(mail_subject, 'http://localhost:8000' + str(url), 'alirezakhoshghalb@ymail.com', [user.email])

        messages.success(self.request, _('User has been created. check your email for confirmation mail.'))


class Login(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = False
    login_again = False

    def get_redirect_url(self):
        if self.request.user:
            if self.request.user.is_staff:
                return reverse('admin:index')

            return reverse('account:my_profile')

    def form_invalid(self, form):
        for e in form.errors:
            messages.error(self.request, _("Invalid login information."))
            self.login_again = True
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['login_again'] = self.login_again
        self.login_again = False
        return c


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(author=user, anon=False)

    return render(request, 'account/profile.html', {
        'user': user,
        'blog_posts': posts
    })


@login_required
def my_profile(request):
    return redirect('account:profile', user_id=request.user.id)


class Notifications(TemplateView, LoginRequiredMixin):
    template_name = "account/notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['notifications'] = Notification.objects.filter(user=user, seen=False)
        return context


class SeenNotification(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        print(self.kwargs['id'])
        try:
            notif = Notification.objects.get(id=self.kwargs['id'])
            print(notif)
            if notif.user.id == request.user.id:
                notif.seen = True
                notif.save()
        except Exception as e:
            pass
        return HttpResponseRedirect(reverse('account:notifications'))


class ActivateUser(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('account:login'))

        return HttpResponse("ERROR.")


def my_logout(request):
    logout(request)
    return redirect('account:login')


class PasswordReset(PasswordResetView):
    success_url = reverse_lazy('account:reset_done')
    from_email = 'alirezakhoshghalb@ymail.com'

    def dispatch(self, *args, **kwargs):
        if self.request.POST.get('email'):
            exists = True
            try:
                user = User.objects.filter(email=self.request.POST.get('email'))
                exists = user.exists()
            except:
                exists = False
            if not exists:
                messages.error(self.request, 'ایمیل وارد شده در سیستم نیست.')
        return super().dispatch(*args, **kwargs)


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:login')


class PasswordResetDone(PasswordResetDoneView):
    pass


class ChangePermissionList(TemplateView, LoginRequiredMixin):
    template_name = "account/change_roles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['reports'] = ReportPost.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class ChangePermission(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_superuser:
            id = self.kwargs['id']
            action = self.kwargs['action']
            try:
                u = User.objects.get(id=id)
                if action == '1':
                    u.is_staff = not u.is_staff
                elif action == '2':
                    u.is_superuser = not u.is_superuser
                elif action == '3':
                    u.is_active = not u.is_active
                u.save()
            except:
                pass
            return HttpResponseRedirect(reverse('account:change_perm_list'))
