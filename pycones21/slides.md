---
theme: "./theme.json"
author: Ismael Mendonça
date: Oct 2, 2021
paging: Slide %d / %d
---

# Python testing best practices

## Agenda

- Testing principles
- Frameworks
- Pruebas funcionales vs Pruebas basadas en clases
- setUp & tearDown
- Patch & Mock
- Raising exceptions
- Datetime
- Recomendaciones para tu CI

---

# Testing principles

## Test isolation

Las pruebas no deben producir "side-effects" sobre otras pruebas.

---

# Testing principles

## Test isolation

Las pruebas no deben producir "side-effects" sobre otras pruebas.

Posibles causas...

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas

```python
def test_get_gist_urls():

    ...

    ### Start the mock without stopping it
    mock.patch.object(GithubClient, "_get", return_value=m_response).start()
    ###

    urls = GithubClient.get_gists_urls()

    assert urls == [response_urls[0]["url"]]


def test_get_gist_names():
    # OMG THIS IS STILL A MOCK!
    #
    # The mock is still applied as a side-effect from the previous test
    assert isinstance(GithubClient._get, mock.Mock)
```

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas

_Ejemplo 1_

```bash
poetry run pytest isolation/1-patch.py

```

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas

Posibles soluciones...

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas

Context manager

```python

def test_get_gist_urls():

    ...

    # Wrap the code where we want the patch to take effect with a context manager
    with mock.patch.object(GithubClient, "_get", return_value=m_response):
        urls = GithubClient.get_gists_urls()

    assert urls == [response_urls[0]["url"]]


def test_get_gist_names():
    # Should fail
    assert isinstance(GithubClient._get, mock.Mock)

```

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas

_Ejemplo 2_

```bash
poetry run pytest isolation/2-patch-ok.py

```

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas

Decorator

```python
# Or you could use a decorator
@mock.patch("pycones21.github_client.requests.get")
def test_get_gist_urls(m_request):

    ...

    m_request.return_value = m_response

    urls = GithubClient.get_gists_urls()

    assert urls == [response_urls[0]["url"]]


def test_get_gist_names():
    # Should also fail
    assert isinstance(GithubClient._get, mock.Mock)
```

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas

_Ejemplo 3_

```bash
poetry run pytest isolation/3-patch-ok.py

```

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas

```python
def test_create_user():
    user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

    assert user.username == "ismaelmt"

    assert user.email == "ismael@ismael.com"
    assert UserStore.count() == 1


def test_user_amount():

    # We want that each test have a clean DB
    # This test will fail, but it shouldn't.
    assert UserStore.count() == 0
```

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas

_Ejemplo 4_

```bash
poetry run pytest isolation/4-db.py

```

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas

```python
@pytest.fixture(autouse=True)
def db_fixture():

    yield

    UserStore.clean()


def test_create_user():
    user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

    assert user.username == "ismaelmt"

    assert user.email == "ismael@ismael.com"
    assert UserStore.count() == 1


def test_user_amount():

    # We want that each test have a clean DB
    # This test will fail, but it shouldn't.
    assert UserStore.count() == 0

```

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas

_Ejemplo 5_

```bash
poetry run pytest isolation/5-db-ok.py

```

---

# Testing principles

## Test isolation

### Compartir estado entre pruebas dentro de una clase

---

# Testing principles

## Test isolation

### Compartir estado entre pruebas dentro de una clase

```python
class TestLeakUsers:
    @classmethod
    def setup_class(cls):
        cls.user = {"name": "Lola Mento", "username": "iamauser@user.com"}


    def test_username(self):
        self.user["name"] = "Elsa Murito"
        assert self.user["username"] == "iamauser@user.com"


    def test_name(self):
        # Capasao!??
        assert self.user["name"] == "Lola Mento"

```

_Importante_: Si necesitas compartir estado, hazlo solo para leerlo durante las pruebas, no lo modifiques!

---

# Testing principles

## Test isolation

### Compartir estado entre pruebas dentro de una clase

_Ejemplo 6_

```bash
poetry run pytest isolation/6-share-state.py

```

---

# Testing principles

> The more you have to mock out to test your code, the worse your code is.
> The more code you have to instantiate and put in place to be able to test a specific piece of behavior,
> the worse your code is.
> The goal is small testable units, along with higher-level integration and functional
> tests to test that the units cooperate correctly.

