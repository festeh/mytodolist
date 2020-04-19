from django.conf.urls import url
from lists.views import home_page, view_list, new_list

urlpatterns = [
    url(r"new$", new_list, name="new_list"),
    url(r"(\d+)/$", view_list, name="view_list"),
]
