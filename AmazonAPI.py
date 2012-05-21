from xml.dom import minidom
import urllib
import urllib2
import httplib2
import base64, hashlib, hmac, time
from datetime import datetime
import re
from urllib import quote

# author Marcos Lopez dev@scidentify.info

class Amazon(object):
  """
  Amazon API to search for products 
  """
  # change this to load from settings!
  AMAZON_ACCESSKEY = 'accesske'
  submit_url = 'http://ecs.amazonaws.com/onca/xml?'

  params = {
    'Service': 'AWSECommerceService',
    'Version': '2010-11-01',
    'Operation': 'ItemSearch',
    'SearchIndex': 'All',
    'Keywords': '',
    'AWSAccessKeyId': AMAZON_ACCESSKEY,
    'ResponseGroup': 'Small,Offers',
    'AssociateTag': 'user-20'
    
  }
  secret_key = ''
  
  def __init__(self, search_keyword=None, secret_key=None):
    if not secret_key:
      return False
    if not search_keyword:
      return False

    self.secret_key = secret_key
    self.params['Keywords'] = search_keyword
    self.params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    self.full_url = self.do_signature(secret_key)
    #print self.buildRequest()
    #self.test_url(url=self.submit_url)


  def do_signature(self, secret_key):

    keys = sorted(self.params.keys())
    args = '&'.join('%s=%s' % (key, quote(unicode(self.params[key]).encode('utf-8'),safe='~')) for key in keys)

    # Amazon uses a different host for XSLT operations
    #host = self.host['Style' in self.params]

    msg = 'GET'
    msg += '\necs.amazonaws.com'
    msg += '\n/onca/xml'
    msg += '\n' + args

    signature = base64.encodestring(hmac.new(self.secret_key, msg, hashlib.sha256).digest())

    url = 'http://%s/onca/xml?%s&Signature=%s' % ('ecs.amazonaws.com', args, signature.replace('/','%2F').replace('+','%2B').replace('=','%3D'))
    return url
    
    
    #return '%s%s' % (self.submit_url, url_string)

  
  def test_url(self, url=None):
    #httpsend = httplib2.Http()
    #response, data = httpsend.request(url, 'GET', {})
    #print response, data

    try:
      data = urllib2.urlopen(self.full_url).read()
    except urllib2.URLError:
      data = None
    if not data:
      final_parse_result = []
      return final_parse_result

    parsedata = minidom.parseString(data)
    elems = parsedata.getElementsByTagName('Items')
    final_parse_result = []
    for i in elems:
    # for each items
      for x in i.childNodes:
        if x.nodeName == 'Item':
          #get the link url
          #detailpage = x.getElementByTagName('DetailPageURL')
          #print detailpage
          dict = {}
          for y in x.childNodes:
            if str(y.nodeName) == 'DetailPageURL':
              #print y.firstChild.data
              dict['url'] = y.firstChild.data

            # all this to get the price...
            if str(y.nodeName) == 'Offers':
              for offer in y.childNodes:
                if offer.nodeName == 'Offer':
                  for offer_detail in offer.childNodes:
                    #print ' - offers - offer - %s' % offer_detail.nodeName
                    if offer_detail.nodeName == 'OfferListing':
                      for price in offer_detail.getElementsByTagName('Price'):
                        for o in price.childNodes:
                          #print o.nodeName
                          if o.nodeName == 'Amount':
                            #print o.firstChild.data
                            dict['amount'] = o.firstChild.data
                          if o.nodeName == 'FormattedPrice':
                            #print o.firstChild.data
                            dict['format_price'] = o.firstChild.data

            
          for y in x.childNodes:
            if not dict.get('format_price', None):
              #print 'no price, lets try again somewhere else in the XML'
              if str(y.nodeName) == 'OfferSummary':
                for offsum in y.childNodes:
                  if offsum.nodeName == 'LowestNewPrice':
                    for lowprice in offsum.childNodes:
                      if lowprice.nodeName == 'Amount':
                        dict['amount'] = lowprice.firstChild.data
                      if lowprice.nodeName == 'FormattedPrice':
                        dict['format_price'] = lowprice.firstChild.data
                

          dict['merchant'] = 'Amazon'
          final_parse_result.append(dict)
          

    ccc=0
    for i in final_parse_result:
      if not i.get('amount', None):
        final_parse_result.pop(ccc)
      ccc+=1
      # print i

    return final_parse_result
