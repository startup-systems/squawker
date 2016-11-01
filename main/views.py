from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from .models import Squawk


def root(request):
    if (request.method == "POST"):
        inputMessage = request.POST['message']
    if (len(inputMessage) <= 140):
        squawk = Squawk(message=inputMessage)
        squawk.save()
    else:
        return HttpResponseBadRequest("Error: Message Exceeded Max Length of 140")

    squawkers = Squawk.objects.order_by('-created')
    return render(request, "index.html", {"squawks":squawkers})