> 30 best practices for software development and testing -- Michael Foord

---

# Testing principles

## Pruebas unitarias

---

# Testing principles

## Pruebas unitarias

Las pruebas unitarias deben:

---

# Testing principles

## Pruebas unitarias

Las pruebas unitarias deben:

- _Tratarse como cajas negras_: Evita modificar métodos internos o estados.

---

# Testing principles

## Pruebas unitarias

Las pruebas unitarias deben:

- _Tratarse como cajas negras_: Evita modificar métodos internos o estados.

- _Pequeñas y bien enfocadas_: Pruebas muy grandes usualmente es un indicador de código mal estructurado.

---

# Testing principles

## Pruebas unitarias

Las pruebas unitarias deben:

- _Tratarse como cajas negras_: Evita modificar métodos internos o estados.

- _Pequeñas y bien enfocadas_: Pruebas muy grandes usualmente es un indicador de código mal estructurado.
- _Rápidas_: "Una prueba que dura más de 0.1 segundos ya no es considerada unitaria"

---

# Testing principles

## Recomendaciones generales

---

# Testing principles

## Recomendaciones generales

- _Tu código debe SIEMPRE incluir pruebas_: Una base de código sin pruebas, debe asumirse como defectuosa.

---

# Testing principles

## Recomendaciones generales

- _Tu código debe SIEMPRE incluir pruebas_: Una base de código sin pruebas, debe asumirse como defectuosa.
- _El código de pruebas debe tratarse como código de producto_: YAGNI, KISS, DRY, patrones de diseño.

---

# Frameworks

---

# Frameworks

Principales frameworks:

- pytest
- unittest
- Nose
- Nose2
  ...

---

# Frameworks

Principales frameworks:

- pytest
- unittest
- ~~Nose~~
- ~~Nose2~~
  ...

---

# Pruebas funcionales vs Pruebas basadas en clases

---

# Pruebas funcionales vs Pruebas basadas en clases

- `pytest`: Permite escribir tests como funciones o como clases.
- `unittest.TestCase`: Todas las pruebas son escritas en clases.

---

# Pruebas funcionales vs Pruebas basadas en clases

Funciones en _pytest_

---

# Pruebas funcionales vs Pruebas basadas en clases

Funciones en _pytest_

```python
def test_get_fake_store():
    user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

    assert FakeStore.get("users", "1") == user
```

---

# Pruebas funcionales vs Pruebas basadas en clases

Clases en _pytest_

---

# Pruebas funcionales vs Pruebas basadas en clases

Clases en _pytest_

```python
class TestFakeStorePytest:
    @pytest.fixture(autouse=True)
    def fake_store(self):
        FakeStore.clean()

    def test_get_fake_store_in_class(self):

        user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

        assert FakeStore.get("users", "1") == user

```

---

# Pruebas funcionales vs Pruebas basadas en clases

Clases en _unittest_

---

# Pruebas funcionales vs Pruebas basadas en clases

Clases en _unittest_

```python
class TestFakeStore(TestCase):
    def setUp(self):
        FakeStore.clean()

    def test_get_fake_store_in_class(self):

        user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

        assert FakeStore.get("users", "1") == user

```

---

# Pruebas funcionales vs Pruebas basadas en clases

_Ejemplo 7_

```bash
poetry run pytest ./class_test/7-class-fun.py
```

---

# Pruebas funcionales vs Pruebas basadas en clases

Las siguientes son recomendaciones generales:

---

# Pruebas funcionales vs Pruebas basadas en clases

Las siguientes son recomendaciones generales:

- Utiliza clases como una forma de agrupación semántica de tus pruebas.

---

# Pruebas funcionales vs Pruebas basadas en clases

Las siguientes son recomendaciones generales:

- Utiliza clases como una forma de agrupación semántica de tus pruebas.
- Si necesitas compartir estado entre pruebas (setup, class attribute), utiliza clases.

---

# Pruebas funcionales vs Pruebas basadas en clases

Las siguientes son recomendaciones generales:

- Utiliza clases como una forma de agrupación semántica de tus pruebas.
- Si necesitas compartir estado entre pruebas (setup, class attribute), utiliza clases.
- Si necesitas ejecutar un conjunto de pruebas en un mismo core, utiliza clases.

---

# Pruebas funcionales vs Pruebas basadas en clases

