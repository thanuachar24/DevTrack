import json
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Reporter, Issue

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # .../Project_DevTrack/devtrack
REPORTER_FILE = BASE_DIR / 'reporters.json'
ISSUE_FILE = BASE_DIR / 'issues.json'

@api_view(['GET', 'POST'])
def create_reporter(request: Request):
    # GET: return single reporter by ?id= or all reporters when no id provided
    if request.method == 'GET':
        reporter_id_str = request.query_params.get('id') if hasattr(request, 'query_params') else request.GET.get('id')
        try:
            with open(REPORTER_FILE, 'r') as file:
                reporters = json.load(file)
                if not isinstance(reporters, list):
                    reporters = []
        except (FileNotFoundError, json.JSONDecodeError):
            reporters = []

        if reporter_id_str is None:
            return Response({"reporters": reporters})

        try:
            reporter_id = int(reporter_id_str)
        except (TypeError, ValueError):
            return Response({"error": "Invalid reporter id"}, status=400)

        for r in reporters:
            if r.get('id') == reporter_id:
                return Response({"reporter": r})

        return Response({"error": "Reporter not found"}, status=404)

    # POST: create reporter (existing behavior)
    data = request.data
    try:
        with open(REPORTER_FILE, 'r') as file:
            reporters = json.load(file)
            if not isinstance(reporters, list):
                reporters = []
    except (FileNotFoundError, json.JSONDecodeError):
        reporters = []

    reporter_id = data.get('id')
    if reporter_id is None:
        return Response({"error": "Reporter ID is required"}, status=400)

    if any(str(item.get('id')) == str(reporter_id) for item in reporters):
        return Response({"error": "Reporter with this ID already exists"}, status=400)

    new_reporter = Reporter(
        id=data.get('id'),
        name=data.get('name'),
        email=data.get('email'),
        team=data.get('team')
    )

    new_reporter.validate()
    reporters.append(new_reporter.to_dict())
    with open(REPORTER_FILE, 'w') as file:
        json.dump(reporters, file, indent=4)

    return Response({"message": "Reporter created successfully", "reporter": new_reporter.to_dict()})

@api_view(['GET', 'POST'])
def create_issue(request: Request):
    # GET: support ?id=1 or ?status=open
    if request.method == 'GET':
        issue_id_str = request.query_params.get('id') if hasattr(request, 'query_params') else request.GET.get('id')
        status_q = request.query_params.get('status') if hasattr(request, 'query_params') else request.GET.get('status')
        reporter_id_str = request.query_params.get('reporter_id') if hasattr(request, 'query_params') else request.GET.get('reporter_id')
        try:
            with open(ISSUE_FILE, 'r') as file:
                issues = json.load(file)
                if not isinstance(issues, list):
                    issues = []
        except (FileNotFoundError, json.JSONDecodeError):
            issues = []

        if issue_id_str is not None:
            try:
                issue_id = int(issue_id_str)
            except (TypeError, ValueError):
                return Response({"error": "Invalid issue id"}, status=400)
            for it in issues:
                if it.get('id') == issue_id:
                    return Response({"issue": it})
            return Response({"error": "Issue not found"}, status=404)

        if reporter_id_str is not None:
            try:
                reporter_id = int(reporter_id_str)
            except (TypeError, ValueError):
                return Response({"error": "Invalid reporter_id"}, status=400)
            filtered = [it for it in issues if it.get('reporter_id') == reporter_id]
            return Response({"issues": filtered})

        if status_q is not None:
            filtered = [it for it in issues if str(it.get('status')).lower() == str(status_q).lower()]
            return Response({"issues": filtered})

        return Response({"issues": issues})

    # POST: create new issue
    data = request.data
    try:
        with open(ISSUE_FILE, 'r') as file:
            issues = json.load(file)
            if not isinstance(issues, list):
                issues = []
    except (FileNotFoundError, json.JSONDecodeError):
        issues = []

    issue_id = data.get('id')
    if issue_id is None:
        return Response({"error": "Issue ID is required"}, status=400)

    if any(str(item.get('id')) == str(issue_id) for item in issues):
        return Response({"error": "Issue with this ID already exists"}, status=400)

    new_issue = Issue(
        id=data.get('id'),
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status'),
        priority=data.get('priority'),
        reporter_id=data.get('reporter_id')
    )

    new_issue.validate()
    issues.append(new_issue.to_dict())
    with open(ISSUE_FILE, 'w') as file:
        json.dump(issues, file, indent=4)

    return Response({"message": "Issue created successfully", "issue": new_issue.to_dict()})

@api_view(['GET'])
def list_issues(request: Request):
    try:
        with open(ISSUE_FILE, 'r') as file:
            issues = json.load(file)
            if not isinstance(issues, list):
                issues = []
    except (FileNotFoundError, json.JSONDecodeError):
        issues = []

    return Response({
        "issues": issues
    })

@api_view(['GET'])
def list_reporters(request: Request):
    try:
        with open(REPORTER_FILE, 'r') as file:
            reporters = json.load(file)
            if not isinstance(reporters, list):
                reporters = []
    except (FileNotFoundError, json.JSONDecodeError):
        reporters = []

    return Response({
        "reporters": reporters
    })
