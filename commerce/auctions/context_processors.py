from .models import *

def watchcount_processor(request):
    watchcount =  Watchlist.objects.filter(user=request.user.id).count()
    return {'watchcount': watchcount}

# I asked the CS50 AI for advice on how to pass a variable to all templates (specifically layout) and it share the context processor would be helpful
# Additionally, explained how to include it in the 