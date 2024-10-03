[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/fabrika/app?startapp=ref_2008453)
[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/CyberToolz)


# Бот для FriendsFactory



# 🔥🔥 Используйте Python версии 3.10 - 3.11.5 🔥🔥

> 🇪🇳 README in english available [here](README-EN)

## Функционал  
|                   Функционал              																	     | Поддерживается |
|:------------------------------------------------------------------------------------------------------------------:|:--------------:|
| Многопоточность																									 | 		 ✔️ 	  |
| Привязка прокси к сессии 																							 | 		 ✔️		  |
| Автопереадресация 																								 |		 ✔️       |
| Автоматический переход 																							 | 		 ✔️ 	  |
| Автоматический буст																								 | 		 ✔️		  |
| Автоматическое управление фабрикой (покупка рабочего, отправка рабочего на работу, требование компенсации рабочего)|		 ✔️ 	  |
| Автозадачи 																										 | 		 ✔️ 	  |
| Поддержка пирограммы .session            																	    	 |       ✔️       |

## [Настройки](https://github.com/Cybertat1on/FriendsFactory.git/blob/main/.env-example/)
|          Настройки           |                                 Описание                                               |
|:----------------------------:|:--------------------------------------------------------------------------------------:|
| **API_ID / API_HASH**    		   | Данные платформы, с которой будет запущена сессия Telegram (по умолчанию - android)|       
| **REF_LINK**            		   | Поместите сюда вашу реф-ссылку    (10% для меня)                                   |
| **AUTO_TASK=**                   | Автовыполнение задач (по умолчанию: True)                                          |
| **AUTO_TAP**            		   | Автоматическое нажатие для получения очков (по умолчанию: True)					|
| **AUTO_BOOST**           		   | Автоматическое использование полного заряда энергии (по умолчанию: True)           |
| **TAP_COUNT**           		   | Случайное количество касаний (по умолчанию: [30, 75])                              |
| **SLEEP_BY_MIN_ENERGY**   	   | Минимальное количество энергии для сна (по умолчанию: 100)                         |
| **SLEEP_BETWEEN_TAPS**    	   | Произвольное время сна между нажатиями (по умолчанию: [15, 30])                    |
| **AUTO_MANAGE_FACTORY**          | Автоматическое управление фабрикой (по умолчанию: True)                            |
| **AUTO_BUY_WORKER**      		   | Автоматическая покупка рабочих (по умолчанию: True)                                |
| **MAX_NUMBER_OF_WORKER_TO_BUY**  | Максимальное количество рабочих (без защиты) для покупки (по умолчанию: 3)         |
| **USE_PROXY_FROM_FILE**   	   | Использовать ли прокси из файла bot/config/proxies.txt (True / False)              |

## Быстрый старт 📚

Для быстрой установки и последующего запуска - запустите файл `run.bat` на **Windows** или `run.sh` на **Линукс**

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/release/python-3100/) **версии 3.10**

## Получение API ключей
1. Перейдите на сайт [**my.telegram.org**](https://my.telegram.org/auth) и войдите в систему, используя свой номер телефона.
2. Выберите `API development tools` и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.

## Установка
Вы можете скачать [**Репозиторий**](https://github.com/Cybertat1on/FriendsFactory.git) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
git clone https://github.com/Cybertat1on/FriendsFactory.git.git
cd BoinkersBot
```

Затем для автоматической установки введите:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux ручная установка
```shell
sudo sh install.sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
python3 main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/BoinkersBot >>> python3 main.py --action (1/2)
# Or
~/BoinkersBot >>> python3 main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


# Windows ручная установка
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/BoinkersBot >>> python main.py --action (1/2)
# Или
~/BoinkersBot >>> python main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```
# Termux ручная установка
```
> pkg update && pkg upgrade -y
> pkg install python rust git -y
> git clone https://github.com/Cybertat1on/FriendsFactory.git
> cd Fabrika-Friends-Factory
> pip install -r requirements.txt
> python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```termux
~/Fabrika-Friends-Factory > python main.py --action (1/2)
# Or
~/Fabrika-Friends-Factory > python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session 
```