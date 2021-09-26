---
theme: "./theme.json"
author: Ismael Mendonça
date: Oct 2, 2021
paging: Slide %d / %d
---

# Python testing best practices

## Agenda

- Testing principles
- Librerías
- Patch & Mock
- Tests funcionales vs Tests basados en clases
- TestCase classes
- setUp and tearDown
- Parametrización
- Recomendaciones para tu CI
- Gotchas

---

# Testing principles

## Test isolation

Las pruebas no deben producir "side-effects" sobre otras pruebas.

Posibles causas...

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas.

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

### Patch que permanece activo entre varias pruebas.

_Example 1_

```bash
poetry run pytest isolation/1-patch.py

```

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas.

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

### Patch que permanece activo entre varias pruebas.

_Example 2_

```bash
poetry run pytest isolation/2-patch-ok.py

```

---

# Testing principles

## Test isolation

### Patch que permanece activo entre varias pruebas.

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

### Patch que permanece activo entre varias pruebas.

_Example 3_

```bash
poetry run pytest isolation/3-patch-ok.py

```

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas.

```python
def test_create_user():
    user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

    assert user.username == "ismaelmt"

    assert user.email == "ismael@ismael.com"
    assert UserStore.count() == 1


def test_user_amount():

    # We want that each test have a clean DB
    # This test will fail, but it shouldn't.
    assert FakeStore.count() == 0
```

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas.

_Example 4_

```bash
poetry run pytest isolation/4-db.py

```

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas.

```python
@pytest.fixture(autouse=True)
def db_fixture():

    yield

    FakeStore.clean()


def test_create_user():
    user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

    assert user.username == "ismaelmt"

    assert user.email == "ismael@ismael.com"
    assert UserStore.count() == 1


def test_user_amount():

    # We want that each test have a clean DB
    # This test will fail, but it shouldn't.
    assert FakeStore.count() == 0

```

---

# Testing principles

## Test isolation

### Datos que persisten entre pruebas.

_Example 5_

```bash
poetry run pytest isolation/5-db-ok.py

```

---

# Testing principles

## Test isolation

### Compartir estado entre pruebas dentro de una clase.

```python
class TestLeakUsers:
    def setup_class(self):
        self.user = {"name": "Lola Mento", "username": "iamauser@user.com"}


    def test_username(self):
        self.user["name"] = "Elsa Murito"
        assert self.user["username"] == "iamauser@user.com"


    def test_name(self):
        # Capasao!??
        assert self.user["name"] == "Lola Mento"

```

- Si necesitas compartir estado, hazlo solo para leerlo durante las pruebas, no lo modifiques!

---

# Testing principles

## Test isolation

### Compartir estado entre pruebas dentro de una clase.

_Example 6_

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

Las pruebas unitarias deben:

- _Tratarse como cajas negras_
  - Evita modificar métodos internos o estados.
- _Pequeñas y bien enfocadas_
  - Pruebas muy grandes usualmente es un indicador de código mal estructurado.
- _Rápidas_
  - "Una prueba que dura más de 0.1 segundos ya no es considerada unitaria"

---

# Testing principles

## Recomendaciones generales

- _Tu código debe SIEMPRE incluir pruebas_
  - Una base de código sin pruebas, debe asumirse como defectuosa.
- _El código de pruebas debe tratarse como código de producto_
  - Principios como YAGNI, KISS, DRY y los patrones de diseño de aplicaciones, deben ser tomados en cuenta durante pruebas.

---

# Frameworks y Librerías

Principales librerías y frameworks:

### Frameworks

- pytest
- unittest
- Nose
- Nose2
  ...

### Librerías

- unittest.mock
- pytest-mock
  ...

---

# Frameworks y Librerías

Principales librerías y frameworks:

### Frameworks

- pytest
- unittest
- ~~Nose~~
- ~~Nose2~~
  ...

### Librerías

- unittest.mock
- ~~pytest-mock~~
  ...

---

