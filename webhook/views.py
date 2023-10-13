from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse, JsonResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from django.views.decorators.csrf import csrf_exempt
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
    # 獲取 X-Line-Signature 頭部值
    signature = request.headers['X-Line-Signature']

    # 獲取請求主體作為文本
    body = request.body.decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponse(status=400)

    # 獲取 LINE ID
    line_id = event.source.user_id

    # 檢查是否已有該 LINE ID 的用戶
    user = get_user_model().objects.filter(line_id=line_id).first()

    # 如果用戶不存在，創建一個新的用戶
    if not user:
        user = get_user_model().objects.create_user(
            username=line_id,  # 使用 LINE ID 作為用戶名
            line_id=line_id
        )

    # 登入該用戶
    login(request, user)

    return HttpResponse(status=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Echo the user's message
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )    
