from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import subprocess
import git
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Initialize LINE bot
line_bot_api = LineBotApi(os.getenv('Channel_access_token'))
handler = WebhookHandler(os.getenv('Channel_secret'))

@csrf_exempt
def update_server(request):
    if request.method == 'POST':
        repo_path = '/home/chunkai/mysite/'
        repo = git.Repo(repo_path)

        try:
            repo.git.pull('origin', 'main')  # 使用repo.git.pull()代替origin.pull()

            # 執行makemigrations
            subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'], cwd=repo_path)

            # 執行makemigrations
            subprocess.check_call(['python', 'manage.py', 'makemigrations'], cwd=repo_path)

            # 執行migrate
            subprocess.check_call(['python', 'manage.py', 'migrate'], cwd=repo_path)

            return JsonResponse({'message': 'Updated PythonAnywhere and migrated successfully'}, status=200)
        except git.GitCommandError as e:
            return JsonResponse({'error': 'GitCommandError: {}'.format(e.stderr)}, status=500)
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': 'Error executing manage.py commands: {}'.format(e.output)}, status=500)
    else:
        return JsonResponse({'error': 'Wrong event type'}, status=400)
    
@csrf_exempt
def callback(request):
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.body.decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponse(status=400)

    return HttpResponse(status=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Echo the user's message
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )    
