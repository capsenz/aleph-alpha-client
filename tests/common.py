import os
from typing import AsyncIterable, Iterable
import pytest
from aleph_alpha_client import AlephAlphaClient, AsyncClient
from aleph_alpha_client.aleph_alpha_client import Client

from aleph_alpha_client.aleph_alpha_model import AlephAlphaModel


@pytest.fixture(scope="session")
def client() -> Iterable[AlephAlphaClient]:
    api_url = get_env_var("TEST_API_URL")

    username = os.environ.get("TEST_USERNAME")
    password = os.environ.get("TEST_PASSWORD")
    token = os.environ.get("TEST_TOKEN")
    if username is not None and password is not None:
        token = None
    elif token is not None:
        username = None
        password = None
    else:
        raise ValueError(
            "Test parameters could not be read from .env. Make sure to create a .env file with either the key TEST_TOKEN or the keys TEST_USERNAME and TEST_PASSWORD."
        )

    client = AlephAlphaClient(
        host=api_url, token=token, email=username, password=password
    )

    yield client


@pytest.fixture(scope="session")
def sync_client() -> Client:
    return Client(token=get_env_var("TEST_TOKEN"), host=get_env_var("TEST_API_URL"))


@pytest.fixture()
async def async_client() -> AsyncIterable[AsyncClient]:
    async with AsyncClient(
        token=get_env_var("TEST_TOKEN"), host=get_env_var("TEST_API_URL")
    ) as client:
        yield client


@pytest.fixture(scope="session")
def model_name() -> str:
    return "luminous-base"


@pytest.fixture(scope="session")
def checkpoint_name() -> str:
    return get_env_var("TEST_CHECKPOINT")


@pytest.fixture(scope="session")
def qa_checkpoint_name() -> str:
    return get_env_var("TEST_CHECKPOINT_QA")


@pytest.fixture(scope="session")
def summarization_checkpoint_name() -> str:
    return get_env_var("TEST_CHECKPOINT_SUMMARIZATION")


@pytest.fixture(scope="session")
def alt_complete_checkpoint_name() -> str:
    return get_env_var("TEST_CHECKPOINT_ALT_COMPLETE")


@pytest.fixture(scope="session")
def alt_complete_adapter_name() -> str:
    return get_env_var("TEST_ADAPTER_ALT_COMPLETE")


def get_env_var(env_var: str) -> str:
    value = os.environ.get(env_var)
    if value is None:
        raise ValueError(
            f"Test parameters could not be read from .env. Make sure to create a .env file with the key {env_var}"
        )
    return value


@pytest.fixture(scope="session")
def model(client: AlephAlphaClient, model_name: str) -> AlephAlphaModel:
    return AlephAlphaModel(client, model_name)


@pytest.fixture(scope="session")
def luminous_base(client: AlephAlphaClient) -> AlephAlphaModel:
    return AlephAlphaModel(client, "luminous-base")


@pytest.fixture(scope="session")
def luminous_extended(client: AlephAlphaClient) -> AlephAlphaModel:
    return AlephAlphaModel(client, "luminous-extended")
