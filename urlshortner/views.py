from django.shortcuts import render
from . import models
from . import forms
from datetime import datetime
import random, string

# Create your views here.
def home(request):
    return render(request, 'home.html')

def createShortURL(request):
    if request.method == 'POST':
        form = forms.CreateNewShortURL(request.POST)
        if form.is_valid():
            original_website = form.cleaned_data['original_url']
            random_chars_list = list(string.ascii_letters)
            random_chars = ''
            for i in range(6):
                random_chars += random.choice(random_chars_list)
            while len(models.ShortURL.objects.filter(short_url = random_chars)) != 0:
                for i in range(6):
                    random_chars += random.choice(random_chars_list)
            d = datetime.now()
            s = models.ShortURL(original_url=original_website, short_url=random_chars, time_date_created = d)
            s.save()
            return render(request, 'urlcreated.html', {'chars':random_chars})
    else:
        form = forms.CreateNewShortURL()
        context = {'form': form}
        return render(request, 'create.html', context)

def redirect(request, url):
    current_obj = models.ShortURL.objects.filter(short_url = url)
    if len(current_obj) == 0:
        return render(request, 'pagenotfound.html')
    context = {'obj':current_obj[0]}
    return render(request, 'redirect.html', context)