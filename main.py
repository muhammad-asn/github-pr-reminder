import os
import requests
import yaml
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from github import Github, Auth

class NotificationChannel(ABC):
    @abstractmethod
    def send_notification(self, message):
        pass

class TelegramChannel(NotificationChannel):
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

        if not self.bot_token or not self.chat_id:
            raise ValueError("Telegram bot token and chat ID must be provided.")

    def send_notification(self, message):
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        requests.post(url, data=data)

github_token = os.getenv('GITHUB_TOKEN')
pending_pull_requests = []

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not github_token:
    raise ValueError("GitHub token not provided. Set the GITHUB_TOKEN environment variable.")

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

auth = Auth.Token(github_token)
github_client = Github(auth=auth)

# Calculate the date range for stale pull requests
DEFAULT_DAYS_RANGE = 7
SET_DAYS_RANGE = config.get('days_range', DEFAULT_DAYS_RANGE)
days_range = (datetime.now() - timedelta(days=SET_DAYS_RANGE)).strftime("%Y-%m-%d %H:%M:%S")

def parse_datetime(datetime_str):
    parsed_datetime = datetime.strptime(str(datetime_str), "%Y-%m-%d %H:%M:%S%z")
    formatted_datetime_str = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime_str

def send_notification(notification_channel, message):
    notification_channel.send_notification(message)

def list_pending_pull_requests(repo, notification_channel):
    try:
        org, repo_name = repo.split('/')
        repository = github_client.get_repo(f'{org}/{repo_name}')
        pull_requests = repository.get_pulls(state='open', sort="created")
        message_title = f"🕔 Pull Requests Reminder: last {SET_DAYS_RANGE} days \n"
        message_pending_title = f"🚨 **Pending Pull Requests:** 🚨 \n"
        message_repository_title = f"💻 Repository: <a href=\"{repository.url}\">{repo}</a>\n"
        message = ""
        counter = 1
        
        # Iterate through the pull requests
        for pr in pull_requests:
            created_at = parse_datetime(pr.created_at)

            threshold_date = datetime.strptime(days_range, "%Y-%m-%d %H:%M:%S")
            created_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

            if created_date > threshold_date:
                pending_pull_requests.append(pr.number)
            
            if len(pending_pull_requests) >= 1:
                message += f"{counter}. ⚠️{pr.title} - <a href=\"https://github.com/{repo}/pull/{pr.number}\">#{pr.number}</a>\n"
                counter += 1
        
        if not pending_pull_requests:
            message = f"{message_title}{message_repository_title}\n✅ There are no stale Pull Requests"
        else:
            message = f"{message_title}{message_repository_title}\n{message_pending_title}\n\n{message}"
            
        # Clear the list of stale pull request numbers for the next repository
        pending_pull_requests.clear()
        send_notification(notification_channel, message)
    
    except Exception as e:
        print(f"❌ Error processing repository '{repo}': {str(e)}")

def main():
    for repo in config.get('repos', []):
        if telegram_bot_token and telegram_chat_id:
            telegram_channel = TelegramChannel(telegram_bot_token, telegram_chat_id)
            list_pending_pull_requests(repo, telegram_channel)

if __name__ == "__main__":
    main()