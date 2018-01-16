#encoding: utf-8
from urllib2 import urlopen
import requests
import json
import urllib
import urllib2
import pymssql
import SqlCon
import sys
import httplib
import  xml.dom.minidom

def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'BHPn8rBxKYDmyqhCT4T9GEfj6EKInPFZ'#SmrfzDZ39a762A0FcVXEaCjBPs2HPM11
    uri = url + '?' + 'address=' + address  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read()
    temp = json.loads(res)
    lat=temp['result']['location']['lat']
    lng=temp['result']['location']['lng']
    return lat,lng

def testgetlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'BHPn8rBxKYDmyqhCT4T9GEfj6EKInPFZ'#SmrfzDZ39a762A0FcVXEaCjBPs2HPM11
    uri = url + '?' + 'address=' + address  + '&output=' + output + '&ak=' + ak
    print uri
    req = urlopen(uri)
    res = req.read()
    temp = json.loads(res)
    print temp
    # lat=temp['result']['location']['lat']
    # lng=temp['result']['location']['lng']
    # return lat,lng

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    #ll = testgetlnglat('桂林市荔蒲县')
    dom = xml.dom.minidom.parse('SQLConfig')
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
    #print sqlstr
    #print host
    #print un,pd,dbt
    ms = SqlCon.SqlCon(host=host,user=un,pwd=pd,db=dbt)
    #ms = SqlCon.SqlCon(host='.', user='sa', pwd='1qaz@WSX', db='testdb')
    reslist = ms.ExecQuery(sqlstr)
    for i in reslist:
        s=i[1]
        try:
            ll=getlnglat(str(i[1]))
            #print 1
            #print ll
            newsql=sqlsupdate%(ll,str(i[0]));
            print newsql
            ms.ExecNonQuery(newsql)
        except:
            print str(i[0])
            continue








#newsql="update dbo.CityMapDistance set name='%s' where id=1"%u'????'
#print newsql
#ms.ExecNonQuery(newsql.encode('utf-8'))
    #file=open(r"C:\Users\MaMQ\hrFood.json",encoding='utf-8')
    #data=[]
    #newData=[]
    #for line in file:
    #    data.append(json.loads(line[:-2]))
    #for dic in data:
    #    address=dic['??ַ']
    #    lat,lng=getlnglat(address)
    #    dic['lat']=lat
    #    dic['lng']=lng
    #    newData.append(dic)
    #for dic in newData:
    #    __jsonDump("HuaiRou",dic)
