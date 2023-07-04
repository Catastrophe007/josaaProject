from django.shortcuts import render
from josaa.models import *
import pandas as pd
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("FilterbyInstitute")  # Replace 'home' with your desired URL name or path
    else:
        form = LoginForm()
    return render(request, 'josaa/login.html', {'form': form})


def FilterbyInstitute(request):
    institute = (
        AcademicProgram.objects.order_by("Institute").values("Institute").distinct()
    )
    institute_names = {"institutes": [item["Institute"] for item in institute]}
    if request.method == "POST":
        college = request.POST.get("college")
        seat = request.POST.get("seat")
        dt = AcademicProgram.objects.filter(Institute=college, SeatType=seat)
        qs = pd.DataFrame(dt.values())
        qs = qs.to_html()
        context = {"institute_names": institute_names, "qs": qs}
        return render(request, "josaa/FilterbyInstitute.html", context)
    return render(request, "josaa/FilterbyInstitute.html", institute_names)


def FilterbyProgram(request):
    program = (
        AcademicProgram.objects.order_by("AcademicProgramName")
        .values("AcademicProgramName")
        .distinct()
    )
    program_names = {"programs": [item["AcademicProgramName"] for item in program]}
    if request.method == "POST":
        program = request.POST.get("program")
        seat = request.POST.get("seat")
        dt = AcademicProgram.objects.filter(AcademicProgramName=program, SeatType=seat)
        qs = pd.DataFrame(dt.values())
        qs = qs.to_html()
        context = {"program_names": program_names, "qs": qs}
        return render(request, "josaa/FilterbyProgram.html", context)
    return render(request, "josaa/FilterbyProgram.html", program_names)


def InstituteTrends(request):
    institute = (
        AcademicProgram.objects.order_by("Institute").values("Institute").distinct()
    )
    institute_names = {"institutes": [item["Institute"] for item in institute]}
    if request.method == "POST":
        college = request.POST.get("college")
        seat = request.POST.get("seat")
        gender = request.POST.get("gender")
        dt = AcademicProgram.objects.filter(
            Institute=college, SeatType=seat, Gender=gender, Round=6
        )
        qs = pd.DataFrame(dt.values())
        qs = qs[["AcademicProgramName", "ClosingRank", "Year"]]
        qs.sort_values("AcademicProgramName")
        qs = qs[~qs["ClosingRank"].astype(str).str.endswith("P")]
        pd.set_option("display.max_rows", None)
        programs = qs["AcademicProgramName"].unique()
        programs = programs.tolist()
        print(programs)
        print(qs)
        data_list = []
        for _, row in qs.iterrows():
            program = row["AcademicProgramName"]
            rank = row["ClosingRank"]
            year = row["Year"]

            # Check if the program already exists in the data list
            program_dict = next((d for d in data_list if d["Program"] == program), None)
            if program_dict is None:
                # Create a new dictionary if the program doesn't exist
                program_dict = {"Program": program, "Rank": [], "Year": []}
                data_list.append(program_dict)

            # Append the closing rank to the program's rank list
            program_dict["Rank"].append(rank)
            program_dict["Year"].append(year)
        print(data_list)
        json_data = json.dumps(data_list)
        context = {"institute_names": institute_names, "json_data": json_data}
        return render(request, "josaa/InstituteTrends.html", context)
    return render(request, "josaa/InstituteTrends.html", institute_names)


def ProgramTrends(request):
    program = (
        AcademicProgram.objects.order_by("AcademicProgramName")
        .values("AcademicProgramName")
        .distinct()
    )
    program_names = {"programs": [item["AcademicProgramName"] for item in program]}

    if request.method == "POST":
        program = request.POST.get("program")
        seat = request.POST.get("seat")
        gender = request.POST.get("gender")
        dt = AcademicProgram.objects.filter(
            AcademicProgramName=program, SeatType=seat, Gender=gender, Round=6
        )
        qs = pd.DataFrame(dt.values())
        qs = qs[["Institute", "ClosingRank", "Year"]]
        qs.sort_values("Institute")
        qs = qs[~qs["ClosingRank"].astype(str).str.endswith("P")]
        # pd.set_option('display.max_rows', None)
        # programs=qs['AcademicProgramName'].unique()
        # programs=programs.tolist()
        # print(programs)
        print(qs)
        data_list = []
        for _, row in qs.iterrows():
            institute = row["Institute"]
            rank = row["ClosingRank"]
            year = row["Year"]

            # Check if the program already exists in the data list
            institute_dict = next(
                (d for d in data_list if d["Institute"] == institute), None
            )
            if institute_dict is None:
                # Create a new dictionary if the program doesn't exist
                institute_dict = {"Institute": institute, "Rank": [], "Year": []}
                data_list.append(institute_dict)

            # Append the closing rank to the program's rank list
            institute_dict["Rank"].append(rank)
            institute_dict["Year"].append(year)
        print(data_list)
        json_data = json.dumps(data_list)
        context = {"program_names": program_names, "json_data": json_data}
        return render(request, "josaa/ProgramTrends.html", context)
    return render(request, "josaa/ProgramTrends.html", program_names)


def RoundTrends(request):
    program = (
        AcademicProgram.objects.order_by("AcademicProgramName").values("AcademicProgramName").distinct()
    )
    program_names = {"programs": [item["AcademicProgramName"] for item in program]}
    institute = (
        AcademicProgram.objects.order_by("Institute").values("Institute").distinct()
    )
    institute_names = {"institutes": [item["Institute"] for item in institute]}
    if request.method == "POST":
        program = request.POST.get("program")
        college = request.POST.get("college")
        seat = request.POST.get("seat")
        gender = request.POST.get("gender")
        dt = AcademicProgram.objects.filter(AcademicProgramName=program, SeatType=seat, Gender=gender, Institute=college) 
        qs = pd.DataFrame(dt.values())
        qs = qs[["ClosingRank", "Year", "Round"]]
        print(qs)
        qs.sort_values("Round")
        qs = qs[~qs["ClosingRank"].astype(str).str.endswith("P")]
        # pd.set_option('display.max_rows', None)
        # programs=qs['AcademicProgramName'].unique()
        # programs=programs.tolist()
        # print(programs)
        data_list = []
        for _, row in qs.iterrows():
            year = row["Year"]
            rank = row["ClosingRank"]
            round = row["Round"]

            # Check if the program already exists in the data list
            year_dict = next((d for d in data_list if d["Year"] == year), None)
            if year_dict is None:
                # Create a new dictionary if the program doesn't exist
                year_dict = {"Year": year, "Rank": [], "Round": []}
                data_list.append(year_dict)

            # Append the closing rank to the program's rank list
            year_dict["Rank"].append(rank)
            year_dict["Round"].append(round)
        json_data = json.dumps(data_list)
        context = {
            "program_names": program_names,
            "json_data": json_data,
            "institute_names": institute_names,
        }
        return render(request, "josaa/RoundTrends.html", context)
    context = {"program_names": program_names, "institute_names": institute_names}
    return render(request, "josaa/RoundTrends.html", context)
