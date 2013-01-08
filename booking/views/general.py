from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import logout as do_logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils import translation
from django.utils.translation import ugettext as _
from django import forms

from booking.models import Resource
from booking.validators import validate_postalnumber
from booking.common import http_forbidden_page


class UserProfileForm(forms.Form):
    full_name = forms.CharField(max_length=200, label=_('Your full name'))
    postal_number = forms.IntegerField(label=_('Your postal number (nnnnn)'),
            validators=[validate_postalnumber])
    phone_number = forms.CharField(max_length=40)


@login_required
def profile(request, username):
    if request.user.username != username:
        return http_forbidden_page(request, _('You can only view your own profile page.'))
    if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                profile = request.user.profile
                profile.full_name = form.cleaned_data['full_name']
                profile.postal_number = form.cleaned_data['postal_number']
                profile.phone_number = form.cleaned_data['phone_number']
                profile.save()
                return HttpResponseRedirect('/')
    else:
        form = UserProfileForm()
        profile = request.user.profile

    context = RequestContext(request, {'form': form})
    return render_to_response('profile.html', context)


def start(request):
    language = translation.get_language()
    resources = Resource.objects.language(language).all()
    context = RequestContext(request, {
        'resources': resources,
        'logged_in': request.user.is_authenticated(),
        'current_language': language,
        'welc': _('Welcome')})
    return render_to_response('start.html', context)


def logout(request):
    do_logout(request)
    return redirect('start')
