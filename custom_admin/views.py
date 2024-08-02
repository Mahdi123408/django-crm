from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class AdminView(View):
    def get(self, request):
        ...
    def post(self, request):
        ...