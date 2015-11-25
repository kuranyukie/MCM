# -*- coding: utf-8 -*-  
from util import *

class curler :

    url = {
        'situation_summary' : 'http://apps.who.int/gho/athena/xmart/data.xls?target=EBOLA_MEASURE/CASES,DEATHS&format=xml&profile=excel&filter=COUNTRY:GIN;COUNTRY:UNSPECIFIED;COUNTRY:LBR;COUNTRY:UNSPECIFIED;COUNTRY:SLE;COUNTRY:UNSPECIFIED;LOCATION:-;DATAPACKAGEID:%(date)s;INDICATOR_TYPE:SITREP_CUMULATIVE;INDICATOR_TYPE:SITREP_CUMULATIVE_21_DAYS;SEX:-',
    }

    path = {
        'situation_summary' : '../data/A', 
    }

    def __init__(self) :
        pass

    def curl_situation_summary(self, filename, year, month, day) :
        date = {'date' : '%(year)s-%(month)s-%(day)02d' % {'year' : year, 'month' : month, 'day' : day}}
        content = request(self.url['situation_summary'] % date)['content']
        if len(content) > 10000 :
            print year, month, day, len(content)
            open(join(self.path['situation_summary'], filename), 'w').write(content)

if __name__ == '__main__':
    c = curler()
    for year in ['2014'] :
        for month in ['11', '12'] :
            for day in range(1, 32) : 
                filename = 'SituationSummary-%s-%s-%02d.xls' % (year, month, day)
                c.curl_situation_summary(filename, year, month, day)
        