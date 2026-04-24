import json
from django.core.management.base import BaseCommand
from core.models import Lesson, Task

LESSONS = [
    {
        "title": "Класс и объект",
        "slug": "oop-class-object",
        "order": 1,
        "chapter": "ООП",
        "theory_html": """
<section style="line-height:1.65;">
  <div style="margin-bottom: 20px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">📦 Что такое класс?</h3>
    <p style="margin: 0 0 8px 0;"><strong>Класс</strong> — это шаблон для создания объектов. Он описывает, какие <strong>свойства</strong> (данные) и <strong>методы</strong> (действия) будут у объектов.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 12px; border-radius: 10px; font-family: monospace; font-size: 13px;">
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Dino</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">pass</span>
    </div>
  </div>
  <div style="margin-bottom: 20px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🦕 Что такое объект?</h3>
    <p style="margin: 0 0 8px 0;"><strong>Объект</strong> — это конкретный экземпляр класса. Каждый объект имеет свои уникальные данные.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 12px; border-radius: 10px; font-family: monospace; font-size: 13px;">
      dino1 = <span style="color: #59bf7e;">Dino</span>() &nbsp;&nbsp;<span style="color: #a7dfbb;"># Объект 1</span><br>
      dino2 = <span style="color: #59bf7e;">Dino</span>() &nbsp;&nbsp;<span style="color: #a7dfbb;"># Объект 2</span>
    </div>
  </div>
  <div style="margin-bottom: 20px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🏗️ Метод __init__ (конструктор)</h3>
    <p style="margin: 0 0 8px 0;"><code style="background: #e6f7ec; padding: 2px 6px; border-radius: 6px;">__init__</code> — вызывается при создании объекта. Через <code style="background: #e6f7ec; padding: 2px 6px; border-radius: 6px;">self</code> мы обращаемся к свойствам объекта.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 12px; border-radius: 10px; font-family: monospace; font-size: 13px;">
      <span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">__init__</span>(<span style="color: #ffb86c;">self</span>, <span style="color: #ffb86c;">name</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.<span style="color: #59bf7e;">name</span> = name
    </div>
  </div>
  <div style="margin-bottom: 20px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🎯 Методы класса</h3>
    <p style="margin: 0;">Методы — это функции внутри класса. Они описывают, что умеет делать объект.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 12px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">speak</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">f"I am {self.name}"</span>
    </div>
  </div>
  <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 14px; border-radius: 10px;">
    <strong style="color: #1f5837;">💡 Аналогия:</strong> Класс = форма для печенья, объект = печенье, __init__ = рецепт
  </div>
</section>
""",
        "starter_code": "class Dino:\n    # TODO: добавь метод __init__(self, name)\n    # TODO: добавь метод speak(self), \n    # который возвращает f\"I am {self.name}\"\n    pass",
        "tests_inline": {
            "functionTests": [],
            "expectedStdout": None,
            "expressionTests": [
                {"expr": "Dino('Rex').speak()", "expected": "I am Rex"}
            ]
        },
        "task_prompt": "Создай класс Dino, который умеет:\n1. Принимать имя — через метод __init__(self, name)\n2. Сохранять имя — в свойство self.name\n3. Представляться — метод speak(self) должен возвращать строку \"I am {name}\"\n\n✅ Проверка: Код Dino('Rex').speak() должен вернуть \"I am Rex\"",
        "task_points": 10,
    },
    {
        "title": "Инкапсуляция",
        "slug": "oop-encapsulation",
        "order": 2,
        "chapter": "ООП",
        "theory_html": """
<section style="line-height:1.65;">
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🔒 Что такое инкапсуляция?</h3>
    <p style="margin: 0 0 8px 0;"><strong>Инкапсуляция</strong> — это сокрытие внутреннего состояния объекта от прямого доступа извне. Данные защищены, работать с ними можно только через специальные методы.</p>
    <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 10px; border-radius: 10px; margin-top: 8px; font-size: 14px;">
      💡 <strong>Аналогия:</strong> Капсула с лекарством — вы не трогаете само лекарство, а принимаете по инструкции.
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🙈 Приватные атрибуты</h3>
    <p style="margin: 0 0 8px 0;"><code style="background: #e6f7ec; padding: 2px 6px; border-radius: 6px;">__имя</code> — двойное подчёркивание делает атрибут приватным.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">BankAccount</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">__init__</span>(<span style="color: #ffb86c;">self</span>, <span style="color: #ffb86c;">balance</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.<span style="color: #59bf7e;">__balance</span> = balance
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🔑 Геттеры и сеттеры</h3>
    <p style="margin: 0;">Методы для безопасного доступа к приватным атрибутам.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">get_balance</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">self</span>.<span style="color: #59bf7e;">__balance</span><br>
      <span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">deposit</span>(<span style="color: #ffb86c;">self</span>, <span style="color: #ffb86c;">amount</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">if</span> amount > 0:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.<span style="color: #59bf7e;">__balance</span> += amount
    </div>
  </div>
  <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 10px; border-radius: 10px;">
    <strong style="color: #1f5837;">✅ Зачем?</strong> Защита данных, скрытие сложности, контроль доступа.
  </div>
</section>
""",
        "starter_code": "class BankAccount:\n    def __init__(self, balance):\n        self.__balance = balance\n    \n    # TODO: добавь метод get_balance(self), который возвращает __balance\n    # TODO: добавь метод deposit(self, amount), который увеличивает __balance на amount\n    pass",
        "tests_inline": {
            "functionTests": [],
            "expectedStdout": "10\n17",
            "expressionTests": []
        },
        "task_prompt": "Создай класс BankAccount, который умеет:\n1. Принимать начальный баланс — через метод __init__(self, balance)\n2. Сохранять баланс в приватный атрибут __balance\n3. Показывать баланс — метод get_balance(self) возвращает текущий баланс\n4. Пополнять счёт — метод deposit(self, amount) увеличивает баланс на amount\n\n✅ Проверка: После создания счёта с балансом 10 и пополнения на 7, баланс должен стать 17",
        "task_points": 10,
    },
    {
        "title": "Наследование",
        "slug": "oop-inheritance",
        "order": 3,
        "chapter": "ООП",
        "theory_html": """
<section style="line-height:1.65;">
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">👨‍👦 Что такое наследование?</h3>
    <p style="margin: 0 0 8px 0;"><strong>Наследование</strong> — механизм создания нового класса на основе существующего. Дочерний класс получает все методы и атрибуты родительского.</p>
    <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 10px; border-radius: 10px; margin-top: 8px; font-size: 14px;">
      💡 <strong>Аналогия:</strong> Ребёнок наследует черты родителей, но может иметь свои уникальные особенности.
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">📝 Синтаксис наследования</h3>
    <p style="margin: 0 0 8px 0;">Дочерний класс указывается в скобках после имени класса.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Animal</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">speak</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">"..."</span><br><br>
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Dog</span>(<span style="color: #59bf7e;">Animal</span>): &nbsp;&nbsp;<span style="color: #a7dfbb;"># Наследуем Animal</span><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">pass</span>
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🔄 Переопределение методов</h3>
    <p style="margin: 0 0 8px 0;">Дочерний класс может изменить поведение метода, создав свой с тем же именем.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Dog</span>(<span style="color: #59bf7e;">Animal</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">speak</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">"woof"</span>
    </div>
  </div>
  <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 12px; border-radius: 10px;">
    <strong style="color: #1f5837;">✅ Зачем?</strong> Переиспользование кода, иерархия классов, расширение функциональности без изменения родителя.
  </div>
</section>
""",
        "starter_code": "class Animal:\n    def speak(self):\n        return \"...\"\n\nclass Dog(Animal):\n    # TODO: переопредели метод speak(self), чтобы он возвращал \"woof\"\n    pass",
        "tests_inline": {
            "functionTests": [],
            "expectedStdout": None,
            "expressionTests": [
                {"expr": "Dog().speak()", "expected": "woof"}
            ]
        },
        "task_prompt": "Создай класс Dog, который наследуется от Animal:\n1. Класс Animal уже есть с методом speak(), который возвращает \"...\"\n2. Создай класс Dog(Animal) — наследник Animal\n3. Переопредели метод speak() в классе Dog, чтобы он возвращал \"woof\"\n\n✅ Проверка: Код Dog().speak() должен вернуть \"woof\"",
        "task_points": 10,
    },
    {
        "title": "Полиморфизм",
        "slug": "oop-polymorphism",
        "order": 4,
        "chapter": "ООП",
        "theory_html": """
<section style="line-height:1.65;">
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🎭 Что такое полиморфизм?</h3>
    <p style="margin: 0 0 8px 0;"><strong>Полиморфизм</strong> — способность объектов разных классов использовать один и тот же интерфейс. Один метод может работать по-разному для разных объектов.</p>
    <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 10px; border-radius: 10px; margin-top: 8px; font-size: 14px;">
      💡 <strong>Аналогия:</strong> Команда «Голос!» — кошка скажет «мяу», собака — «гав», корова — «му».
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🎯 Единый интерфейс</h3>
    <p style="margin: 0 0 8px 0;">Разные классы имеют метод с одинаковым именем, но разной реализацией.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Cat</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">sound</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">"meow"</span><br><br>
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Cow</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">sound</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">"moo"</span>
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🔄 Полиморфная функция</h3>
    <p style="margin: 0 0 8px 0;">Функция может работать с любым объектом, у которого есть нужный метод.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">make_sound</span>(<span style="color: #ffb86c;">animal</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">animal</span>.<span style="color: #a7dfbb;">sound</span>()<br><br>
      <span style="color: #a7dfbb;">print</span>(<span style="color: #a7dfbb;">make_sound</span>(<span style="color: #59bf7e;">Cat</span>())) &nbsp;&nbsp;<span style="color: #a7dfbb;"># meow</span><br>
      <span style="color: #a7dfbb;">print</span>(<span style="color: #a7dfbb;">make_sound</span>(<span style="color: #59bf7e;">Cow</span>())) &nbsp;&nbsp;<span style="color: #a7dfbb;"># moo</span>
    </div>
  </div>
  <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 12px; border-radius: 10px;">
    <strong style="color: #1f5837;">✅ Зачем?</strong> Универсальный код, гибкость, простота расширения — новые классы работают без изменений.
  </div>
</section>
""",
        "starter_code": "class Cat:\n    def sound(self):\n        return \"meow\"\n\nclass Cow:\n    def sound(self):\n        return \"moo\"\n\ndef make_sound(animal):\n    # TODO: вызови метод sound() у animal и верни результат\n    pass",
        "tests_inline": {
            "functionTests": [],
            "expectedStdout": None,
            "expressionTests": [
                {"expr": "make_sound(Cat())", "expected": "meow"},
                {"expr": "make_sound(Cow())", "expected": "moo"}
            ]
        },
        "task_prompt": "Реализуй функцию make_sound(animal), которая:\n1. Принимает объект animal (экземпляр класса Cat или Cow)\n2. Вызывает у него метод sound()\n3. Возвращает результат вызова\n\n✅ Проверка: make_sound(Cat()) должен вернуть \"meow\", make_sound(Cow()) — \"moo\"",
        "task_points": 10,
    },
    {
        "title": "Абстракция",
        "slug": "oop-abstraction",
        "order": 5,
        "chapter": "ООП",
        "theory_html": """
<section style="line-height:1.65;">
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">📐 Что такое абстракция?</h3>
    <p style="margin: 0 0 8px 0;"><strong>Абстракция</strong> — выделение главных характеристик объекта, скрывая второстепенные детали. Пользователь знает ЧТО делает объект, но не КАК.</p>
    <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 10px; border-radius: 10px; margin-top: 8px; font-size: 14px;">
      💡 <strong>Аналогия:</strong> Чтобы водить машину, не нужно знать, как работает двигатель внутри. Достаточно знать педали и руль.
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">📦 Абстрактные классы (ABC)</h3>
    <p style="margin: 0 0 8px 0;">Абстрактный класс — это шаблон, который нельзя создать напрямую. Он задаёт правила для дочерних классов.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">from</span> abc <span style="color: #7fcf9b;">import</span> ABC, abstractmethod<br><br>
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Shape</span>(ABC): &nbsp;&nbsp;<span style="color: #a7dfbb;"># Абстрактный класс</span><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">@abstractmethod</span><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">area</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">pass</span>
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🔨 Реализация абстрактных методов</h3>
    <p style="margin: 0 0 8px 0;">Дочерний класс ОБЯЗАН реализовать все абстрактные методы родителя.</p>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Rectangle</span>(<span style="color: #59bf7e;">Shape</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">__init__</span>(<span style="color: #ffb86c;">self</span>, <span style="color: #ffb86c;">w</span>, <span style="color: #ffb86c;">h</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.w = w<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.h = h<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">area</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">self</span>.w * <span style="color: #ffb86c;">self</span>.h
    </div>
  </div>
  <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 12px; border-radius: 10px;">
    <strong style="color: #1f5837;">✅ Зачем?</strong> Создание чётких интерфейсов, гарантия наличия методов, удобство командной работы.
  </div>
</section>
""",
        "starter_code": "from abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass\n\nclass Rectangle(Shape):\n    # TODO: добавь __init__(self, width, height)\n    # TODO: реализуй метод area(self), возвращающий width * height\n    pass",
        "tests_inline": {
            "functionTests": [],
            "expectedStdout": None,
            "expressionTests": [
                {"expr": "Rectangle(2, 3).area()", "expected": 6}
            ]
        },
        "task_prompt": "Создай класс Rectangle, который наследуется от абстрактного класса Shape:\n1. Добавь метод __init__(self, width, height) для сохранения ширины и высоты\n2. Реализуй абстрактный метод area(self), который возвращает площадь (width * height)\n\n✅ Проверка: Rectangle(2, 3).area() должен вернуть 6\n\n💡 Подсказка: Абстрактные методы ОБЯЗАТЕЛЬНО нужно реализовать в дочернем классе, иначе будет ошибка.",
        "task_points": 10,
    },
    {
        "title": "Dunder-методы",
        "slug": "oop-dunder-methods",
        "order": 6,
        "chapter": "ООП",
        "theory_html": """
<section style="line-height:1.65;">
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">✨ Что такое dunder-методы?</h3>
    <p style="margin: 0 0 8px 0;"><strong>Dunder-методы</strong> (double underscore) — специальные методы с двумя подчёркиваниями в начале и конце. Они определяют поведение объектов для встроенных операций.</p>
    <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 10px; border-radius: 10px; margin-top: 8px; font-size: 14px;">
      💡 <strong>Название:</strong> «dunder» = <strong>d</strong>ouble <strong>under</strong>score (двойное подчёркивание)
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">📝 Основные dunder-методы</h3>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 12px; margin-top: 8px;">
      <span style="color: #a7dfbb;">__init__</span>(self, ...) &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #a7dfbb;"># Конструктор, создание объекта</span><br>
      <span style="color: #a7dfbb;">__str__</span>(self) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #a7dfbb;"># print(object) или str(object)</span><br>
      <span style="color: #a7dfbb;">__add__</span>(self, other) &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #a7dfbb;"># object1 + object2</span><br>
      <span style="color: #a7dfbb;">__sub__</span>(self, other) &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #a7dfbb;"># object1 - object2</span><br>
      <span style="color: #a7dfbb;">__eq__</span>(self, other) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #a7dfbb;"># object1 == object2</span><br>
      <span style="color: #a7dfbb;">__len__</span>(self) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #a7dfbb;"># len(object)</span>
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🔧 Пример: __add__ и __str__</h3>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Vector</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">__init__</span>(<span style="color: #ffb86c;">self</span>, <span style="color: #ffb86c;">x</span>, <span style="color: #ffb86c;">y</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.x = x<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.y = y<br><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">__add__</span>(<span style="color: #ffb86c;">self</span>, <span style="color: #ffb86c;">other</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #59bf7e;">Vector</span>(<span style="color: #ffb86c;">self</span>.x + other.x, <span style="color: #ffb86c;">self</span>.y + other.y)<br><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">__str__</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">f"Vector({self.x}, {self.y})"</span>
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🎯 Использование</h3>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      v1 = <span style="color: #59bf7e;">Vector</span>(1, 2)<br>
      v2 = <span style="color: #59bf7e;">Vector</span>(3, 4)<br>
      v3 = v1 + v2 &nbsp;&nbsp;<span style="color: #a7dfbb;"># Вызывается __add__</span><br>
      <span style="color: #a7dfbb;">print</span>(v3) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #a7dfbb;"># Вызывается __str__ → "Vector(4, 6)"</span>
    </div>
  </div>
  <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 12px; border-radius: 10px;">
    <strong style="color: #1f5837;">✅ Зачем?</strong> Создание естественного поведения объектов, поддержка операторов, удобный вывод, красивый код.
  </div>
</section>
""",
        "starter_code": "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    \n    # TODO: реализуй __add__(self, other) — возвращает новый Vector с суммой x и y\n    # TODO: реализуй __str__(self) — возвращает строку \"Vector(x, y)\"\n    pass",
        "tests_inline": {
            "functionTests": [],
            "expectedStdout": None,
            "expressionTests": [
                {"expr": "(Vector(1, 2) + Vector(3, 4)).x", "expected": 4},
                {"expr": "(Vector(1, 2) + Vector(3, 4)).y", "expected": 6}
            ]
        },
        "task_prompt": "Реализуй в классе Vector два dunder-метода:\n1. __add__(self, other) — должен возвращать новый объект Vector, у которого x = self.x + other.x, y = self.y + other.y\n2. __str__(self) — должен возвращать строку в формате \"Vector(x, y)\" (например, \"Vector(4, 6)\")\n\n✅ Проверка: (Vector(1, 2) + Vector(3, 4)) должен дать Vector с x=4, y=6\n\n💡 Подсказка: __add__ возвращает НОВЫЙ объект, не изменяя self. __str__ возвращает строку для print().",
        "task_points": 10,
    },
    {
        "title": "Композиция",
        "slug": "oop-composition",
        "order": 7,
        "chapter": "ООП",
        "theory_html": """
<section style="line-height:1.65;">
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🔧 Что такое композиция?</h3>
    <p style="margin: 0 0 8px 0;"><strong>Композиция</strong> — это принцип, при котором объект состоит из других объектов. Вместо наследования «является», композиция использует отношение «имеет».</p>
    <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 10px; border-radius: 10px; margin-top: 8px; font-size: 14px;">
      💡 <strong>Аналогия:</strong> Машина <strong>имеет</strong> двигатель, колёса и руль. Она не является двигателем, а состоит из него.
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🏗️ Композиция vs Наследование</h3>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 12px; margin-top: 8px;">
      <span style="color: #a7dfbb;"># Наследование (is-a)</span><br>
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Dog</span>(<span style="color: #59bf7e;">Animal</span>): &nbsp;&nbsp;<span style="color: #a7dfbb;"># Собака ЯВЛЯЕТСЯ животным</span><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">pass</span><br><br>
      <span style="color: #a7dfbb;"># Композиция (has-a)</span><br>
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Car</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">__init__</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.engine = <span style="color: #59bf7e;">Engine</span>() &nbsp;&nbsp;<span style="color: #a7dfbb;"># Машина ИМЕЕТ двигатель</span>
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">📝 Пример композиции</h3>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Engine</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">start</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">"engine started"</span><br><br>
      <span style="color: #7fcf9b;">class</span> <span style="color: #59bf7e;">Car</span>:<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">__init__</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffb86c;">self</span>.engine = <span style="color: #59bf7e;">Engine</span>()<br><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">def</span> <span style="color: #a7dfbb;">start</span>(<span style="color: #ffb86c;">self</span>):<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #7fcf9b;">return</span> <span style="color: #ffb86c;">self</span>.engine.start()
    </div>
  </div>
  <div style="margin-bottom: 16px;">
    <h3 style="color: #2f8852; margin: 0 0 8px 0;">🎯 Использование</h3>
    <div style="background: #1a2a22; color: #e2e8f0; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 13px; margin-top: 8px;">
      my_car = <span style="color: #59bf7e;">Car</span>()<br>
      <span style="color: #a7dfbb;">print</span>(my_car.start()) &nbsp;&nbsp;<span style="color: #a7dfbb;"># "engine started"</span>
    </div>
  </div>
  <div style="background: #f0f7f3; border-left: 4px solid #59bf7e; padding: 12px; border-radius: 10px;">
    <strong style="color: #1f5837;">✅ Зачем?</strong> Гибкость, переиспользование кода, слабая связанность объектов, легче менять составные части.
  </div>
</section>
""",
        "starter_code": "class Engine:\n    def start(self):\n        return \"engine started\"\n\nclass Car:\n    def __init__(self):\n        # TODO: создай атрибут self.engine — экземпляр класса Engine\n        pass\n    \n    def start(self):\n        # TODO: вызови метод start() у self.engine и верни результат\n        pass",
        "tests_inline": {
            "functionTests": [],
            "expectedStdout": None,
            "expressionTests": [
                {"expr": "Car().start()", "expected": "engine started"}
            ]
        },
        "task_prompt": "Создай класс Car, который использует композицию с классом Engine:\n1. В методе __init__ создай атрибут self.engine — экземпляр класса Engine\n2. В методе start(self) вызови метод start() у self.engine и верни результат\n\n✅ Проверка: Car().start() должен вернуть \"engine started\"\n\n💡 Подсказка: Класс Engine уже есть. Просто создай его экземпляр внутри Car и используй его метод.",
        "task_points": 10,
    },
]


