<h1> Проект Web/Mobile + API тестирования видеоплатформы и стримингово сервиса VK Видео </h1>

----
> <code><img width="1%" title="VK Видео" src="images/vklogo.png"></code> <a target="_blank" href="https://vkvideo.ru/">VK Видео</a>

![This is an image](images/vkvideo.png)

----
<!-- Технологии -->

## Используемые технологии
<p  align="center">
    <code><img width="5%" title="Python" src="images/python.png"></code>
    <code><img width="6%" title="Selene" src="images/selene.png"></code>
    <code><img width="5%" title="Pytest" src="images/pytest.png"></code>
    <code><img width="5%" title="Browserstack" src="images/browserstack.png"></code>
    <code><img width="5%" title="Jenkins" src="images/jenkins.png"></code>
    <code><img width="5%" title="Allure Report" src="images/allure_report.png"></code>
    <code><img width="4.5%" title="Selenium" src="images/selenium.png"></code>
    <code><img width="5%" title="Allure TestOps" src="images/allure_testops.png"></code>
    <code><img width="5%" title="Android Studio" src="images/android_studio.png"></code>
    <code><img width="5%" title="Jira" src="images/jira.png"></code>
    <code><img width="5%" title="Telegram" src="images/tg.png"></code>
    <code><img width="7.5%" title="Appium" src="images/appium.png"></code>
    <code><img width="4%" title="Requests" src="images/requests.png"></code>
    <code><img width="5%" title="Github" src="images/Github.png"></code>

</p>

----
<!-- Тест кейсы -->
UI (11):

* ✅ Проверка заголовка главной страницы
* ✅ Проверка breadcrumbs:
  * Подборка Технологии (+ инфо по первому видео)
  * Подборка Путешествия (+ инфо по первому видео)
* ✅ Проверка работы навигации:
  * Переход в раздел Музыка (+ инфо по первому видео)
  * Переход в раздел Детям → Развивашки (+ инфо по первому видео)
  * Переход в раздел Политика → Популярное (+ инфо по первому видео)
  * Переход в раздел Фильмы и сериалы → Фантастика (+ инфо по первому видео)
* ✅ Комбинированный тест навигация + breadcrumbs:
  * Отобразить скрытые разделы навигации: Развернуть → Интерактив → От сообществ (+ инфо по первым пяти интерактивам)
* ✅ Проверка работоспособности поисковой строки:
  * Поиск на примере 3х разных запросов (+ инфо по первому видео из каждого запроса)
  * Поиск по запросу и проверка работоспособности фильтров (+ инфо по первым пяти видео)
* ✅ Поиск видео по запросу → Воспроизведение видео → Проверка управления плеером с клавиатуры (+ инфо по видео)

 API (6):
* ✅ Получение ифнормации о главной странице
* ✅ Проверка breadcrumbs:
  * Подборка Еда (+ инфо по первым 10 видео)
  * Подборка Авто (+ инфо по первым 10 видео)
* ✅ Проверка работы навигации:
  * Переход в раздел Детям → Рекомендации (+ инфо по первым 10 видео)
  * Переход в раздел Музыка → Главные новинки (+ инфо по первым 5 видео)
  * Переход в раздел Политика →
      * Подпобка Шоу (+ инфо по первым 5 видео)
      * Подпобка Новости (+ инфо по первым 5 видео)
      * Подпобка Интервью (+ инфо по первым 5 видео)
      * Подпобка Популярное (+ инфо по первым 5 видео)
      * Подпобка Документальное (+ инфо по первым 5 видео)

<!--  -->

----
## Локальный запуск автотестов
#### Для запуска API тестов необходима предварительная настройка 
> [!NOTE]
> Открыть запрос выполнив клик по любой активной кнопке на Web интерфейсе `VK Видео` в режиме `DevTools (F12) → Network → Headers`

####  `Headers` должен содержать:
```bash
Request Method:   POST 
Status Code:      200 OK
```
#### <img width="70%" title="DevTools" src="images/api_post.png">

#### Переключаемся в `Network` → `Payload`
#### <img width="100%" title="DevTools" src="images/api_key.png">

#### Копируем 
```bash
V = "5.280"
CLIENT_ID = "Ваш ID"
ACCESS_TOKEN = "Ваш TOKEN"
```
#### Их необходимо указать в файле конфигурации `tests → api → conftest.py`

----

### Рекомендуемые параметры запуска

```bash
>  pytest .\tests\ --alluredir=allure-results -v -s   
```
### Построение Allure-отчета

```bash
>  allure generate allure-results -o allure-report --clean

>  allure open allure-report
```

### Перед повторным запуском выполнить
```bash
> Remove-Item -Recurse -Force allure-results, allure-report -ErrorAction SilentlyContinue
```
----
<!-- Allure report -->
# <img width="3%" title="Allure Report" src="images/allure_report.png"> Allure report

##### Результаты выполнения тестова можно посмотреть в Allure-отчете
![This is an image](images/allure_reports.png)
![This is an image](images/allure_int.png)
![This is an image](images/allure_graph.png)

----
<!-- Jenkins -->

### <img width="3%" title="Jenkins" src="images/jenkins.png"> Запуск проекта в Jenkins

### [Задача в jenkins](https://jenkins.autotests.cloud/job/Okko-reqres-project/)

----
<!-- Allure TestOps -->

### <img width="3%" title="Allure TestOps" src="images/allure_testops.png"> Интеграция с Allure TestOps

### [Dashboard](https://allure.autotests.cloud/project/4221/dashboards)

![This is an image](images/allure_testops_dash.jpg)

----
<!-- Jira -->

### <img width="3%" title="Jira" src="images/jira.png"> Интеграция с Jira

![This is an image](images/jira_okko.jpg)

----
<!-- Telegram -->

### <img width="3%" title="Telegram" src="images/tg.png"> Оповещения в Telegram
##### После выполнения тестов, в Telegram bot приходит сообщение с графиком и информацией о тестовом прогоне.

![This is an image](images/bot_mobile_result.png)
![This is an image](images/bot_api_result.png)
