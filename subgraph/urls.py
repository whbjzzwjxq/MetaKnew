from django.conf.urls import url
from subgraph import views
from subgraph.script import Latin_America_Import as latin
urlpatterns = [
    url("add/node", views.add_node),
    url("run/script", latin.script_latin)
]
