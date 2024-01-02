from django.urls import path
from . import views
from .views import TeamView

urlpatterns = [
    path("", views.getRoutes),
    # Team API
    path("getTeam/<str:teamId>", views.TeamView.get),
    path("postTeam", views.TeamView.post),
    path("deleteTeam/<str:teamId>", views.TeamView.delete),
    path("getTeams", views.TeamView.getTeams),
    path("arrived/<str:teamId>", views.TeamView.arrived),
    path("postRoute", views.TeamView.post_route),
    path("resetRoute", views.TeamView.reset_route),
    path("getRoute/<str:teamId>", views.TeamView.getRoute),
    # Validation API
    path("validate_token/", views.ValidationView.validate_token),
    path("signout/", views.ValidationView.signout),
]
