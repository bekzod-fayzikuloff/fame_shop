[![Python](https://img.shields.io/badge/-Python-464646?style=for-the-badge&logo=Python)](https://www.python.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
## Fame Shop

``git clone https://github.com/bekzod-fayzikuloff/fame_shop.git``

## Запуск
```
Билд и первый запуск Docker образа осуществляется командой
Для того чтобы все миграции применились
```
``docker-compose --profile migrate up --build``

***
* Используются форматтеры и линтеры.
* Комментарии к коду
* Docker
* Провекра github action
* Возможность регистрации, входа и выхода пользователя
* Фильтрация товаров по тэгам
* Корзина как для авторизованных и так и для не авторизованных пользователей
* Оформления заказа
* Автоматическое использования информации о пользователе как помощь в оформлении заказа
* Просмотр истории осуществленных заказов
* Просмотр каждого товара
* Удобная корзина с подсчетом суммы и количества товаров с динамическим изменением

``envs/.env.example пример переменных окружения, переименуйте файла в .env/.env ``
и осущиствие запуск докер контейнера
