# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import boto

import sys
sys.path.append( '..' )
from twittube.models import Sponsor
from conversation.models import Participant

def index(request):
    all_sponsors = Sponsor.objects.all()
    return render(request, 'twittube/index.html', {'all_s':all_sponsors})
    #return HttpResponse("Hello, world. You're at the index.")


class UploadFileForm(forms.Form):
    file  = forms.FileField()

def handlefile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #return HttpResponse(request.FILES['file'].read())
        if form.is_valid():
            s = Sponsor()
            s.save()
            filename = str(s.id)+'_0.mp4'
            s.filename = filename
            s.save()
            originalname = request.FILES['file'].name
            default_storage.save(originalname, request.FILES['file'])
            transcode = boto.elastictranscoder.connect_to_region("us-west-2",aws_access_key_id='AKIAJKADLVELVEBLGGGQ', aws_secret_access_key='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')
	     params_in = { 'Key': originalname, 'FrameRate': 'auto', 'Resolution': 'auto', 'AspectRatio': 'auto', 'Interlaced': 'auto', 'Container': 'auto',}

            params_out =  { 'Key':  filename,
        	'ThumbnailPattern': '',
        	'Rotate':           'auto',
        	'PresetId':         '1351620000001-000061',
    	     }
	     transcode.create_job(pipeline_id='assignment1', input_name=params_in, output=params_out)
            return HttpResponseRedirect(reverse('twittube.views.index'))
        else:
            return HttpResponse("upload form invalid")
    else:
        form = UploadFileForm()
    return HttpResponse("upload failed.")

