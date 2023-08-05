# Etthp

Это ehttp - легковесная и предельно простая библиотека для создания http api интерфейсов.

- [ ] add auto-restart on change code
- [X] fix cookies
- [X] rewrite on sockets
- [X] add redirect
- [ ] url params
- [X] Возможность возвращать строки с не ascii символами
- [ ] custom 404 and 500

Для установки ehttp в систему необходимо выполнить команду `pip install ehttp` или загрузить этот репозиторий и выполнить `python setup.py install`

# Использование

```python
import ehttp


server = ehttp.Server(
    host="localhost",  # адресс, на котором будет запущен сервер
    port=3000,  # порт
    force_bind=False,  # принудительно завершить процесс если он занимает нужный порт
    default_headers=None  # заголовки, которые всегда будет возвращать сервер
)
```

Этот код импортирует и установит конфигурацию по умолчанию для ehttp сервера в вашем проекте.
Для запуска необходимо вызвать `server.start()`.

```python
@server.bind("/index")
def index(req: ehttp.Request):
    return """
    <b>
        hello
    </b> 
    <i>
        world
    </i>"""
```

![1673024283799](image/README/1673024283799.png)

Декораторы используются для назначения пути на внутренний метод на сервере.
После декоратора должен быть объявлен метод, первым аргументом принимающий объект типа `ehttp.Request`, а остальными matсh группы для регулярных выражений.
Возвращать метод может объект типа `ehttp.Response`, `dict`, `str`, `bytes` или `ehttp.File`. Так же можно возвращать нумерованные аргументы response в кортеже.

Вы можете использовать регулярные выражения с помощью метода `bind`.

```python
@server.bind(r'/regex/(\w*)(?:\.)(\w*)(?:|/)')
def regex(req: ehttp.Request, first, second):
    return ehttp.Response(
        200, f"""\t\t{req.path}
        \t{first} - {second}
        """,
        content_type="txt"
        )
```

![1673024340725](image/README/1673024340725.png)

Или если вы не умеете использовать регулярные выражения вы можете использовать лёгкие бинды - `ebind`.

```python
@server.ebind('/ebind/<first>.<second>')
def ebind(req: ehttp.Request, first, second):
    return ehttp.Response(
        200, f"""\t\t{req.path}
        \t{first} - {second}
        """,
        content_type="txt"
    )
```

![1673024638845](image/README/1673024638845.png)

Вы также можете взаимодействовать с входящим запросом. Например вернуть пользователю всю известную о запросе информацию следующим кодом:

```python
@server.bind("/info")
def info(req: ehttp.Request):
    return req.__dict__
```

![1673027113084](image/README/1673027113084.png)

Для возврата пользователю файла нужно создать экзэмпляр класса ehttp.File и вернуть его в функции.

```python
@server.bind("/git")
def git(_):
    return ehttp.File(".gitignore")
```

![1673027492228](image/README/1673027492228.png)

Если будет запрошен путь, который не имеет подходящего обработчика - будет вызван стандартный метод `_err404`.

![1673027492228](image/README/1673027986194.png)

Пока что его нельзя переназначить его без костылей, но как временное решение - бинд на `r".*"` после всех, который будет ловить оставшиеся запросы.

Также имеется реализация внутренних ошибок на методе `_err500`.

```python
@server.ebind('/div/<first>&<second>')
def div(_, first, second):
    return float(first)/float(second)
```

![1673027492228](image/README/1673028562753.png)

Вместе с сообщением и 500 кодом вы получите сообщение в консоль от логгера об ошибке.
![1673028640229](image/README/1673028640229.png)

Модуль позволяет также создавать прокси для запросов. Это может быть полезно для фикса ошибок CORS стороннего ресурса или других вариантах, когда вернуть надо ответ на некоторый другой адресс. Для прокси есть метод ehttp.proxy(), который внутри использует возможность возвращать ответ на запрос библиотеки requests.

```python
def proxy(address="http://localhost:80", host="0.0.0.0", port=3000, force_bind=False):
    @server.bind("(.*)")
    def _(req: Request, path):
        return requests.request(
            req.method, address+path,
            headers=req.headers, data=req.raw_data,
            timeout=20
        )
    server.start()
```