class Command(BaseCommand):
    help = "Create or update 7 OOP lessons with tasks."

    def handle(self, *args, **options):
        created_lessons = 0
        updated_lessons = 0
        created_tasks = 0
        updated_tasks = 0

        for item in LESSONS:
            lesson_defaults = {
                "title": item["title"],
                "order": item["order"],
                "chapter": item["chapter"],
                "theory_html": item["theory_html"],
                "starter_code": item["starter_code"],
                "tests_inline": json.dumps(item["tests_inline"], ensure_ascii=False, indent=2),
            }
            lesson, lesson_created = Lesson.objects.update_or_create(
                slug=item["slug"],
                defaults=lesson_defaults,
            )
            if lesson_created:
                created_lessons += 1
            else:
                updated_lessons += 1

            task, task_created = Task.objects.update_or_create(
                lesson=lesson,
                defaults={
                    "prompt": item["task_prompt"],
                    "points": item["task_points"],
                },
            )
            if task_created:
                created_tasks += 1
            else:
                updated_tasks += 1

            self.stdout.write(self.style.SUCCESS(f"Lesson ready: {lesson.slug}"))

        self.stdout.write("")
        self.stdout.write(self.style.WARNING(
            f"Done: lessons created={created_lessons}, updated={updated_lessons}; "
            f"tasks created={created_tasks}, updated={updated_tasks}"
        ))