Las siguientes son recomendaciones generales:

- Utiliza clases como una forma de agrupación semántica de tus pruebas.
- Si necesitas compartir estado entre pruebas (setup, class attribute), utiliza clases.
- Si necesitas ejecutar un conjunto de pruebas en un mismo core, utiliza clases.
- Usa `fixtures` para código que necesites reusar entre funciones o métodos.

---

# setup & teardown

---

# setup & teardown

Si necesitas datos para tus tests, utiliza los metodos setup y teardown
para preparar y limpiar los datos respectivamente.

---

# setup & teardown

## pytest

---

# setup & teardown

## pytest

_Recomendacion_: fixtures

---

# setup & teardown

## pytest

_Recomendacion_: fixtures

- En pytest nos valemos de `fixtures`. Puedes crear una fixture que realice tanto el setup como el teardown.
- Diferentes scopes: `package`, `session`, `class`, `module`, `function`.

```python
@pytest.fixture
def db(autouse=True, scope="function"):

    # setup
    UserStore.create_user(username="test_user", email="test@example.com")

    yield

    #teardown
    FakeStore.clean()
```

---

# setup & teardown

## pytest

_No recomendado_: xunit-style

---

# setup & teardown

## pytest

_No recomendado_: xunit-style

- O puedes usar también setup y teardown al estilo xunit:
  - `setup_class`, `setup_module`, `setup_function`
  - `teardown_class`, `teardown_module`, `teardown_function`

---

# setup & teardown

## unittest

---

# setup & teardown

## unittest

```python
class TestUser(unittest.TestCase):

    def setUp(self):
        ...

    @classmethod
    def setUpClass(cls):
        cls.user = ...
```

---

# setup & teardown

## unittest

```python
class TestUser(unittest.TestCase):

    def setUp(self):
        ...

    @classmethod
    def setUpClass(cls):
        cls.user = ...
```

_¡Cuidado!_

Cuando utilizas `setUpClass` lo que defines se mantendrá instanciado a nivel de clase,
si modificas alguna de las variables del `setUpClass` puedes causar algún "side-effect".

---

# Patch & Mock

## Mocking

---

# Patch & Mock

## Mocking

Librerías:

- unittest.mock
- pytest-mock: Provee un fixture llamado `mocker`

---

# Patch & Mock

## Mocking

Librerias:

- unittest.mock ✓
- ~~pytest-mock~~: Provee un fixture llamado `mocker`

---

# Patch & Mock

## Mocking

Librerias:

- unittest.mock ✓
- ~~pytest-mock~~: Provee un fixture llamado `mocker`
  - `mocker`: Automáticamente deshace el patch al final del test.

---

# Patch & Mock

## Mocking

Librerias:

- unittest.mock ✓
- ~~pytest-mock~~: Provee un fixture llamado `mocker`
  - `mocker`: Automáticamente deshace el patch al final del test.
  - Conveniente, pero puede resultar _contraproducente_ en equipos grandes de ingeniería.

---

# Patch & Mock

## Mocking

Librerias:

- unittest.mock ✓
- ~~pytest-mock~~: Provee un fixture llamado `mocker`
  - `mocker`: Automáticamente deshace el patch al final del test.
  - Conveniente, pero puede resultar _contraproducente_ en equipos grandes de ingeniería.
  - Confusión entre `unittest.mock` y `mocker`. No funcionan bien en conjunto.

---

# Patch & Mock

## Mocking

Problemas con mocker

```python
def test_mocker_context(mocker):
    with mocker.patch.object(UserStore, "count"):
        assert isinstance(UserStore.count, mocker.MagicMock)
```

---

# Patch & Mock

## Mocking

_Ejemplo 8_

```bash
poetry run pytest mock_patch/8-mocker.py

```

---

# Patch & Mock

## Mocking

Problemas con mocker

```python

def new_count():
    return 10

def test_mocker_context(mocker):
    with mocker.patch.object(UserStore, "count", new=new_count):
        assert isinstance(UserStore.count, mocker.MagicMock)
```

---

# Patch & Mock

## Mocking

_Ejemplo 9_

```bash
poetry run pytest mock_patch/9-mocker.py

```

---

# Patch & Mock

## Mocking

