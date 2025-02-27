import pytest
from aleph_alpha_client import ExplanationRequest, AlephAlphaClient
from aleph_alpha_client.aleph_alpha_client import AsyncClient, Client
from aleph_alpha_client.aleph_alpha_model import AlephAlphaModel
from aleph_alpha_client.prompt import Prompt

from tests.common import (
    sync_client,
    client,
    model_name,
    model,
    checkpoint_name,
    async_client,
)


# AsynClient


async def test_can_explain_with_async_client(
    async_client: AsyncClient, model_name: str
):
    request = ExplanationRequest(
        prompt=Prompt.from_text("An apple a day"),
        target=" keeps the doctor away",
        suppression_factor=0.1,
    )

    response = await async_client._explain(request, model=model_name)
    assert response.result


async def test_can_explain_with_async_client_against_checkpoint(
    async_client: AsyncClient,
    checkpoint_name: str,
):
    request = ExplanationRequest(
        prompt=Prompt.from_text("An apple a day"),
        target=" keeps the doctor away",
        suppression_factor=0.1,
    )

    response = await async_client._explain(request, checkpoint=checkpoint_name)
    assert response.result


# Client


def test_explanation(sync_client: Client, model_name: str):
    request = ExplanationRequest(
        prompt=Prompt.from_text("An apple a day"),
        target=" keeps the doctor away",
        suppression_factor=0.1,
    )

    explanation = sync_client._explain(request, model=model_name)

    assert len(explanation.result) > 0


def test_explanation_against_checkpoint(sync_client: Client, checkpoint_name: str):
    request = ExplanationRequest(
        prompt=Prompt.from_text("An apple a day"),
        target=" keeps the doctor away",
        suppression_factor=0.1,
    )
    explanation = sync_client._explain(request, checkpoint=checkpoint_name)

    assert len(explanation.result) > 0


# AlephAlphaClient


def test_explanation_with_client_against_checkpoint(
    client: AlephAlphaClient, checkpoint_name: str
):

    request = ExplanationRequest(
        prompt=Prompt.from_text("An apple a day"),
        target=" keeps the doctor away",
        suppression_factor=0.1,
    )

    explanation = client._explain(
        model=None, request=request, checkpoint=checkpoint_name
    )

    # List is true if not None and not empty
    assert explanation["result"]
