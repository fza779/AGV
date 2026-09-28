from django.urls import path

from .views import FzaHealthView, PathPlanningView


urlpatterns = [
    path("health/", FzaHealthView.as_view(), name="fza-health"),
    path("path-plan/", PathPlanningView.as_view(), name="path-plan"),
]