```python
class GithubClient:
    ...
    @classmethod
    def get_gists(cls):
        LIST_GISTS_ENDPOINT = f"{cls.API_HOST}/gists"

        response = cls._get(LIST_GISTS_ENDPOINT)

        return response
    ...
```

---

# Patch & Mock

## Mocking

`call` methods en mocks

---

# Patch & Mock

## Mocking

`call` methods en mocks

```python
from unittest import mock
from pycones21.github_client import GithubClient


@mock.patch.object(GithubClient, "_get")
def test_assertion(m_get):
    with mock.patch.object(GithubClient, "get_gists_urls") as m_get_gists_urls:
        GithubClient.get_gists()
    assert m_get_gists_urls.called_once()

```

---

# Patch & Mock

## Mocking

_Ejemplo 10_

```bash
poetry run pytest mock_patch/10-mock-call.py

```

---

# Patch & Mock

## Mocking

`call` methods en mocks

```python
from unittest import mock
from pycones21.github_client import GithubClient


@mock.patch.object(GithubClient, "_get")
def test_assertion(m_get):
    with mock.patch.object(GithubClient, "get_gists_urls") as m_get_gists_urls:
        GithubClient.get_gists_urls()
    m_get_gists_urls.assert_called_once()

```

---

# Patch & Mock

## Mocking

_Ejemplo 11_

```bash
poetry run pytest mock_patch/11-mock-call-ok.py

```

---

# Patch & Mock

## Patch

### Patch target

---

# Patch & Mock

## Patch

### Patch target

El objeto al que queremos aplicarle el patch debe cumplir con las siguientes reglas:

---

# Patch & Mock

## Patch

### Patch target

El objeto al que queremos aplicarle el patch debe cumplir con las siguientes reglas:

- Debe poder ser importado de tu archivo de pruebas.

---

# Patch & Mock

## Patch

### Patch target

El objeto al que queremos aplicarle el patch debe cumplir con las siguientes reglas:

- Debe poder ser importado de tu archivo de pruebas.

- El _path_ debe ser del objeto que va a ser usado y no donde el objeto se define.

---

# Patch & Mock

## Patch

### Patch target

```python
# service.py
from pycones21.github_client import GithubClient

def call_github():
    gists = GithubClient.get_gists()
    return gists
```

---

# Patch & Mock

## Patch

### Patch target

El patch debe hacerse en `service` y no en `github_client`

---

# Patch & Mock

## Patch

### Patch target

El patch debe hacerse en `service` y no en `github_client`

```python

from pycones21.service import call_github

@mock.patch("pycones21.service.GithubClient.get_gists")
def test_get_gists(m_gists):

    call_github()
    m_gists.assert_called_once()
```

---

# Patch & Mock

## Patch

### Patch target

_Ejemplo 12_

```bash
poetry run pytest mock_patch/12-patch-target.py
```

---

# Patch & Mock

## Patch

### Patch hell

---

# Patch & Mock

## Patch

### Patch hell

```python

def test_nested_mocks():
    with mock.patch.object(FakeStore, "namespace_exists") as m1:
        with mock.patch.object(FakeStore, "get") as m2:
            with mock.patch.object(FakeStore, "set_namespace") as m3:
                with mock.patch.object(FakeStore, "count") as m4:
                    assert isinstance(m1, mock.MagicMock)
                    assert isinstance(m2, mock.MagicMock)
                    assert isinstance(m3, mock.MagicMock)
                    assert isinstance(m4, mock.MagicMock)

```

---

# Patch & Mock

## Patch

### Patch hell

La alternativa `patch.multiple`:

---

# Patch & Mock

## Patch

### Patch hell

La alternativa `patch.multiple`:

```python

@mock.patch.multiple(
    FakeStore,
    namespace_exists=mock.DEFAULT,
    get=mock.DEFAULT,
    set_namespace=mock.DEFAULT,
    count=mock.DEFAULT,
)
def test_multimock(**mocks):
    namespace_exists, get, set_namespace, count = mocks.values()
    assert isinstance(namespace_exists, mock.MagicMock)
    assert isinstance(get, mock.MagicMock)
    assert isinstance(set_namespace, mock.MagicMock)
    assert isinstance(count, mock.MagicMock)
```

---

# Patch & Mock

## Patch

### Patch hell

_Ejemplo 14_

```bash
poetry run pytest mock_patch/14-patch-hell.py
```

---

# Raising exceptions

---

