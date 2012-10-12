from django.core.context_processors import csrf
from django.shortcuts import render_to_response


def render_to_res_csrf(template, request, context):
    # context.update(csrf(request))
    return render_to_response(template, context)
