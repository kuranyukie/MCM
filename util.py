# -*- coding: utf-8 -*-  
import re, socket, urllib2, json, random, sys, os
from multiprocessing import Process, Lock
from time import sleep, time, mktime, ctime, localtime
from datetime import datetime, date, timedelta
from os.path import exists, getsize, join, isfile
from os import rename, listdir, remove
from sys import stdin, stdout, stderr, exit
from math import *
from copy import *

def request(url, getData = None, postData = None, timeout = None) :
    num_timeout, num_unknown, num_other = 0, 0, 0
    try :
        if getData != None :
            url += '?' + '&'.join(['%s=%s' % (str(key), str(value)) for key, value in getData.items()])
        data = None
        if postData != None :
            data = str(postData)
        request = urllib2.Request(url, data = data)
        response = urllib2.urlopen(request, timeout = timeout)
        content = response.read()
    except urllib2.HTTPError, e:
        # TODO
        return {'e' : 'HTTPError', 'content' : e.read()}
    except urllib2.URLError, e :
        if isinstance(e.reason, socket.timeout) :
            return {'e' : 'TIMEOUT', 'content' : None}
        else :
            print '[Other Exception]', e
            return {'e' : 'OTHER', 'content' : None}
    except socket.timeout :
        return {'e' : 'TIMEOUT', 'content' : None}
    except KeyboardInterrupt, e :
        raise
    except Exception, e:
        print '[Unknown Exception]', e
        return {'e' : 'UNKNOWN', 'content' : None}
    else :
        return {'e' : None, 'content' : content}

def decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv

def decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        rv[key] = value
    return rv

def anti_serialize(data, seperator, mapper, caster_value = None, caster_key = None) :
    if type(data) == str :
        return dict([(
            field.split(mapper)[0] if caster_key   is None else caster_key(field.split(mapper)[0]),
            field.split(mapper)[1] if caster_value is None else caster_value(field.split(mapper)[1])
            ) for field in data.split(seperator)])
    if type(data) == dict :
        return dict([(key, anti_serialize(value, seperator, mapper, caster_value, caster_key)) for (key, value) in data.items()])
    if type(data) == list :
        return [anti_serialize(datum, seperator, mapper, caster_value, caster_key) for datum in data]

def j(data, indent = 4, ensure_ascii = False, sort_keys = True, encoding = 'utf-8') :
    return json.dumps(data, indent = indent, ensure_ascii = ensure_ascii, sort_keys = sort_keys, encoding = encoding)

def c(*dicts) :
    _ = {}
    for __ in dicts : _.update(__)
    return _

def load_txt(fin, fields = None, key = None) :
    if fields == None :
        fields = fin.readline().strip().split('\t')
    mapping = dict([(_, fields[_]) for _ in range(len(fields))])
    
    lines = fin.readlines()
    if len(lines) == 0 :
        return []
    if lines[-1] == '' :
        lines = lines[:-1]

    records = [line.strip('\n').split('\t') for line in lines]
    _ = [dict([(mapping[_], record[_]) for _ in range(len(record))]) for record in records]
    if key is not None :
        data = {datum[key] : datum for datum in _}
    else : 
        data = _
    return data

def load_json(fin, object_hook = None) :
    return json.loads(''.join([line.strip('\n') for line in fin.readlines()]), object_hook = object_hook)

def upper_first(st) :
    if st == '' : return st
    else : return st[0].upper() + st[1:]

def get_date_str(timestamp = None) :
    if timestamp is None : timestamp = time()
    return str(datetime.fromtimestamp(timestamp))[:10].replace('-', '.').replace('T', '.').replace(':', '.')

def split_filename(filename) :
    if '.' in filename :
        return re.findall('(.*)\.([^\.]+)', filename)[0]
    else : return (filename, '')

def add_suffix(filename, suffix) :
    _ = split_filename(filename)
    return _[0] + suffix + ('' if _[1] == '' else '.') + _[1]

def check_criterion(data, criterion = None) :
    if criterion is None : return True
    for key, value in criterion.items() :
        if data.get(key) is None : return False
        if type(value) == dict :
            if not check_criterion(data[key], value) : return False
        else :
            # TODO
            if data[key] != value : return False
    return True

def perform_projection(data, projection = None) :
    if projection is None : return data
    res = {}
    for key, value in projection.items() :
        if data.get(key) is None : continue
        if value == True : res[key] = data[key]
        else :
            if type(value) == dict :
                res[key] = perform_projection(data[key], value)
            else : raise BaseException('Unknown projection : ' + str(value))
    return res

def find(data, criterion = None, projection = None) :
    if not check_criterion(data, criterion) : return False
    else : return perform_projection(data, projection)