# Raising exceptions

```python
import pytest


def raise_exception():
    raise Exception("error")


def test_raises_exception():
    with pytest.raises(Exception) as error:
        raise_exception()
        assert str(error.value) == "Some other string"
```

---

_Ejemplo 15_

```bash
poetry run pytest exceptions/15-raise-exception.py
```

---

# Raising exceptions

```python
import pytest


def raise_exception():
    raise Exception("error")


def test_raises_exception():
    with pytest.raises(Exception) as error:
        raise_exception()

    # Assert outside of the raises context manager
    assert str(error.value) == "Some other string"
```

---

# Raising exceptions

_Ejemplo 16_

```bash
poetry run pytest exceptions/16-raise-exception-ok.py
```

---

# Datetime

---

# Datetime

```python
import datetime
from freezegun import freeze_time
from datetime import timedelta


def day_tomorrow(today):
    return today + timedelta(days=1)


def test_date_naive():
    today = datetime.datetime.today()
    day_tomorrow = day_tomorrow(today)

    assert tomorrow.day == 2

```

---

# Datetime

_Ejemplo 16_

```bash
poetry run pytest time_examples/16-dates.py
```

---

# Datetime

Alternativas

---

# Datetime

Alternativas

```python
import datetime
from freezegun import freeze_time
def test_day_injection():
    today = datetime.datetime(2021, 10, 2)
    tomorrow = day_tomorrow(today)

    assert tomorrow == 3

```

---

# Datetime

Alternativas

```python
import datetime
from freezegun import freeze_time

@freeze_time("2021-10-02")
def test_date_naive():
    today = datetime.datetime.today()
    tomorrow = day_tomorrow(today)

    assert tomorrow == 3
```

---

# Datetime

_Ejemplo 17_

```bash
poetry run pytest time_examples/17-dates.py
```

---

# Buenas prácticas en CI (Continuous Integration)

---

# Buenas prácticas en CI (Continuous Integration)

## Test coverage

- 100% test coverage no implica 100% de calidad.

---

# Buenas prácticas en CI (Continuous Integration)

## Test coverage

- 100% test coverage no implica 100% de calidad.
  - Sin embargo, es buena práctica tener un mínimo nivel que nos permita garantizar la cobertura del código.

---

# Buenas prácticas en CI (Continuous Integration)

## Test coverage

- 100% test coverage no implica 100% de calidad.
  - Sin embargo, es buena práctica tener un mínimo nivel que nos permita garantizar la cobertura del código.
- Coverage _>80%_ o _>90%_ suele ser lo más recomendado en backend.

---

# Buenas prácticas en CI (Continuous Integration)

## Test coverage

- 100% test coverage no implica 100% de calidad.
  - Sin embargo, es buena práctica tener un mínimo nivel que nos permita garantizar la cobertura del código.
- Coverage _>80%_ o _>90%_ suele ser lo más recomendado en backend.
- Con librerías como pytest podemos pedir un mínimo de coverage en CI:

```bash

pytest --cov-fail-under=90
```

---

# Buenas prácticas en CI (Continuous Integration)

## Paralelización de pruebas

---

# Buenas prácticas en CI (Continuous Integration)

## Paralelización de pruebas

### pytest

---

# Buenas prácticas en CI (Continuous Integration)

## Paralelización de pruebas

### pytest

Con `pytest-xdist` puedes ejecutar pruebas paralelas especificando el número de cores:

```bash
poetry run pytest -n2 isolation/1-patch.py
```

---

# Buenas prácticas en CI (Continuous Integration)

## Paralelización de pruebas

### Django

---

# Buenas prácticas en CI (Continuous Integration)

## Paralelización de pruebas

### Django

```bash
python manage.py test --parallel
```

---

# Buenas prácticas en CI (Continuous Integration)

## Test reports

- Incluye _coverage reports_ que indiquen el nivel de cobertura del código y las líneas cubiertas.

```bash
poetry run pytest --cov=. isolation/1-patch.py
```

---

# Buenas prácticas en CI (Continuous Integration)

## Test reports

- Incluye _coverage reports_ que indiquen el nivel de cobertura del código y las líneas cubiertas.

```bash
poetry run pytest --cov=. isolation/1-patch.py
```

- Reporte de flaky/heisen tests

---

# ¡Muchas gracias!

## ¿Preguntas?
