from piston.handler import BaseHandler
#from Intellishop.models import Api
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
# from django.forms import ModelForm
# from django import forms
from django.views.decorators.csrf import csrf_exempt
from models import Product, Illiterate
import re
class CalcHandler( BaseHandler ):
    def read( self, request, expression ):
#        p=Api(input=expression)
#        p.save()
        search_product = str.lower(str(expression))
        lis = re.split(',', (search_product))
        error = "Please check the order of entry"
        try:
            search_str1 = Illiterate.objects.get(common_name=lis[0]).actual_name
            search_str2 = Illiterate.objects.get(common_name=lis[1]).actual_name
        except:
            search_str1 = ""
            search_str2 = ""
            log = open("logs/log.txt", "a")
            log.write(search_product + "\n")
            log.close()
            error = "object does not exist in database try refining your search"
        if len(lis) == 2:
            prod = Product.objects.filter(product_name=search_str1, shops__shop_name=search_str2)
            if (bool(prod)):
                argument = 'shop/result.html/'
                t = loader.get_template(argument)
                c = Context({'prod': prod, 'search_product': lis[0],'notsame':(search_product!=prod[0].product_name)})
                return HttpResponse(t.render(c))
            elif (error):
                return HttpResponse(error)
        elif len(lis) == 3:
            try:
                search_str3 = Illiterate.objects.get(common_name=lis[2]).actual_name
            except:
                search_str3 = ""
                log = open("logs/log.txt", "a")
                log.write(search_product + "\n")
                log.close()
                error = "object does not exist in database try refining your search"
            prod = Product.objects.filter(product_name=search_str1, manufacturer=search_str2, shops__shop_name=lis[2])
            if (bool(prod)):
                argument = 'shop/result.html/'
                t = loader.get_template(argument)
                c = Context({'prod': prod, 'search_product': lis[0],'notsame':(search_product!=prod[0].product_name)})
                return HttpResponse(t.render(c))
            elif (error):
                return HttpResponse(error)
        else:
            pass
        return render_to_response('shop/base.html/')