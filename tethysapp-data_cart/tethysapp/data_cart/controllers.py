from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from tethys_gizmos.gizmo_options import TextInput
import requests
import utilities
import os

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    added = False
    waterml_url = ''

    # action if a new URL was added....

    zip_info = utilities.list_zip_files(request)
    print zip_info
    workspace = utilities.get_workspace()
    context = {'file_info': zip_info, 'workspace': workspace}
    return render(request, 'data_cart/home.html', context)


def showfile(request, id):
    """
    Controller for the app home page.
    """
    base_path = utilities.get_workspace()
    file_path = os.path.join(base_path, id)
    response = HttpResponse(FileWrapper(open(file_path)), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="' + id + '"'
    return response

def addfile(request):

    waterml_url = ''
    added = False
    zip_file_id = ''

    # Define Gizmo Options
    text_input_options = TextInput(display_text='Enter WaterML URL',
                                   name='waterml',
                                   attributes='style=width:500px;')

    # Check form data
    if request.POST and 'waterml' in request.POST:
        added = True
        waterml_url = request.POST['waterml']
        zip_info = utilities.make_waterml_zip(waterml_url)
        print zip_info
        zip_file_id = zip_info['site_name']

    # now we download & zip & save the waterml URL
    context = {'waterml-url': waterml_url,
               'added': added,
               'zip_file_id': zip_file_id,
               'text_input_options': text_input_options}

    return render(request, 'data_cart/add.html', context)


# the WaterML URL
def saveWaterML(url):
    r = requests.get(url)
    (site_name, zip_name) = utilities.waterml_site_name(url)

