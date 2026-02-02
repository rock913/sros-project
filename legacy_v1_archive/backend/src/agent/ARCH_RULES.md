# MPA Architecture Rules (Copilot Context)

## 1. Domain Layer (`domain/`)
- **Pure Python**: No heavy dependencies (LangChain, FastAPI, SQLAlchemy).
- **Schema First**: defining data structures using `pydantic.BaseModel`.
- **Protocol First**: Define behavior using `typing.Protocol` in `ports/`.
- **No I/O**: No database access, no http requests here.

## 2. Infrastructure Layer (`infrastructure/`)
- **Adapters**: Implement `ports/` protocols here.
- **Dependency Injection**: Classes should accept dependencies in `__init__`.
- **Tools**: Wrap external APIs here.

## 3. Testing
- **Speed**: Unit tests must run in < 0.1s.
- **Mocking**: strict usage of `unittest.mock` or `pytest-mock` to mock `ports`.
- **Forbidden**: Do not use real I/O in unit tests.

## 4. Code Style
- **Type Hints**: Mandatory for all function arguments and returns.
- **Docstrings**: Google style docstrings.
