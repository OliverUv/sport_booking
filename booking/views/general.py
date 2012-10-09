from django.shortcuts import redirect
from django.contrib.auth import logout as do_logout
from django.template import Context
from booking.common import render_to_res_csrf


def start(request):
    context = Context({'logged_in': request.user.is_authenticated()})
    return render_to_res_csrf('start.html', request, context)


def logout(request):
    do_logout(request)
    return redirect('start')
