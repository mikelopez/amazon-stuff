from AmazonAPI import *
url = 'http://ecs.amazonaws.com/onca/xml?AWSAccessKeyId=AKIAJWMJWQF2BFASPJ4A&ItemId=B003VUO6H4&Keywords=ps3&Operation=ItemSearch&ResponseGroup=Small%2COffers&SearchIndex=All&Service=AWSECommerceService&Timestamp=2011-05-11T06%3A41%3A36.000Z&Version=2010-11-01&Signature=ZlJsd5c4%2BDCfg8wLitibL8ZanXEGzuGFbKexy9Cqs%2Fk%3D'

a= Amazon(search_keyword='ps3', secret_key='zSuaWUAMlOcYnuzQqftg0DzElU/LxLHaxhC24O9Y')
v = a.test_url()
print 'var is'
print v
