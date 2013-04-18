from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import Product, Illiterate, Shop
import re
import dj_simple_sms
@csrf_exempt
def home(request):
    error=''
    if(request.method == 'POST'):
        search_product = re.sub( '\s+', ' ', str.lower(str(request.POST.get(r'search_product'))) ).strip()
        lis = re.split(',', (search_product))
        if(len(lis)==0 or len(lis)==1):
            error = "Entry not standard compliant!!! Please check below."
            argument = 'shop/base.html'
            t = loader.get_template(argument)
            c = Context({'error': error})
            return HttpResponse(t.render(c))
        try:
            search_str1 = Illiterate.objects.get(common_name=lis[0].strip()).actual_name
            search_str2 = Illiterate.objects.get(common_name=lis[1].strip()).actual_name
        except:
            search_str1 = ""
            search_str2 = ""
            log = open("logs/log.txt", "a")
            log.write(search_product + "\n")
            log.close()
            error = "object does not exist in database try refining your search"
        if len(lis) == 2:
            prod = Product.objects.filter(product_name=search_str1, shops__shop_name=search_str2)
            if not prod:
                prod = Product.objects.filter(manufacturer=search_str1, shops__shop_name=search_str2)
            if (bool(prod)):
                argument = 'shop/result.html/'
                t = loader.get_template(argument)
                c = Context({'prod': prod, 'search_product': lis[0],'notsame':(search_product!=prod[0].product_name)})
                return HttpResponse(t.render(c))
            elif (error):
                argument = 'shop/base.html'
                t = loader.get_template(argument)
                c = Context({'error': error})
                return HttpResponse(t.render(c))
        elif len(lis) == 3:
            try:
                search_str3 = Illiterate.objects.get(common_name=lis[2].strip()).actual_name
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
                argument = 'shop/base.html'
                t = loader.get_template(argument)
                c = Context({'error': error})
                return HttpResponse(t.render(c))
    else:
        pass
    argument = 'shop/base.html'
    t = loader.get_template(argument)
    c = Context({'error': error})
    return HttpResponse(t.render(c))
def shops(request):
    if not (request.GET.keys()):
        try:
            shops = Shop.objects.all()
            argument = 'shop/shops.html'
            t = loader.get_template(argument)
            c = Context({'shops':shops})
            return HttpResponse(t.render(c))
        except:
            pass
    else:
        try:
            prods = Product.objects.filter(shops__shop_name=request.GET['sname'])
            argument = 'shop/products.html'
            t = loader.get_template(argument)
            c = Context({'products':prods})
            return HttpResponse(t.render(c))
        except:
            pass
    return HttpResponse("all failed")
def about(request):
    t = loader.get_template('shop/about.html')
    c = Context({})
    return HttpResponse(t._render(c))
def sms(sms):
        message='test'
        error='Empty Message!!!'
        search_product= sms.body.strip()
        if(search_product):
            search_product= re.sub( '\s+', ' ', str.lower(str(sms.body)) ).strip()
            lis = re.split(',', (search_product))
            if(len(lis)==0 or len(lis)==1):
                error = "Please check the format of entry"
                response = dj_simple_sms.models.SMS(to_number=sms.from_number, from_number='Intellishop', body=error)
                response.send()
                return
            try:
                search_str1 = Illiterate.objects.get(common_name=lis[0].strip()).actual_name
                search_str2 = Illiterate.objects.get(common_name=lis[1].strip()).actual_name
            except:
                search_str1 = ""
                search_str2 = ""
                log = open("logs/log.txt", "a")
                log.write(search_product + "\n")
                log.close()
                error = "object does not exist in database try refining your search"
            if len(lis) == 2:
                prod = Product.objects.filter(product_name=search_str1, shops__shop_name=search_str2)
                if not prod:
                    prod = Product.objects.filter(manufacturer=search_str1, shops__shop_name=search_str2)
                if (bool(prod)):
                    for product in prod:
                        message=product.product_name+" is in "+search_str2+"\n"
                    response = dj_simple_sms.models.SMS(to_number=sms.from_number, from_number='Intellishop', body=message)
                    response.send()
                    return
                elif(search_str2 or search_str1) :
                    error = "Please check the format of entry"
                    response = dj_simple_sms.models.SMS(to_number=sms.from_number, from_number='Intellishop', body=error)
                    response.send()
                    return
                else :
                    error = "object does not exist in database try refining your search"
                    response = dj_simple_sms.models.SMS(to_number=sms.from_number, from_number='Intellishop', body=error)
                    response.send()
                    return
            elif len(lis) == 3:
                try:
                    search_str3 = Illiterate.objects.get(common_name=lis[2].strip()).actual_name
                except:
                    search_str3 = ""
                    log = open("logs/log.txt", "a")
                    log.write(search_product + "\n")
                    log.close()
                    error = "object does not exist in database try refining your search"
                    response = dj_simple_sms.models.SMS(to_number=sms.from_number, from_number='Intellishop', body=error)
                    response.send()
                    return
                prod = Product.objects.filter(product_name=search_str1, manufacturer=search_str2, shops__shop_name=lis[2].strip())
                if (bool(prod)):
                    for product in prod:
                        message=product.product_name+" by "+search_str2+" is in "+search_str3+"\n"
                    response = dj_simple_sms.models.SMS(to_number=sms.from_number, from_number='Intellishop', body=message)
                    response.send()
                    return
                elif (error):
                    response = dj_simple_sms.models.SMS(to_number=sms.from_number, from_number='Intellishop', body=error)
                    response.send()
                    return
        else:
            response = dj_simple_sms.models.SMS(to_number=sms.from_number, from_number='Intellishop', body=message)
            response.send()
