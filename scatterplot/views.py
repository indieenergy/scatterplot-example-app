import base64
import calendar
import datetime
import geopod
import hashlib
import hmac
import time

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from dateutil import parser

from scatterplot.models import Geopod

def home(request):
    data_str = request.GET.get('data', '')
    
    signature = base64.urlsafe_b64decode(request.GET.get('sig', '').encode("ascii"))
    signature_check = hmac.new(settings.GEOPOD_CONSUMER_SECRET.encode("ascii"), msg=data_str.encode("ascii"), digestmod=hashlib.sha256).digest()
    
    if signature != signature_check:
        return HttpResponseForbidden()
    
    if data_str:
        data = simplejson.loads(base64.urlsafe_b64decode(data_str.encode("ascii")))
        subdomain = data.get('subdomain', '')
        if subdomain:
            gp = get_object_or_404(Geopod, subdomain=subdomain)
            gc = geopod.GeopodClient(gp.subdomain, gp.access_token, gp.access_token_secret, settings.GEOPOD_CONSUMER_KEY, settings.GEOPOD_CONSUMER_SECRET, host=settings.API_HOST)
            points = gc.request('/point/', params={'markers[]': 'his'})
    
    now = datetime.datetime.now()
    start = request.GET.get('start', str(datetime.date(year=now.year, month=now.month, day=now.day)))
    end = request.GET.get('end', str(datetime.date(year=now.year, month=now.month, day=now.day)))
    
    context = {
        'geopod': gp,
        'points': points,
        'start': start,
        'end': end,
    }
    return render_to_response('scatterplot.html', context, context_instance=RequestContext(request))


def data(request):
    now = datetime.datetime.now()
    x_axis = request.GET.get('x_axis')
    y_axis = request.GET.get('y_axis')
    print x_axis
    print y_axis
    start = request.GET.get('start', str(datetime.date(year=now.year, month=now.month, day=now.day)))
    end = request.GET.get('end', str(datetime.date(year=now.year, month=now.month, day=now.day)))
    
    start_date = parser.parse(start)
    end_date = parser.parse(end)
    
    subdomain = request.GET.get('subdomain', '')
    if not subdomain:
        return HttpResponseBadRequest()
    
    gp = get_object_or_404(Geopod, subdomain=subdomain)
    gc = geopod.GeopodClient(gp.subdomain, gp.access_token, gp.access_token_secret, settings.GEOPOD_CONSUMER_KEY, settings.GEOPOD_CONSUMER_SECRET, host=settings.API_HOST)
    
    data_series = []
    points = []
    

    x_points = gc.request('/history/%s/%s/%s/' % (x_axis, start, end))
    y_points = gc.request('/history/%s/%s/%s/' % (y_axis, start, end))
        
    print 'x-> %s' % (x_points.get('name', '???'))
    print 'y-> %s' % (y_points.get('name', '???'))

    x_axis = [x[1] for x in x_points.get('data')]
    y_axis = [x[1] for x in y_points.get('data')]

    scatter = zip(x_axis, y_axis)

    data_series.append({
        'name': 'Scatter Plot',
        'unit': '',
        'data': scatter,
        'point_id': 'foo',
    })
        
    graph_data = {
        'start_date': start,
        'end_date': end,
        'utc_offset':  (time.mktime(start_date.timetuple()) - calendar.timegm(start_date.timetuple()))*1000,
        'series': data_series,
    }
    return HttpResponse(simplejson.dumps(graph_data), mimetype="text/javascript")


@csrf_exempt
def auth(request):
    response = None
    
    if request.method == 'POST':
        subdomain = request.POST.get('subdomain', '')
        if subdomain:
            gp, created = Geopod.objects.get_or_create(subdomain=request.POST.get('subdomain'))
            gp.name = request.POST.get('name', '')
            gp.access_token = request.POST.get('access_token', '')
            gp.access_token_secret = request.POST.get('access_token_secret', '')
            gp.save()
            response = HttpResponse()
        else:
            response = HttpResponseBadRequest()
    else:
        response = HttpResponseNotAllowed(['POST',])
    
    return response