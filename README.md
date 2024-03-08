# david-szalai-qokoon

## Setup

Be sure to use a virtual environment:
> ```sh
> $ python3 -m venv venv
> ```
Here, `venv` is just an example, the virtual environment can be given *any* name.

To activate the virtual environment, run the following command:
> ```sh
> $ source venv/bin/activate
> ```

Upon activation, run `pip list`. Only `pip` and `setuptools` should be installed in the virtual environment.

To install requirements, run:
> ```sh
> $ pip install -r requirements.txt
> ```

Run `pip list` again, the virtual environment should contain `annotated-types`, `anyio`, `certifi`, `click`, `exceptiongroup`, `fastapi`, `h11`, `httpcore`, `httpx`, `idna`, `iniconfig`, `numpy`, `packaging`, `pandas`, `pluggy`, `pydantic`, `pydantic-core`, `pytest`, `python-dateutil`, `pytz`, `six`, `sniffio`, `starlette`, `tomli`, `typing-extensions`, `tzdata`, and `uvicorn`.

## TESTING:

# /cash-flow

The use of [Postman](https://www.postman.com/) is recommended for endpoint testing.

To test the `/cash-flow` endpoint, the parameters need to be formatted like so:

```json
{
  "type": "quarterly",
  "start_date": "2019-04-01"
}
```

## API TESTING:

To test the API endpoints, open the repo in VSCode (or something similar) and run the following:
> ```sh
> $ pytest endpoint_test.py
> ```