from django.conf.urls import url
from lists.views import home_page, view_list, new_list, add_task

urlpatterns = [
    url(r"new$", new_list, name="new_list"),
    url(r"(\d+)/$", view_list, name="view_list"),
    url(r"(\d+)/add_task", add_task, name="add_task")
]
