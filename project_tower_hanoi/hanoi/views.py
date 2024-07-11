from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import solve_hanoi_to_file
import json
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'hanoi/index.html')

@csrf_exempt
def solve_puzzle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            num_disks = int(data.get('num_disks'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid input'}, status=400)
        
        if num_disks > 0:
            file_path = '/Users/davidsuta/Documents/CS50_WEB/project_tower_hanoi/hanoi/hanoi_moves/hanoi_moves.txt'
            solution = solve_hanoi_to_file(num_disks, file_path)
            return JsonResponse({'solution': solution})
        return JsonResponse({'error': 'Number of disks must be greater than 0'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

