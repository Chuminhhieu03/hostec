from django.urls import path
from application import views

urlpatterns = [
    path('',views.index,name="index"),
    path('<id>/detail',views.detail,name="detail"),
    path('show/',views.showCart, name="showCart"),
    path('addToCart/',views.addToCart,name="addToCart"),
    path('increaseCart/',views.increaseCart,name="increaseCart"),
    path('decreaseCart/',views.decreaseCart,name="decareaseCart"),
    path('removeCart/',views.removeCart,name="removeCart"),
    path('testimo/',views.testimo,name="testimo"),
    path('contact/',views.contact,name="contact"),
    path('portfolio/',views.portfolio,name="portfolio"),
    path('createOrder/',views.createOrder,name="createOrder"),
    path('order/',views.getOrder,name="getOrder"),
    path('order/<id>',views.getOrderdt,name="getOrder"),
    path('makeComment/',views.makeComment,name="makeComment"),
    path('demo/',views.demo,name="demo")
]