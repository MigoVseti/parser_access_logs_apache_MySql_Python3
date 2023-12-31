# Apache Access Log Parser

Это парсер журналов доступа Apache на основе Python, который может анализировать журналы доступа как принудительно, так и с помощью cron. Разобранные записи добавляются в базу данных MySql с помощью SQLAlchemy.

## Установка

Перед использованием парсера журналов доступа Apache убедитесь, что у вас установлены следующие библиотеки:

- Flask
- SQLAlchemy
- pymysql

Вы можете установить эти библиотеки с помощью pip:

pip install Flask SQLAlchemy pymysql

## Использование

Чтобы использовать парсер журналов доступа Apache, выполните следующие действия:

1. Клонируйте репозиторий на вашу локальную машину:

git clone https://github.com/your-username/apache-access-log-parser.git

2. Перейдите в каталог:

cd apache-access-log-parser

3. Отредактируйте файл config.json, указав параметры подключения к базе данных, а также хост и порт API.

4. Запустите приложение Flask:

python parser.py

5. Откройте веб-браузер и перейдите по адресу http://localhost:5000/logs для просмотра журналов.

Вы также можете получить сгруппированные журналы, перейдя по адресу http://localhost:5000/logs/grouped и указав параметры group_by, sort_by и sort_order в URL.

## Вклад

Вклад в парсер журналов доступа Apache приветствуется! Чтобы внести свой вклад, сделайте форк репозитория и создайте pull request.
