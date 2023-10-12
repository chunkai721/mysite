from django.shortcuts import render

# Create your views here.
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import git

@csrf_exempt
def update_server(request):
    if request.method == 'POST':
        repo_path = '/home/chunkai/mysite/'
        repo = git.Repo(repo_path)

        try:
            repo.git.pull('origin', 'main')  # 使用repo.git.pull()代替origin.pull()

            # 執行makemigrations
            subprocess.check_call(['python', 'manage.py', 'makemigrations'], cwd=repo_path)

            # 執行migrate
            subprocess.check_call(['python', 'manage.py', 'migrate'], cwd=repo_path)

            return JsonResponse({'message': 'Updated PythonAnywhere and migrated successfully'}, status=200)
        except git.GitCommandError as e:
            return JsonResponse({'error': 'GitCommandError: {}'.format(e.stderr)}, status=500)
        except subprocess.CalledProcessError:
            return JsonResponse({'error': 'Error executing manage.py commands'}, status=500)
    else:
        return JsonResponse({'error': 'Wrong event type'}, status=400)


