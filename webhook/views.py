from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import subprocess
import git


# Initialize LINE bot
line_bot_api = LineBotApi('d8NLd76ri5tk87nHVatdlQxwbvmFzxN31DsEjSBz4A1wCC99dnSzcRbT7sia6b4iQBPbA3kXSbUKh/Mkc4d6j8eTFOsfA+Xs1FYq1DkyXAoJaoEX3gGZirKpTo5NQwoiOHDjBVbK7gNRXkfKUMqUPAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('da4d953d7bb43d3535148d3ee59e8668')

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
