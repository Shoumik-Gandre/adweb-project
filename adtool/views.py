from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib import messages

from rest_framework.views import APIView
from .models import Advertisement, AdvertisementLog, Website
from adtool.advertisement_api import AdvertisementAPI
import secrets
import string



class AdvertisementListView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'adtool/home.html'
    context_object_name = 'Advertisements'
    paginate_by = 5

    def get_queryset(self):
        return Advertisement.objects.filter(user=self.request.user).order_by('-id')


class AdvertisementDetailView(LoginRequiredMixin, UserPassesTestMixin,  DetailView):
    model = Advertisement

    def test_func(self):
        advertisement = self.get_object()
        if self.request.user == advertisement.user:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        log = serializers.serialize('json', self.get_object().advertisementlog_set.filter(is_clicked=True))
        context['click_log'] = log
        return context


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    fields = ['name', 'size', 'image', 'url_link', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdvertisementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Advertisement
    fields = ['name', 'image', 'url_link', 'size', 'category', 'is_enabled']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        advertisement = self.get_object()
        if self.request.user == advertisement.user:
            return True
        return False


class AdvertisementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Advertisement
    success_url = '/'

    def test_func(self):
        advertisement = self.get_object()
        if self.request.user == advertisement.user:
            return True
        return False


class Api(APIView):
    def get(self, request, size, user_key):
        try:
            advertisementapi = AdvertisementAPI(request, Advertisement, size)
            advertisement_html = advertisementapi.get_advertisement(user_key)
            return JsonResponse(advertisement_html, safe=False)
        except Exception as e:
            return JsonResponse("The Advertisement could not be displayed", safe=False)
    
    def post(self, request):
        try:
            size = request.POST['size']
            user_key = request.POST['key']
            advertisementapi = AdvertisementAPI(request, Advertisement, size)
            advertisement_html = advertisementapi.get_advertisement(user_key)
            return JsonResponse(advertisement_html, safe=False)
        except Exception as e:
            return JsonResponse("The Advertisement could not be displayed", safe=False)


def ad_redir(self, pk, site_pk, unique_key):
    try:
        w = Website.objects.get(pk=site_pk)
        ad = Advertisement.objects.get(pk=pk)
        ad.clicks += 1
        ad.save()
        a = AdvertisementLog.objects.get(unique_key=unique_key)
        a.is_clicked = True
        a.save()
        return redirect(str(Advertisement.objects.get(pk=pk).url_link))
    except Exception as e:
        return HttpResponseNotFound('Not Found')


@login_required
def dashboard(request):
    ads = Advertisement.objects.filter(user=request.user)
    ads = serializers.serialize('json', ads)

    context = {
        'ads': ads,
    }
    return render(request, 'adtool/dashboard.html', context)

def landing(request):
    return render(request, 'adtool/landing.html')

def about(request):
    return render(request, 'adtool/about.html')

@login_required
def register_website(request):
    user = request.user
    if user.profile.is_adclient:
        if request.method == 'GET':
            w = Website.objects.filter(user=user)
            return render(request, 'adtool/website_key.html', context={'websites': w})
        elif request.method == 'POST':
                if request.POST['btn'] == 'add':
                    Website.objects.create(user=user, url=request.POST['website-url']).save()
                elif request.POST['btn'] == 'delete':
                    try:
                        Website.objects.get(user=user, url=request.POST['website-url']).delete()
                    except Exception as e:
                        pass

                return redirect('register_website')
    else:
        if request.method == 'POST':
            u_p = user.profile
            u_p.is_adclient = True
            u_p.save()
            Website.objects.create(user=user, url=request.POST['website-url']).save()
            messages.success(request, "Your account has been updated, now you can display ads on your website")
            return redirect('register_website')

        elif request.method == 'GET':
            return render(request, 'adtool/adclient_confirmation.html')


"""
AJAX SECTION
"""

def enable_toggle(request):

    if request.method == 'GET':
        try:
            ad_id = request.GET['ad_id']
            ad_key = request.GET['ad_key']
            toggleThisAd = Advertisement.objects.get(pk=ad_id, identification_key=ad_key)
            toggleThisAd.is_enabled = not toggleThisAd.is_enabled
            toggleThisAd.save()
            return HttpResponse("Success!") # Sending an success response
        except Exception as e:
            print(e)
            return HttpResponse("Failure!")
    else:
        return HttpResponse("Request method is not a GET")

def change_userkey(request):
    if request.method == 'GET':
        user_key = request.GET['key']
        try:
            w = Website.objects.get(userkey=user_key)
            w.save()
            userkey = w.userkey
            return HttpResponse(userkey)
        except Exception as e:
            return HttpResponse(status=404)

def delete_userkey(request):
    if request.method == 'GET':
        user_key = request.GET['key']
        try:
            w = Website.objects.get(userkey=user_key)
            w.delete()
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=404)