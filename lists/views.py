import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from todolist import settings

temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"


def index(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None or search == "top":
        # get the top news
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
            "us", 1, settings.APIKEY
        )
    else:
        # get the search query request
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            search, "popularity", page, settings.APIKEY
        )
    r = requests.get(url=url)

    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    context = parse_news_content(data, search)
    # send the news feed to template in context
    return render(request, 'lists/home.html', context=context)


def parse_news_content(data, search):
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    # seprating the necessary data
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description": "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"]
        })
    return context


# return render(request, "lists/index.html", {"form": TodoForm()})

def load_content(request):
    try:
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)
        if search is None or search == "top":
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us", page, settings.APIKEY
            )
        else:
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search, "popularity", page, settings.APIKEY
            )
        print("url:", url)
        r = requests.get(url=url)

        data = r.json()
        if data["status"] != "ok":
            return JsonResponse({"success": False})
        context = parse_news_content(data, search)
        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({"success": False})
