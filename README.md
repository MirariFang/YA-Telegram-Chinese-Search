# Yet Another Telegram Chinese search

This project implements Chinese search support for Telegram. Currently, our system only support searching histories using provided log files or new messages grabbed by a bot in a specific group chat.

 For more details about this project, please refer to our project report. 

## Prerequisite

- Python >= 3.6
- Java JDK 11
- Any Python virtual environment (recommended but not required)

## Setup

It is recommended to use our sample logs (in `/sample_logs`) for demo purpose instead of using the bot to grab your own chat histories from Telegram due to the privacy concerns. If you want to set up the Telegram bot and test with your own chat histories, please refer to the [Appendix](##Appendix). 

### Package installation

To install all the required packages, make sure you already have Python and JDK installed, and run

`sh setup.sh`

### Setup Tokenizer

To setup the tokenizer, run 

`sh start_server.sh`

### Setup web application server

To setup the web application locally, first go to the directory `/zh-search-web`

`cd zh-search-web`

Then, run

`flask run`

After it's been started, go to http://127.0.0.1:5000/search and enjoy searching! 

## Appendix

### Telgram Bot setup

To setup the Telegram bot to grab your own chat histories:

1. Apply for a Telegram API [here](https://my.telegram.org/app) 
2. Setup a bot account [here](https://t.me/BotFather). 
3. Get the group chat id of the group that you want your bot to grab histories from and add your bot to that group. You may want to follow the steps in this [Stack Overflow answer](https://stackoverflow.com/a/32572159/13737207)
4. Add your API id, API hash, bot token, and chat id to environment variables `API_ID`, `API_HASH`, `BOT_TOKEN`, and `CHAT_ID` respectively. You can also go to the file `bot.py` and modify the credentials at the beginning. 
5. Create a new directory `logs` here for storing the chat histories.
6. Run `python bot.py` to start the bot. It will automatically fetch any new messages in the group and store it as log files in `/logs`. 

You can refer to Telegram's official documentation [here](https://core.telegram.org/api) if you have any issues with Telegram. 
### Use your own chat histories for searching

Place your log files in `/sample_logs` and restart the tokenizer. Note that it should have the same format as the sample logs. 

## Contact

Mirari Fang - zf4@illinois.edu

## Acknowledgements

- [telegram-search](https://github.com/EYHN/telegram-search)
