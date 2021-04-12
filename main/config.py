def CustomContext(request):
    context = {
        'host' : request.META['HTTP_HOST']
    }

    return context