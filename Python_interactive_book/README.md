## Интерактивная книга по Python (ООП)

Курс на Django с серверными шаблонами. Код выполняется в браузере (Pyodide). Контент уроков и задания управляются через админку.

### Возможности
- Авторизация на обложке
- 6–7 уроков по ООП (теория + практика)
- Встроенный интерпретатор (Pyodide)
- Очки, эмоции персонажа, конфетти, отметка пройденных глав
- Личный кабинет с прогрессом
- PDF-сертификат по завершению
- Админка для редактирования уроков и заданий

## Требования
- Windows 10/11
- Python 3.12+
- PowerShell

## Установка и запуск (Windows)
1) Перейдите в каталог проекта:

```powershell
Set-Location -LiteralPath 'D:\My_Pet_Projects\Python_interactive_book'
```

2) Создайте venv и установите зависимости:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install django==5.0.4 reportlab==4.2.5
```

3) Примените миграции и запустите сервер:

```powershell
python manage.py migrate
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/` — увидите обложку (вход/регистрация).

## Наполнение контента через админку
1) Создайте суперпользователя:

```powershell
python manage.py createsuperuser
```

2) Зайдите в `http://127.0.0.1:8000/admin/` → раздел Lessons:
- Заполните: `title`, `slug`, `order`, `theory_html`, `starter_code`, (опц.) `tests_inline`
- Добавьте один или несколько `Task` с `points` (очки за урок = сумма points)

Рекомендации:
- `theory_html`: можно использовать HTML/картинки
- `starter_code`: стартовый шаблон решения для редактора на странице урока

## Автосоздание 7 уроков ООП (без админки)
Добавлен management command, который сам создаёт/обновляет 7 уроков и задания к ним.
Команда заполняет поля моделей `Lesson` и `Task`:
- `Lesson`: `title`, `slug`, `order`, `chapter`, `theory_html`, `starter_code`, `tests_inline`
- `Task`: `lesson`, `prompt`, `points`

Запуск:

```powershell
Set-Location -LiteralPath 'D:\My_Pet_Projects\Python_interactive_book'
.\.venv\Scripts\Activate.ps1
python manage.py seed_oop_lessons
```

Поведение:
- если урока с таким `slug` нет — он создаётся;
- если уже есть — данные урока обновляются;
- для каждого урока создаётся/обновляется одно задание (`Task`).

### Пример `theory_html` (готов к вставке в админку)
```html
<section style="line-height:1.65;">
  <h2 style="margin-top:0;">Наследование в Python</h2>
  <p>
    <strong>Наследование</strong> — это механизм, при котором новый класс (дочерний)
    получает свойства и методы существующего класса (родительского).
  </p>

  <h3>Зачем это нужно?</h3>
  <ul>
    <li>Переиспользование кода</li>
    <li>Упрощение структуры программы</li>
    <li>Расширение поведения без дублирования</li>
  </ul>

  <h3>Пример</h3>
  <pre style="background:#0f172a;color:#e2e8f0;padding:12px;border-radius:8px;overflow:auto;"><code>class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "woof"

class Cat(Animal):
    def speak(self):
        return "meow"

print(Dog().speak())  # woof
print(Cat().speak())  # meow</code></pre>

  <h3>Мини-практика</h3>
  <p>
    Создайте класс <code>Bird</code>, унаследуйте его от <code>Animal</code>
    и верните из <code>speak()</code> строку <code>"tweet"</code>.
  </p>
</section>
```

## Модели и как их заполнять

### `Lesson` (основной контент урока)
Отвечает за страницу урока: теория, стартовый код, тесты.

Поля:
- `title` — название урока
- `slug` — уникальный URL (латиница, через дефис), например `oop-class-object`
- `order` — порядок в оглавлении (1, 2, 3...)
- `chapter` — раздел (например `ООП`)
- `theory_html` — теория в HTML
- `starter_code` — код, который студент видит в редакторе
- `tests_inline` — JSON со строгими тестами (исполняются в браузере через Pyodide)

Как заполнять:
- Заполняйте вручную в админке `Lessons`.
- `slug` уникальный, не меняйте без необходимости (сломаются ссылки).
- `tests_inline` должен быть валидным JSON.

### `Task` (задачи урока)
Отвечает за текст задания и очки.

Поля:
- `lesson` — связь с уроком
- `prompt` — условие задачи
- `points` — очки за задачу

Как заполнять:
- Добавляйте через inline внутри `Lesson`.
- Если задач несколько, очки урока = сумма `points` всех задач.

### `ChapterProgress` (прогресс пользователя по уроку)
Отвечает за факт прохождения конкретного урока конкретным пользователем.

Поля:
- `user`, `lesson`
- `is_completed`
- `best_score`
- `completed_at`

Как заполнять:
- Обычно не вручную. Заполняется автоматически при отправке решения.

### `UserProfile` (сводка по пользователю)
Отвечает за агрегаты в личном кабинете.

Поля:
- `user`
- `total_points`
- `completed_percent`

Как заполнять:
- Не вручную. Пересчитывается автоматически из `ChapterProgress`.

### `Submission` (история попыток)
Отвечает за лог всех отправок кода.

Поля:
- `user`, `lesson`
- `code`
- `is_success`
- `output`
- `created_at`

Как заполнять:
- Не вручную. Создаётся автоматически кнопкой «Отправить».

## Готовые данные для заполнения (7 уроков)

Ниже — конкретные значения, которые можно сразу внести в админку.

