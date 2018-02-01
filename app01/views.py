from django.shortcuts import render,HttpResponse

# Create your views here.
def test(req):
    req.session['aaa']='666'
    return HttpResponse('ok')