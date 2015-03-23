from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import get_urls
import dev_videos
import models
import datetime
import json
from django.utils import timezone


from django.http import HttpResponse

# Create your views here.
def index(request):
    #dev_videos.get_videos()
    past_24 = get_urls_by_hour(24)
    all_else = get_urls_by_hour(24,True)
    return render(request,"index.html",{"past_24":past_24,"all_else":all_else})

def past_hours(request):
    hours = request.GET.get("hours",24)
    try:
        hours = int(hours)
    except ValueError:
        response_data = {"error": "number of hours must be a number"}
        return HttpResponse(json.dumps(response_data),content_type="application/json",status=400)
    if hours < 0:
        response_data = {"error": "number of hours cannot be negative"}
        return HttpResponse(json.dumps(response_data),content_type="application/json",status=400)
    urls_to_return =  [(url.url, url.true_url) for url in get_urls_by_hour(hours)]
    return  HttpResponse(json.dumps(urls_to_return),content_type="application/json",status=200)

def get_urls_by_hour(hours, negate = False):
    one_day = datetime.datetime.now() - datetime.timedelta(hours=hours)
    one_day =  timezone.make_aware(one_day, timezone.get_default_timezone())
    urls = models.link.objects.order_by("-date_added")
    urls_to_return = []
    for url in urls:
        if not negate:
            if url.date_added >= one_day:
                urls_to_return.append(url)
        else:
            if url.date_added < one_day:
                urls_to_return.append(url)
    return urls_to_return

def update_video_links(request):
    if request.method != "POST":
        return HttpResponse(status=400)
    dev_videos.get_videos()
    return HttpResponse(status=200)

@csrf_exempt
def update_googl(request):
    if request.method != "POST":
        return HttpResponse(status=400)
    get_urls.update()
    return HttpResponse(status=200)
