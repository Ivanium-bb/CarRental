## Запуск и проверка:

#### Запуск приложения:

``` $ docker-compose up ```

#### Запуск тестов:

``` $ docker exec -it carrental_web_1 python manage.py test ```

## Проверка доступности автомобиля:

###     

    curl --location --request GET 'http://127.0.0.1:8000/api/v1/available/1/' 

## Расчёт стоимости на определённый период:

###   

    curl --location --request POST 'http://127.0.0.1:8000/api/v1/price/' \
    --form 'session_start="2021-04-02"' \
    --form 'session_finish="2021-03-31"'

## Создание сессии аредны автомобиля:

###   

    curl --location --request POST 'http://127.0.0.1:8000/api/v1/session/' \
    --form 'session_start="2023-03-27"' \
    --form 'session_finish="2023-03-28"' \
    --form 'car="1"'


## Получение статистики:

###   

    curl --location --request GET 'http://127.0.0.1:8000/api/v1/statistic/' 
