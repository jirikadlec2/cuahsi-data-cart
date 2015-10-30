import os
from lxml import etree
from .app import CuahsiDataCartDemo as app
import unidecode
import requests

from datetime import datetime
from datetime import timedelta
from dateutil import parser
import csv
from collections import OrderedDict
import re
from django.http import HttpResponse
import zipfile

from tethys_sdk.gizmos import TimeSeries
import xml.etree.ElementTree as ET
import time


def getHumanReadableSize(filepath,precision=2):
    print 'filepath: ' + filepath
    size = os.path.getsize(filepath)
    print size
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division


    return "%0.2f %s" % (size,suffixes[suffixIndex])


def get_app_base_uri(request):
    base_url = request.build_absolute_uri()
    if "?" in base_url:
        base_url = base_url.split("?")[0]
    return base_url


def list_zip_files(request):
    workspace = get_workspace()
    files = [f for f in os.listdir(workspace) if os.path.isfile(f)]
    file_info = []
    base_uri = get_app_base_uri(request)
    domain = request.META['HTTP_HOST']
    for f in files:
        full_path = os.path.join(workspace, f)
        basename = os.path.basename(f)
        uri = base_uri + 'showfile/' + basename
        app_uri = 'http://' + domain + '/apps/timeseries-viewer/?src=test&res_id=' + basename
        filesize = getHumanReadableSize(full_path)
        file_info.append({'name': basename, 'uri': uri, 'size': filesize, 'app': app_uri})
    return file_info


def get_workspace():
    return app.get_app_workspace().path


def make_waterml_zip(url):
    r = requests.get(url)
    xml = r.content
    root = etree.XML(xml)
    root_tag = root.tag.lower()
    status = ''
    try:
        if 'timeseriesresponse' in root_tag or 'timeseries' in root_tag or "envelope" in root_tag:

            t0 = time.time()

            # metadata items
            units, site_name, variable_name = None, None, None
            unit_is_set = False

            # iterate through xml document and read all values
            for element in root.iter():
                brack_lock = -1
                if '}' in element.tag:
                    brack_lock = element.tag.index('}')  #The namespace in the tag is enclosed in {}.
                    tag = element.tag[brack_lock+1:]     #Takes only actual tag, no namespace

                if 'siteName' == tag:
                    site_name = element.text
                    break

            # constructs the zip file name
            site_name_ascii = unidecode.unidecode(site_name)
            zfname = site_name_ascii.lower().replace(' ', '-') + '.zip'
            xmlname = zfname.replace('.zip','.xml')

            # get workspace
            print 'zfname:' + zfname

            workspace_object = app.get_app_workspace()
            workspace = workspace_object.path
            print 'workspace:' + workspace

            zip_name = os.path.join(workspace, zfname)
            print 'zip_name: ' + zip_name

            zf = zipfile.ZipFile(zip_name, mode='w', compression=zipfile.ZIP_DEFLATED)
            try:
                print 'writing zip file..'
                zf.writestr(xmlname, xml)
            finally:
                zf.close()

            return {'site_name': site_name, 'zip_name': zip_name, 'status': 'ok'}
        else:
            error_message = "Parsing error: The waterml document doesn't appear to be a WaterML 1.0/1.1 time series"
            print error_message
            return {'site_name': '', 'zip_name': '', 'status': 'error'}
    except Exception, e:
        print e
        print "Parsing error: The Data in the Url, or in the request, was not correctly formatted for water ml 1."
        return {'site_name': '', 'zip_name': '', 'status': 'error'}
