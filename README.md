Gmail to Telegram (ENG)

Gmail to Telegram (ENG)
===========================
This program connects your Google Mail with Telegram.
It works using standard Google and Telegram libraries.

To install dependencies:

pip install -r requirements.txt

BUT before doing this — open the requirements.txt file first.


Telegram
-----------------
To create a Telegram bot:
It’s better to check the internet for a full guide, but the hint is: @BotFather.

To determine which channel to use, run test_telegram.py.


Google Console
-----------------
Working with Google is a bit more complicated:

Go to console.cloud.google.com and create your own “application”.

Navigate to:
Google Cloud Console → APIs & Services → +Enable API and Services → Gmail API → Enable

Then go to Manage → Credentials → +Create credentials

Open your newly created project, click Add secret, and find the button to Download JSON.
Make sure to download the JSON file!

Rename the downloaded file to credentials.json and then run test_gmail.py or main.py.

If everything is correct, logs will show that an authorization key was created and saved as token.json.
Make sure this file appears. Then check again by running test_gmail.py.
If your console shows a list without errors — everything is working properly.

From time to time token in token.json is expired. Programm automaticly request new token and save it to token.json.
You can see it in logs





Gmail to Telegram (RUS)
===========================
Эта программа сделана для соеденения почты Google и Telegram
Работает на стандартных библиотеках Google и Telegram:

Чтобы установить зависимости:
- pip install -r requirements.txt

НО прежде чем делать это - сначала зайдте в сам файл requirements.txt


Telegram
-----------------
Для того чтобы создать бота в телеграме:
лучше спросить у интернета, но подсказка: @BotFather

Для того чтобы понять какой канал: воспользуйтесь test_telegram.py


Google Console
-----------------
С гуглом немного посложнее:
Вам необходимо создать свою "программу" в Console.cloud.google.com
Выбрать Зайти на сайт Console Google Cloud -> APIs & services -> +Enable API and Services -> Gmail API -> 
И там должна быть кнопка enable или типа того. Далее заходите также и нажимаете Manage ->
Credentials -> +Create credentials -> Потом заходим в свой названный проект и +Add secret и там будет кнопка Save json file
Обязательно её найдите и скачайте файл json!!!
Далее переименовать его нужно в credentials.json и запустить test_gmail.py или main.py

Смотрите - в логах должно отоброжаться что создался ключ авторизации и сохранился в token.json - также у вас появился
этот файл -> проверяйте ещё раз в text_gmail.py - если появляется в консоли список без ошибок - всё работает

Время от времени токен в token.json перестаёт действовать и программа сама запрашивает новый. Это видно по логам