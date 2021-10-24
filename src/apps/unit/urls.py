from django.urls import path

from .views import (
    TopicViewSet,
    UnitViewSet,
    UnitTheoryElementViewSet,
    UnitExercisesElementViewSet,
    UnitUserAnswerViewSet
)


urlpatterns = (
    path("topics/list/", TopicViewSet.as_view({"get": "list"}), name="topic-list"),
    path("units/list/", UnitViewSet.as_view({"get": "list"}), name="unit-list"),
    path("units/theory/list/",
         UnitTheoryElementViewSet.as_view({"get": "list"}),
         name="unit-theory-list"),
    path("units/exercise/list/",
         UnitExercisesElementViewSet.as_view({
             "get": "list",
         }),
         name="unit-exercise-list"),
    path("units/exercise/answer/",
         UnitUserAnswerViewSet.as_view({
             "get": "list",
             "post": "create"
         }),
         name="unit-exercise-answers"),
)
