from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

tasks = [
    {"id": 1, "name": "Task 1", "completed": False},
    {"id": 2, "name": "Task 2", "completed": True},
]

@require_http_methods(["GET"])
def index(request):
    return JsonResponse({"tasks": tasks})
  
@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    data = json.loads(request.body)
    new_task = {
        "id": len(tasks) + 1 , 
        "name": data['name'],
        "completed": data.get("completed", False)
    }
    tasks.append(new_task)
    return JsonResponse(new_task, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete(request):
    if not request.body:
        return JsonResponse({"error": "No data provided"}, status=400)

    data = json.loads(request.body)
    task_id = data.get('id')

    if not isinstance(task_id, int):
        return JsonResponse({"error": "ID must be a number"}, status=400)

    task_exists = any(task['id'] == task_id for task in tasks)
    
    if not task_exists:
        return JsonResponse({"error": "Task not found"}, status=404)


    tasks[:] = [task for task in tasks if task['id'] != task_id]
    return JsonResponse({"message": "task deleted sucessfully!"}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def edit(request):
    if not request.body:
        return JsonResponse({"error": "No data provided"}, status=400)

    data = json.loads(request.body)
    task_id = data.get('id')
    new_name = data.get('name')

    if not isinstance(task_id, int):
        return JsonResponse({"error": "ID must be a number"}, status=400)

    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task:
        task['name'] = new_name
        return JsonResponse({"message": "task edit sucessfully!"}, status=201)

    else:
        return JsonResponse({"error": "Task not found"}, status=404)


