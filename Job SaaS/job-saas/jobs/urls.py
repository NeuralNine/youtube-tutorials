from django.urls import path

from .views import home_view, search_job_view, results_list_view

urlpatterns = [
    path('', home_view, name='home'),
    path('search/', search_job_view, name='search'),
    path('results/', results_list_view, name='results'),
]
