from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth import logout as do_logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django import forms

from booking.models import Resource, UserProfile, User, ResourceType


def build_request_context(request, values):
    if values is None:
        values = {}
    # Add resources that base.html depends on:
    language = get_language()
    resource_types = ResourceType.objects.language(language).all()

    base = {
        'resource_types': resource_types,
        'language': language}
    values['base'] = base
    return RequestContext(request, values)


def http_forbidden_page(request, message):
    if message is None or message == '':
        message = 'Request was made with bad parameters.'
    context = build_request_context(request, {'message': message})
    return render_to_response('403.html', context)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'postal_number', 'phone_number')


class BanUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_banned', 'ban_reason')


@login_required
def profile(request, username):
    if request.user.username != username:
        return http_forbidden_page(request, _('You can only view your own profile page.'))
    if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
    else:
        form = UserProfileForm(instance=request.user.profile)

    context = build_request_context(request, {'form': form})
    return render_to_response('profile.html', context)


@login_required
def ban(request, username):
    if not request.user.is_staff:
        return http_forbidden_page(request, _('You have to be staff to ban people!'))
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
            form = BanUserForm(request.POST, instance=user.profile)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
    else:
        form = BanUserForm(instance=user.profile)

    context = build_request_context(request, {'form': form})
    return render_to_response('ban.html', context)


def start(request):
    language = translation.get_language()
    resources = Resource.objects.language(language).all()
    context = build_request_context(request, {
        'resources': resources})
    return render_to_response('start.html', context)


def logout(request):
    do_logout(request)
    return redirect('start')
