from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import ArticleSerializers
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Article
# Create your views here.

@csrf_exempt
def article_list(request):

    if request.method == 'GET':
         articles = Article.objects.all()
         serializer = ArticleSerializers(articles, many=True)
         return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        else:
            return JsonResponse(serializer.errors,status=400)

@csrf_exempt
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist :
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ArticleSerializers(article)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializers(article,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors,status=400)    
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse('deleted',status=204)



