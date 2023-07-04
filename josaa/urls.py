from . import views
from django.urls import path

urlpatterns=[
    path("",views.login_view,name="LoginView"),
    path("FilterbyInstitute",views.FilterbyInstitute,name="FilterbyInstitute"),
    path("FilterbyProgram",views.FilterbyProgram,name="FilterbyProgram"),
    path("InstituteTrends",views.InstituteTrends,name="InstituteTrends"),
    path("ProgramTrends",views.ProgramTrends,name="ProgramTrends"),
    path("RoundTrends",views.RoundTrends,name="RoundTrends")
]