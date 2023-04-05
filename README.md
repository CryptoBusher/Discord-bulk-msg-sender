## Script for sending scheduled messages in Discord chats
The script can send scheduled messages (f.e. every hour, every day, etc.) or one-time messages using specified delays. You can use it to submit your crypto wallets for whitelists, schedule GM/GN for specific chats, and farm !work/!daily shit in grind-based projects.

## Pros
1. Safe use of your Discord tokens with proxies and user agents
2. Randomisation of delays
3. Specific settings for each Discord account
4. Message randomisation (fe ['gm', 'GM MFERS', 'gm!', 'GM'])

## Cons
1. One-threaded, synchronous code

## Logics
1. User specifies accounts in the txt file
2. Script initializes accounts, in case of fail - saves data to the 'data/failed_accounts' folder
3. Script starts sending messages according to the delay, start on run and loop settings
4. If the loop is disabled - the account is deleted from the queue after sending the first message

## First start
1. Install python v 3.10.*


    `sudo apt update`
    `sudo apt install software-properties-common -y`
    `sudo add-apt-repository ppa:deadsnakes/ppa`
    `sudo apt install python3.10`
    `python3.10 --version`
    
1.1 Install Python PIP with 3.10


    sudo apt install python3-pip
    wget https://bootstrap.pypa.io/get-pip.py
    python3.10 get-pip.py
    python3.10 -m pip install --upgrade pip
    pip3.10 --version

2. Download the repo
3. Run cmd, navigate to the project folder
4. Run the command `python3.10 -m pip install -r requirements.txt` to install all required dependencies
5. Prepare data in the 'data/accounts.txt' file. 1 line = 1 account. Check the 'data/accounts_sample' file to see the correct format.
   1. custom_name_for_logs: choose any name, for logging purposes
   2. discord_token: discord token that can be obtained from the browser's Network tab
   3. http_proxy: proxy in format `http://username:password@host:port`
   4. useragent: any useragent
   5. discord_chat_id: id of the specific chat
   6. ['message1', 'message2', 'message3'.....]: list of messages, in case there is only 1 message - define it in the list as well (f.e. ['single_message'])
   7. min_delay_sec: min delay before sending the message in seconds
   8. max_delay_sec: max delay before sending the message in seconds
   9. start_on_the_run_True_or_False: set True if you wish the bot to send the first message without delays right after you run the script, and set False if you wish to use the delay before the first message
   10. loop_True_or_False: set True if you wish to send messages in the loop, set False if you wish to send only 1 message
6. Run the bot using the `python3.10 discord_bulk_msg_sender.py` command
7. Failed accounts can be found in the 'data/failed_accounts' folder
