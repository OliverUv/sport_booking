from django.shortcuts import redirect, render_to_response
from django.contrib.auth import logout as do_logout
from django.template import RequestContext
from django.utils import translation


def start(request):
    context = RequestContext(request, {
        'logged_in': request.user.is_authenticated(),
        'current_language': translation.get_language(),
        'welc': translation.ugettext('Welcome')})
    return render_to_response('start.html', context)


def logout(request):
    do_logout(request)
    return redirect('start')
