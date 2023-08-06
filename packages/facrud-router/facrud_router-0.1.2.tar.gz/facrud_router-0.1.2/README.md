<p align="center">
  <a href="https://pypi.org/project/facrud-router" style="font-size: 7vw">facrud-router</a>
</p>
<div align="center">
  <a href="https://pypi.org/project/facrud-router" target="_blank">
      <img src="https://img.shields.io/pypi/pyversions/facrud-router.svg?color=%2334D058" alt="Supported Python versions">
  </a>
</div>

---

**Source
Code**: <a href="https://github.com/drtnn/facrud-router" target="_blank">https://github.com/drtnn/facrud-router</a>

---

## Requirements

Python 3.9+

facrud-router stands on the shoulders of giants:

* <a href="https://fastapi.tiangolo.com/" class="external-link" target="_blank">FastAPI</a>
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>
* <a href="https://docs.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>

## Installation

<div class="termy">

```console
$ pip install facrud-router

---> 100%
```

</div>

## Example

### Create it

* Create a file `main.py` with:

```Python
import uuid
from dataclasses import dataclass
from dataclasses import field

import uvicorn
from facrud_router import ModelCRUDRouter
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.api.deps import get_session
from app.api.deps import authentication_scheme

app = FastAPI(
    title="FastAPI CURD Router Demo",
    version="0.1.2",
    description="FastAPI CRUD Router for SQLAlchemy",
    openapi_url="/openapi.json",
    docs_url="/",
)


@dataclass
class User:
    __sa_dataclass_metadata_key__ = "sa"
    __tablename__ = "user"

    id: uuid.UUID = field(
        init=False,
        default_factory=uuid.uuid4,
        metadata={"sa": Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)},
    )
    username: str = field(metadata={"sa": Column(String(255), nullable=False, index=True)})
    full_name: str = field(metadata={"sa": Column(String(255), nullable=False)})


class UserRequestSchema(BaseModel):
    username: str = Field(title="Username", max_length=255)
    full_name: str = Field(title="User Full Name", max_length=255)


class UserResponseSchema(BaseModel):
    id: uuid.UUID = Field(title="User Id")
    username: str = Field(title="Username", max_length=255)
    full_name: str = Field(title="User Full Name", max_length=255)


router = ModelCRUDRouter(
    prefix="user",
    model=User,
    identifier_type=uuid.UUID,
    get_session=get_session,
    get_authentication=authentication_scheme,
    request_schema=UserRequestSchema,
    response_schema=UserResponseSchema
)

app.include_router(router.api_router)

if __name__ == "__main__":
    uvicorn.run(app)
```

### Run it

Run the server with:

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

### Check it

You already created an API that:

* GET `/user/{user_id}` retrieves User object by UUID.
* GET `/user` returns list of User objects.
* POST `/user` creates User object.
* DELETE `/user/{user_id}` deletes User object by UUID.
* PUT `/user/{user_id}` updates User object by UUID.
* PATCH `/user/{user_id}` partial updates User object by UUID.

### Interactive API docs

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

You will see the automatic interactive API documentation (provided
by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://s277iva.storage.yandex.net/rdisk/39f77d6a2a593fcede3451e4194b5c1a053d36e5cd19df08aefcb71c86462a16/639a5c01/Mi8za20nmVQrIk4Fir018ergP14R4XLjm1uJKqpk3XOveziTE8zylkfyZXMhjEI8Lo-1k6j_qfSKDKxzgrX-nQ==?uid=0&filename=Снимок%20экрана%202022-12-14%20в%2022.27.48.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&fsize=294734&hid=6c672c8a77ee2319904796e479f32ca5&media_type=image&tknv=v2&etag=6caedc9763924ef4f783c454bacd5280&rtoken=k4U9Mma4C5VY&force_default=no&ycrid=na-ba31b448645bc9c9ebc720e5b053697c-downloader1e&ts=5efd2165e4240&s=6256b791ad3cf37e9e0ad18aafb43cbaaba7fd482ef308966b55d70fbc76d3b6&pb=U2FsdGVkX1_7XtCdPrLpy5WEc4mK7uDBcLcXGBLcy3mWB3nbjWhWx3c_S30YJv8mSie8ZL_Q0AmgK5XH_cesURROSl2UAOBZbp-l_JY77ZE)

## License

This project is licensed under the terms of the Apache License 2.0.