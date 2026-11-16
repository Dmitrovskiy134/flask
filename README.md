# Домашнее задание «Flask» — REST API объявлений

## Содержание

- `app.py` — Flask-приложение с SQLite для обязательного задания №1
- `test_api.py` — автоматические проверки API
- `requirements.txt` — зависимости
- `ads.db` — создаётся автоматически при первом запуске

## Запуск

В терминале в папке проекта:

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Если PowerShell запрещает активацию, можно обойти её:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

На Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Сервер доступен на `http://127.0.0.1:5000`.

## API

| Метод | URL | Действие |
|---|---|---|
| POST | `/ads` | Создать |
| GET | `/ads` | Получить список |
| GET | `/ads/1` | Получить по id |
| PATCH | `/ads/1` | Изменить заголовок и/или описание |
| DELETE | `/ads/1` | Удалить |

### POST /ads

```json
{
  "title": "Ремонт холодильников",
  "description": "Выезд на дом",
  "owner": "Денис"
}
```

Возвращает `201 Created`, уникальный `id` и `created_at` в UTC.

### PATCH /ads/1

```json
{"description": "Быстрый выезд"}
```

Возвращает `200 OK` и обновлённое объявление. Владельца и дату менять нельзя.

### DELETE /ads/1

Возвращает `204 No Content` без тела ответа.

## Тестирование

```bash
python -m unittest -v
```

Все запросы можно выполнять в Postman, выбрав соответствующий HTTP-метод,
Body → raw → JSON. Для получения объявления в браузере откройте
`http://127.0.0.1:5000/ads`.

## Замечание по необязательному заданию №2

Авторизации **нет**. Поле `owner` приходит от клиента и поэтому пока не защищено
от подмены. Для №2 понадобятся таблица пользователей, хэширование паролей,
аутентификация и проверка совпадения владельца с авторизованным пользователем.

Не включайте `debug=True` на публичном сервере.


## Проверка в Windows PowerShell (без Postman)

Оставьте Flask запущенным в первом терминале PyCharm. Во втором терминале:

```powershell
$body = '{"title":"Ремонт холодильников","description":"Выезд на дом","owner":"Денис"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/ads" -Method Post `
  -ContentType "application/json; charset=utf-8" `
  -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
```

Номер `id` возьмите из ответа сервера. Для проверки одного объявления
откройте в браузере `http://127.0.0.1:5000/ads/1`, заменив `1` на полученный ID.

## Отправка преподавателю

Загрузите в репозиторий файлы `app.py`, `requirements.txt`, `README.md`,
`test_api.py` и `.gitignore`. Файл `ads.db` и папку `.venv` в репозиторий
добавлять не нужно. Если в README исходного репозитория Нетологии указан
другой способ сдачи или структура папок, соблюдайте именно его.

**В объём решения входит только обязательное задание №1.**
