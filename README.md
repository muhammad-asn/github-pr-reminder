# Github Pull Requests (PR) Reminder
Stay organized and on top of Github pull requests. Simplify your workflow, never forget a PR. For devs, PMs, and more.

## Prerequisites

Before you can use this script, you'll need the following:

- Python >= 3.9 installed on your system.
- A Telegram bot created using BotFather on the Telegram platform.
- The API token of your Telegram bot.
- The chat ID of the user or group where you want to send messages.

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/muhammad-asn/github-pr-reminder.git
   ```

2. Change into the project directory:

   ```bash
   cd github-pr-reminder
   ```

3. Install the required Python libraries using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Set `.env` value

   ```python
    export GITHUB_TOKEN='g_XXXXX'
    export TELEGRAM_BOT_TOKEN='1xxxx:XXXX'
    export TELEGRAM_CHAT_ID='-10XXXXXX'
   ```

5. Adjust the `config.yaml` value
   ```yaml
   kind: GithubPullRequestsReminder
   repos:
     - muhammad-asn/efk-nginx
     - muhammad-asn/terraform-provider-idcloudhost-s3
   days_range: 180 #default 7 days
   ```

6. Run the script to send a message to your Telegram bot:
   ```bash
   python send_message.py
   ```

7. Check your Telegram chat to see the message from the bot.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request.
