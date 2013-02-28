# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from lol.models import Snippet, Language
from django.db.models import Avg, Count, Sum
from django.core.exceptions import ValidationError
from lol.forms import UploadForm

def index(request):
    if request.method == 'GET':
        random = Snippet.objects.order_by('?')[0]
        return render_to_response('index.html', {'snippet': random}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        bias = request.POST['submitButton']
        snippet_id = request.POST['snippet_id']
        s = get_object_or_404(Snippet, pk=snippet_id)
        if (bias == 'Leet'):
            s.leet += 1
        elif(bias == 'Lame'):
            s.lame += 1
        s.save()
        return redirect('index')


def upload(request):
    if request.method == 'GET':
        form = UploadForm() 
        return render(request, 'upload.html', {
            'form': form
        })
    elif request.method == 'POST':
        form = UploadForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            desc = form.cleaned_data['description']
            formCode = form.cleaned_data['inputCode']
            lang = form.cleaned_data['language']
            gistId = form.cleaned_data['gist_id']
            if(gistId):
                s = Snippet(code=formCode, description=desc, gist_id=gistId, language=lang)
            else:
                s = Snippet(code=formCode, description=desc, language=lang)
            s.save()
            return redirect('view', snippet_id=s.id)
        else:
            return render(request, 'upload.html', {
                'form': form
            })

def top(request, limit):
    limit = int(limit)
    top = sorted(Snippet.objects.all(), key=lambda a: a.score, reverse=True)[:limit]
    return render_to_response('top.html', {'top': top, 'limit': limit})

def view(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    score = bayesian_average(snippet)
    return render_to_response('view.html', {'snippet': snippet, 'score': score})

def bayesian_average(snippet):
    #http://blog.linkibol.com/2010/05/07/how-to-build-a-popularity-algorithm-you-can-be-proud-of/
    #br = ( (avg_num_votes * avg_rating) + (this_num_votes * this_rating) ) / (avg_num_votes + this_num_votes)
    #1. Someone should check my math; 2. This looks expensive as hell
    sall = Snippet.objects.all()
    avg_rating = sall.aggregate(Avg('leet')).values()[0]
    avg_num_votes = (sall.aggregate(Sum('leet')).values()[0] + sall.aggregate(Sum('lame')).values()[0]) / len(sall)
    this_num_votes = snippet.leet + snippet.lame
    this_rating = snippet.leet
    return 0
    #return ( (avg_num_votes * avg_rating) + (this_num_votes * this_rating) ) / (avg_num_votes + this_num_votes)

