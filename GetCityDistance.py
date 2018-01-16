# encoding: utf-8
from urllib2 import urlopen, Request
import requests
import json
import urllib
import urllib2
import pymssql
import SqlCon
import sys
import httplib
import  xml.dom.minidom

def getDistance(slatlngs, dlatlng,ak):
    url = 'http://api.map.baidu.com/routematrix/v2/driving'
    output = 'json'
    #'BHPn8rBxKYDmyqhCT4T9GEfj6EKInPFZ'
    #'SmrfzDZ39a762A0FcVXEaCjBPs2HPM11'
    file_object = open('thefile.txt', 'a')
    file_object.write(url + '\n')
    try:
        print -1

        # headers = { 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; utf-8; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }
        params = {'output': output, 'origins': slatlngs, 'destinations': dlatlng,
                  'ak': 'SmrfzDZ39a762A0FcVXEaCjBPs2HPM11'}
        data = {}
        data['output'] = output
        data['origins'] = slatlngs
        data['destinations'] = dlatlng
        data['ak'] = ak
        # values = {'name' : 'Michael Foord',
        #  'location' : 'Northampton',
        #  'language' : 'Python' }
        uri = url + '?' + 'output=' + output + '&origins=' + slatlngs + '&destinations=' + dlatlng + '&ak=' + ak
        req = requests.get(uri)
        print req

        # ?????û?????
        temp = req.json()
        print temp
        dis = temp['result'][0]['distance']['value']
        return dis
    except Exception, e:
        file_object = open('thefile.txt', 'a')
        file_object.write(str(e) + '\n')
        file_object.close()
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        return 1


# def __jsonDump(name,_json):
#    """???뱣??·?????ֵ??????????????ݵ???Ӧ???ļ???"""
#    with open(name + '.json','a') as outfile:
#        json.dump(_json,outfile,ensure_ascii=False)
#    with open(name + '.json','a') as outfile:
#        outfile.write(',\n')
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    dom = xml.dom.minidom.parse('GetDistanceConfig')
    root = dom.documentElement
    itemlist = root.getElementsByTagName('login')
    item = itemlist[0]
    un = str(item.getAttribute("username"))
    pd = str(item.getAttribute("passwd"))
    ss = dom.getElementsByTagName('SQLSTR')
    sqlstr = str(ss[0].firstChild.data)
    su = dom.getElementsByTagName('SQLUpdate')
    sqlsupdate = str(su[0].firstChild.data)
    ht = dom.getElementsByTagName('host')
    host = str(ht[0].firstChild.data)
    db = dom.getElementsByTagName('database')
    dbt = str(db[0].firstChild.data)
    ak = dom.getElementsByTagName('baiduak')
    bak = str(ak[0].firstChild.data)
    ms = SqlCon.SqlCon(host=host, user=un, pwd=pd, db=dbt)
    # reslist = ms.ExecQuery("  SELECT  LngLat  FROM dbo.CityMapDistance WHERE id IN (SELECT   min(ID) FROM dbo.CityMapDistance GROUP BY CityName )")
    # for i in reslist:
    #    s+=i[0]+'|'
    # s=s[:-1]
    print sqlstr
    sreslist = ms.ExecQuery(sqlstr)
    for m in sreslist:
        try:
            dc = getDistance(m[0], m[1],bak)
            if dc <= 1:
                sys.exit(0)
            else:
                id = m[2]
                newsql = sqlsupdate% (dc, id);
                print newsql
                ms.ExecNonQuery(newsql.encode('utf-8'))
        except:
            file_object = open('thefile.txt', 'a')
            file_object.write('\n')
            file_object.close()
            # print 'str(Exception):\t', str(Exception)
            # print 'str(e):\t\t', str(e)
            # print 'repr(e):\t', repr(e)
            # print 'e.message:\t', e.message

            # if __name__ == '__main__':
            #   reload(sys)
            #   sys.setdefaultencoding('utf8')
            #   ms = SqlCon.SqlCon(host="59.151.127.51",user="datawarehouse_r",pwd="sdLEK236XDwd6",db="YHBI_DW")
            #   reslist = ms.ExecQuery("select distinct sCityName from dbo.CityMapDistance")
            #   for i in reslist:
            #       s=i[0]
            #       try:
            #           ll=getlnglat(str(i[0]))
            #           #print 1
            #           #print ll
            #           newsql="update dbo.CityMapDistance set SLngLat='%s' where sCityName='%s'"%(ll,s);
            #           #print newsql
            #           ms.ExecNonQuery(newsql.encode('utf-8'))
            #       except:
            #           print i[0]
            #           continue








            # newsql="update dbo.CityMapDistance set name='%s' where id=1"%u'????'
            # print newsql
            # ms.ExecNonQuery(newsql.encode('utf-8'))
            # file=open(r"C:\Users\MaMQ\hrFood.json",encoding='utf-8')
            # data=[]
            # newData=[]
            # for line in file:
            #    data.append(json.loads(line[:-2]))
            # for dic in data:
            #    address=dic['??ַ']
            #    lat,lng=getlnglat(address)
            #    dic['lat']=lat
            #    dic['lng']=lng
            #    newData.append(dic)
            # for dic in newData:
            #    __jsonDump("HuaiRou",dic)