# Functional vs class-based tests

```python
# pytest function
def test_get_fake_store():
    user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

    assert FakeStore.get("users", "1") == user


# pytest class
class TestFakeStorePytest:
    @pytest.fixture(autouse=True)
    def fake_store(self):
        FakeStore.clean()

    def test_get_fake_store_in_class(self):

        user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

        assert FakeStore.get("users", "1") == user


# unittest class
class TestFakeStore(TestCase):
    def setUp(self):
        FakeStore.clean()

    def test_get_fake_store_in_class(self):

        user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

        assert FakeStore.get("users", "1") == user
```

---

# Functional vs class-based tests

```bash
poetry run pytest ./class_test/7-class-fun.py
```

---

# Functional vs class-based tests

- `pytest`: Permite escribir tests como funciones o como clases.
- `unittest.TestCase`: Todas las pruebas son escritas en clases.

Tus pruebas son una ventana a tu código, tus pruebas sirven de documentación sobre el uso de tu código.

Las siguientes son recomendaciones generales:

- Utiliza clases como una forma de agrupación semántica de tus pruebas.
- Si necesitas compartir estado entre pruebas (setup, class attribute), utiliza clases.
- Si necesitas ejecutar un conjunto de pruebas en un mismo core, utiliza clases.
- Usa `fixtures` para código que necesites reusar entre funciones o métodos.

---

# Patch & Mock

## Mocking

Recordando...

- unittest.mock ✓
- ~~pytest-mock~~
  - Provee un fixture llamado `mocker`

`mocker`: Automáticamente deshace el mock al final del test.

Conveniente, pero puede resultar _contraproducente_ en equipos grandes de ingenieria.

- Confusión entre `unittest.mock` y `mocker`. No funcionan bien en conjunto.

---

# Patch & Mock

## Mocking

_Example 8_

```python
def test_mocker_context(mocker):
    with mocker.patch.object(UserStore, "count"):
        assert isinstance(UserStore.count, mocker.MagicMock)
```

---

# Patch & Mock

## Mocking

Probamos...

```bash
poetry run pytest mock_patch/8-mocker.py

```

---

# Patch & Mock

## Mocking

_Example 9_

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

Probamos...

```bash
poetry run pytest mock_patch/9-mocker.py

```

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

## Patch hell

_Example 10_

```bash
poetry run pytest mock_patch/10-patch-hell.py
```

---

# setup & teardown

Si necesitas datos para tus tests, utiliza los metodos setup y teardown para preparar y limpiar los datos respectivamente.

## pytest

_Recomendado_

- En pytest nos valemos de `fixtures`. Puedes crear una fixture que realice tanto el setup como el teardown.

```python
@pytest.fixture
def db(autouse=True, scope="function"):

    # setup
    UserStore.create_user(username="test_user", email="test@example.com")

    yield

    #teardown
    FakeStore.clean()
```

- Diferentes scopes: `package`, `session`, `class`, `module`, `function`.

_No recomendado_

- O puedes usar también setup y teardown al estilo xunit:
  - `setup_class`, `setup_module`, `setup_function`
  - `teardown_class`, `teardown_module`, `teardown_function`

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

# Buenas prácticas en CI (Continuous Integration)

## Test coverage

- 100% test coverage no implica 100% de calidad.
  - Sin embargo, es buena práctica tener un mínimo nivel que nos permita garantizar la cobertura del código.
- Coverage _>80%_ o _>90%_ suele ser lo más recomendado en backend.
- Con librerías como pytest podemos pedir un mínimo de coverage en CI:

Procura que el "step" de testing en tu CI garantice un nivel "aceptable" de _coverage_:

```bash

pytest --cov-fail-under=90
```

---

# Buenas prácticas en CI (Continuous Integration)

## Paralelización de pruebas

### pytest

Con `pytest-xdist` puedes ejecutar pruebas paralelas especificando el número de cores:

```bash
poetry run pytest -n2 isolation/1-patch.py
```

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
