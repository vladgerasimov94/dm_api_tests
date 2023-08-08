# Проект для тестирования сервиса "dm_api_account"


### Ответственные лица:

* Герасимов Владислав:
  * [telegram](https://t.me/dogen108)

  

### Тестируемый сервис:
**dm_api_account**
* Swagger: [swagger](http://5.63.153.31:5051/index.html?urls.primaryName=Account)


### Установка и запуск
```shell
 git clone https://github.com/vladgerasimov94/dm_api_tests
 cd dm_api_tests
 pip install -r requirements.txt
```

### Docker
```shell
docker build -t dm_api_tests . 
docker run -it --rm dm_api_tests
```

### Различия в ветках фреймворка
В ветке main - фреймворк, который включает в себя все вспомогательные библиотеки.  
В ветке client - фреймворк, из которого вынесены вспомогательные библиотеки.  
В ветке client_gen - фреймворк, где клиент account и login сгенерированы, а так же сгенерирован клиент из gRPC модели.  

### Используемые технологии
<p  align="center">
  <code><img width="5%" title="Pycharm" src="images/logo_stacks/pycharm.png"></code>
  <code><img width="5%" title="Python" src="images/logo_stacks/python.png"></code>
  <code><img width="5%" title="Pytest" src="images/logo_stacks/pytest.png"></code>
  <code><img width="5%" title="Postman" src="images/logo_stacks/postman.png"></code>
  <code><img width="5%" title="Docker" src="images/logo_stacks/docker.png"></code>
  <code><img width="5%" title="Requests" src="images/logo_stacks/requests.png"></code>
  <code><img width="5%" title="GitHub" src="images/logo_stacks/github.png"></code>
  <code><img width="5%" title="Allure Report" src="images/logo_stacks/allure_report.png"></code>
  <code><img width="5%" title="gRPC" src="images/logo_stacks/grpc.png"></code>
  <code><img width="5%" title="OpenApi" src="images/logo_stacks/openapi.png"></code>
</p>

### Архитектура проекта

```
 ├── config                     # Папка со всей конфигурацией проекта
 │   ├── prod.yml                # Настройки для прода
 │   └── server.yml              # Настройки для тестовой среды
 │   └── stg.yml                 # Настройки для локальной тестовой среды
 ├── data                        # Папка для констант и статических тестовых данных
 │   └── post_v1_account.py      # Файл с константами для метода создания аккаунта
 ├── apis                        # Папка для констант и статических тестовых данных
 │   ├── dm_api_account          # REST клиент для работы с dm_api_account
 │   ├── dm_api_forum            # REST клиент для работы с dm_api_forum
 │   ├── dm_api_search           # gRPC клиент для работы с search API
 │   └── dm_api_search_async     # Асинхронный gRPC клиент для работы с search API
 ├── common_libs                 # Папка для констант и статических тестовых данных
 │   ├── db_client               # Клиент с логгированием для работы с базой данных
 │   ├── orm_client              # Клиент с логгированием для работы с базой данных через ORM
 │   └── rest_client             # Клиент с логгированием для работы REST API
 ├── generic                     # Папка с базовыми специфичными для проекта проверочными и вспомогательными классами и функциями
 │   ├── helpers                 # Папка для вспомогательного функционала общего назначения 
 │   │   ├── account.py          # Помощник для работы с account_api
 │   │   ├── forum.py            # Помощник для работы с forum_api
 │   │   ├── dm_db.py            # Помощник для работы с базой данных
 │   │   ├── login.py            # Помощник для работы с login_api
 │   │   ├── mailhog.py          # Помощник для работы с почтовым сервером
 │   │   ├── search.py           # Помощник для работы с gRPC сервисом
 │   │   ├── orm_models.py       # ORM модели для работы с базой данных
 │   │   └── orm_db.py           # Помощник для работы с базой данных используя ORM
 │   ├── assertions              # Папка для проверок
 │   │   └── post_v1_account.py  # Файл содержит assert-ы для метода post_v1_account
 ├── services                    # Папка в которой хранятся фасады для работы с API
 │   └── dm_api_account          # Фасад, который объединяет API и классы помощники
 ├── tests                       # Папка для хранения тестов
 │   ├── test_account            # Папка с тестами для account_api
 │   ├── tests_login             # Папка с тестами для login_api
 │   └── test_search             # Папка с тестами для search gRPC API
 ├── .gitignore                  # Стандартный файл для игнорирования нежелательных файлов для загрузки в репозиторий
 ├── conftest.py                 # Файл с инициализацией настроек и фикстур
 ├── requirements.txt            # Файл с зависимостями
 └── README.md                   # Файл с описанием репозитория для тестов
```
### В файле config настраиваются окружения и выносятся основные подключения.
![This is an image](images/screenshots/config.png)



### <img width="3%" title="Allure Report" src="images/logo_stacks/allure_report.png"> Allure report
##### После прохождения тестов, результаты можно посмотреть в генерируемом Allure отчете.
![This is an image](images/screenshots/allure-report.png)

##### Во вкладке Graphs можно посмотреть графики о прохождении тестов, по их приоритезации, по времени прохождения и др.
![This is an image](images/screenshots/allure-graphs.png)

##### Во вкладке Suites находятся собранные тест кейсы, у которых описаны шаги и добавлены логи.
![This is an image](images/screenshots/allure-suites.png)


