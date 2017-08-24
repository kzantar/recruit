# Проверочное задание

## Задача

давайте возьмем фиктивный метод, который принимает на вход
логин
пароль
некий тип модели benefitType
и ряд параметров ключ-значение в JSON - до 1000, так что их скорее всего логично передавать в content
через post-запрос. Пока пусть это будут параметры a,b,c

В БД (mariadb) хранятся:
login
password
пользователя и для каждого пользователя набор моделей (dataSets)

При вызове метода(логин, пароль, benefitType) c параметрами JSON a,b,c 
после авторизации пользователя должны возвращаться результаты расчета всех моделей, которые у этого пользователя есть, 
с подстановкой параметров benefitType и a,b,c

Для примера возьмем трех пользователей (логины и пароли можете сами им назначить).

У первого пользователя 1 модель (a+b+c)*benefitType
У второго пользователя 2 модели (a+b)*benefitType и (b+c)*benefitType
У третьего пользователя 3 модели a*benefitType и (b+c) и c*benefitType

Нужно обернуть этот метод и сделать из него API подняв веб-сервер на tornado


## Решение

```
# Установим зависимости
$ pip install -r requirements.txt

# Запустим MariaDB
docker run --name mariadb-server -d -p 3000:3306  -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=recruit mariadb

# Заполним тестовые данные
python models.py

# Старт сервера
python main.py

# Тестирование

http -a user_1:pass -f POST :8080 benefitType=2.5 params='{"a": 1, "b":2, "c":10}'
http -a user_2:pass -f POST :8080 benefitType=2.5 params='{"a": 1, "b":1, "c":1}'
http -a user_3:pass -f POST :8080 benefitType=a params='{"a": 1, "b":1, "c":1}'
http -a user_3:pass -f POST :8080 benefitType=1.5 params='{"a": "abc", "b": 1, "c": 1}'
http -a user_4:pass -f POST :8080 benefitType=1.5 params='{"a": 2, "b": 1, "c": 1}'
```
