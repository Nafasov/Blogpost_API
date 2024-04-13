from django.urls import path
from .views import ContactAPIView

app_name = 'contact'

urlpatterns = [
    path('contact/', ContactAPIView.as_view(), name='contact'),
]

'''
    Contact
        -list
        -create
'''
