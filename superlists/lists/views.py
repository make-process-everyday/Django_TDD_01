from django.shortcuts import render, redirect
from lists.models import Item
from django.http import HttpResponse

# 在这里编写视图,视图函数有两个作用：
# 一是处理用户输入，二是返回适当的响应
def home_page(request):
    # return HttpResponse('<html><title>To-Do lists</title></html>')
    # render 函数， 根据请求， 调用模板，返回HeepResponse 对象
    # 模板功能是Django 很强的一个功能
    return render(request, 'home.html', {'new_item_text': request.POST.get('item_text',"")})

# Create your views here.