### 1) Lesson
- `title`: Класс и объект
- `slug`: oop-class-object
- `order`: 1
- `chapter`: ООП
- `starter_code`:
```python
class Dino:
    # TODO: добавь __init__(self, name)
    # TODO: метод speak(self), возвращающий строку "I am <name>"
    pass
```
- `tests_inline`:
```json
{
  "functionTests": [
    {
      "function": "Dino",
      "cases": [
        {"args": ["Rex"], "expected": null}
      ]
    }
  ],
  "expectedStdout": null
}
```
- `Task.prompt`: Создайте класс `Dino` с `__init__` и `speak()`.
- `Task.points`: 10

### 2) Lesson
- `title`: Инкапсуляция
- `slug`: oop-encapsulation
- `order`: 2
- `chapter`: ООП
- `starter_code`:
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    # TODO: get_balance()
    # TODO: deposit(amount)
```
- `tests_inline`:
```json
{
  "functionTests": [],
  "expectedStdout": null
}
```
- `Task.prompt`: Реализуйте `get_balance()` и `deposit(amount)` для класса `BankAccount`.
- `Task.points`: 10

### 3) Lesson
- `title`: Наследование
- `slug`: oop-inheritance
- `order`: 3
- `chapter`: ООП
- `starter_code`:
```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    # TODO: переопредели speak() -> "woof"
    pass
```
- `tests_inline`:
```json
{
  "functionTests": [],
  "expectedStdout": null
}
```
- `Task.prompt`: Создайте наследника `Dog` и переопределите `speak()`.
- `Task.points`: 10

### 4) Lesson
- `title`: Полиморфизм
- `slug`: oop-polymorphism
- `order`: 4
- `chapter`: ООП
- `starter_code`:
```python
class Cat:
    def sound(self):
        return "meow"

class Cow:
    def sound(self):
        return "moo"

def make_sound(animal):
    # TODO
    pass
```
- `tests_inline`:
```json
{
  "functionTests": [
    {
      "function": "make_sound",
      "cases": [
        {"args": [{"sound": null}], "expected": null}
      ]
    }
  ],
  "expectedStdout": null
}
```
- `Task.prompt`: Реализуйте `make_sound(animal)`, вызывая полиморфный метод `sound()`.
- `Task.points`: 10

### 5) Lesson
- `title`: Абстракция
- `slug`: oop-abstraction
- `order`: 5
- `chapter`: ООП
- `starter_code`:
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    # TODO
    pass
```
- `tests_inline`:
```json
{
  "functionTests": [],
  "expectedStdout": null
}
```
- `Task.prompt`: Реализуйте `Rectangle` и метод `area()`.
- `Task.points`: 10

### 6) Lesson
- `title`: Dunder-методы
- `slug`: oop-dunder-methods
- `order`: 6
- `chapter`: ООП
- `starter_code`:
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # TODO: __add__
    # TODO: __str__
```
- `tests_inline`:
```json
{
  "functionTests": [],
  "expectedStdout": null
}
```
- `Task.prompt`: Реализуйте `__add__` и `__str__` у `Vector`.
- `Task.points`: 10

### 7) Lesson
- `title`: Композиция
- `slug`: oop-composition
- `order`: 7
- `chapter`: ООП
- `starter_code`:
```python
class Engine:
    def start(self):
        return "engine started"

class Car:
    def __init__(self):
        # TODO: композиция
        pass
```
- `tests_inline`:
```json
{
  "functionTests": [],
  "expectedStdout": null
}
```
- `Task.prompt`: Создайте `Car`, содержащий `Engine`, и метод запуска двигателя.
- `Task.points`: 10

## Пользовательский сценарий
1) `/` — обложка: войдите/зарегистрируйтесь
2) `/toc/` — оглавление с отметками прогресса
3) `/lesson/<slug>/` — урок:
   - слева теория из админки
   - справа редактор и консоль
   - «Запустить» — выполнить код в браузере
   - «Отправить» — сохранить попытку; при успехе — очки и отметка «Пройдено»
4) `/profile/` — очки, % завершения, пройденные главы
5) `/certificate/` — скачать PDF-сертификат (если завершены все уроки)

## Основные URL
- `/`, `/login/`, `/logout/`, `/register/`
- `/toc/`, `/lesson/<slug>/`, `/submit/<slug>/`
- `/profile/`, `/certificate/`
- `/admin/`

## Структура
- `backend/project/settings.py` — настройки (templates, static, редиректы)
- `backend/project/urls.py` — маршруты проекта (подключение `core.urls`)
- `backend/core/models.py` — `Lesson`, `Task`, `ChapterProgress`, `UserProfile`, `Submission`
- `backend/core/views.py` — cover/login/register/toc/lesson/submit/profile/certificate
- `backend/core/urls.py` — маршруты приложения
- `backend/templates/core/` — шаблоны (`base.html`, `cover.html`, `login.html`, `register.html`, `toc.html`, `lesson_detail.html`, `profile.html`)
- `backend/static/core/` — стили и скрипты (`css/theme.css`, `js/*`, `img/*`)

## Тестирование решения (логика)
- Код запускается в браузере (Pyodide); stdout/stderr перехватываются
- Клиент запускает строгие проверки из `tests_inline` (JSON) и формирует подробный отчёт
- Сервер сохраняет `Submission`, обновляет `ChapterProgress` и `UserProfile`
- Очки защищены от «фарма»: учитывается лучший результат по уроку (`best_score`)

## Частые проблемы
- Вижу приветствие Django вместо обложки:
  - В `backend/project/urls.py` должен быть `path('', include('core.urls'))`
  - Перезапустите `runserver` после правок
- 404 на `/favicon.ico` — добавьте файл в `static/core/img/` и подключите в `base.html`

## Продакшн (кратко)
- БД: PostgreSQL; `ALLOWED_HOSTS`, `DEBUG=False`
- Статика: `python manage.py collectstatic`
- Запуск: gunicorn/uvicorn за nginx (WSGI/ASGI)

## Лицензия
MIT (при необходимости скорректируйте)