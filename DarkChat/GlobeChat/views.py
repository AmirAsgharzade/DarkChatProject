from django.shortcuts import render
from django.http import JsonResponse ,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET
from .models import GlobeHistory
from Authen.models import CustomUser
import json
import asyncio
from django.core.cache import cache


global folder 
folder = 'GlobeChat/'

class IndexView(LoginRequiredMixin,TemplateView):
    login_url = 'authen/login'
    redirect_field_name = ''
    template_name = f'{folder}index.html'
    

class GlobeHistoryMessages(View):
    http_method_names = ['get']
    async def get(self,request,*args,**kwargs):
        offset = int(request.GET.get('offset',0))  # Default to 0 if not provided
        limit = int(request.GET.get('limit', 20))
        loop = asyncio.get_event_loop()
        messages = await loop.run_in_executor(None,cache.get,'messages')
        if not messages:
            messages = await loop.run_in_executor(None,self.get_history)
            cache.set('messages',messages,timeout=60)
            # data = {'messages':list(messages)}
            # print(messages)
        return JsonResponse(messages[offset:offset+limit],safe=False)

    def get_history(self,*args):
        return list(GlobeHistory.objects.all().order_by('-timestamp').values())

class MessageSent(View):
    async def get(self,request,*args,**kwargs):
        return HttpResponse('Method Not allowed',status=405)
    async def post(self,request,*args,**kwargs):
        loop = asyncio.get_event_loop()
        data = json.loads(request.body)

        user = await loop.run_in_executor(None,self.get_user,data['username'])
        if user:
            await loop.run_in_executor(None,self.create_message,user,data['content'])
            await loop.run_in_executor(None,cache.delete,'messages')
        return JsonResponse({'sent':True},status=201)
    
    def get_user(self,username):
        return CustomUser.objects.get(username=username)
    def create_message(self,user,content):
        message = GlobeHistory.objects.create(
            user=user,username=user.username,color=user.color,content= content
            )
        message.save()
        return True


def test(request):
    return render(request,'GlobeChat/test.html')
