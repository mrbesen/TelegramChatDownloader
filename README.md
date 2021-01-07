# THIS REPO IS DISCONTINUED [HERE IS THE LAST VERSION](https://git.mrbesen.de/MrBesen/TelegramChatDownloader)



### TelegramChatDownloader
A CLI program to download a chat from telegram.
##### How to install (linux only)
requirements:
* python3
* [telethon](https://github.com/LonamiWebs/Telethon)
* [TelegramAPI-ID](https://core.telegram.org/api/obtaining_api_id)
install requirements:
```
sudo apt install python3-pip git
pip3 install telethon
```
get the downloader:
```git clone https://github.com/mrbesen/TelegramChatDownloader.git```
open the file telegramApi.py and enter your API ID, token and username.

Then run:
```
cd TelegramChatDownloader/
./telegramApi.py
```
##### Output Format
The chat structure is stored as "chat.xml" in the folder "out/"
All Media-files are Stored in the Folder out/media/

Stickers get downloaded too, but they wont get a file-postfix.
They are stored in the [WEBP](https://de.wikipedia.org/wiki/WebP) format.
