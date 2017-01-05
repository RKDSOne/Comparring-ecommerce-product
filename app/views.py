from django.shortcuts import render_to_response
from django.template import RequestContext
from bs4 import BeautifulSoup as bs
from py_bing_search import PyBingWebSearch
from app.forms import *
import requests

def compare(request):
    if request.method == 'POST':
        form = search(request.POST)
        if form.is_valid():
            product = form.cleaned_data['querry']
            API_KEY = "Your API key"

            querry = "buy " + product

            bing_web = PyBingWebSearch(API_KEY, querry, web_only=False)

            results = bing_web.search(limit=50, format='json')

            fkart_urls = []
            fkart_price_ar = []
            sdeal_urls = []
            sdeal_price_ar = []
            min_fkart = 0
            min_sdeal = 0

            for result in results:
                comp = result.url.split('.')[1]

                if comp == 'flipkart':
                    p = ' '

                    try:
                        p = result.url.split('/')[4]
                    except:
                        continue

                    if p == 'p':
                        fkart_urls.append(result.url)
                        fkart_flag = 1

                if comp == 'snapdeal':
                    p = ' '

                    try:
                        p = result.url.split('/')[3]
                    except:
                        continue

                    if p == 'product':
                        sdeal_urls.append(result.url)
                        sdeal_flag = 1

            if len(fkart_urls) == 0 and len(sdeal_urls) == 0:
                result = 'Search Failed!'
                context = RequestContext(request, {'result': result})
                return render_to_response('home.html', context)

            else:
                for url in fkart_urls:
                    fkart_url = url
                    fkart_page = requests.get(fkart_url)
                    fkart_html = fkart_page.text
                    fkart_soup = bs(fkart_html, 'html.parser')
                    meta_desc = fkart_soup.findAll(attrs={"name": "Description"})
                    meta_desc_content_split = meta_desc[0]['content'].split(" ")
                    for_bool = 0
                    For_bool = 0

                    try:
                        for_index = meta_desc_content_split.index('for')
                    except:
                        for_bool = 1

                    try:
                        for_index = meta_desc_content_split.index('For')
                    except:
                        For_bool = 1

                    if for_bool == 0 or For_bool == 0:
                        str_price = meta_desc_content_split[for_index + 1]
                        if(str_price == 'Rs.'):
                            fkart_price = meta_desc_content_split[for_index + 2]
                            fkart_price_ar.append(fkart_price)
                        else:
                            fkart_price = str_price[3:]
                            fkart_price_ar.append(fkart_price)

                for url in sdeal_urls:
                    sdeal_url = url
                    sdeal_page = requests.get(sdeal_url)
                    sdeal_html = sdeal_page.text
                    sdeal_soup = bs(sdeal_html, 'html.parser')
                    input_tag = sdeal_soup.find_all('input', id='productPrice')
                    ex = 0
                    try:
                        str_price = input_tag[0]['value']
                    except:
                        ex = 1
                    if(ex != 1):
                        sdeal_price_ar.append(str_price)

                if(len(fkart_price_ar)>0):
                    min_fkart = fkart_price_ar[0]
                    for price in fkart_price_ar:
                        if(price>min_fkart):
                            min_fkart = price

                if(len(sdeal_price_ar)>0):
                    min_sdeal = sdeal_price_ar[0]
                    for price in sdeal_price_ar:
                        if(price>min_sdeal):
                            min_sdeal = price

                result = 'Search Succesful!'
                context = RequestContext(request, {
                    'form': form,
                    'result': result,
                    'flipkart_price': str(min_fkart),
                    'snapdeal_price': str(min_sdeal)
                })
                return render_to_response('home.html', context)
    else:
        form = search()
        context = RequestContext(request, {'form': form})
        return render_to_response('home.html', context)

