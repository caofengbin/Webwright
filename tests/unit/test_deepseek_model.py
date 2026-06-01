import pytest

from webwright.models import get_model
from webwright.models.deepseek_model import DeepSeekModel


def test_deepseek_model_reads_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-secret")

    model = get_model({"model_class": "deepseek"})

    assert isinstance(model, DeepSeekModel)
    assert model.config.deepseek_api_key == "deepseek-secret"
    assert model.config.model_name == "deepseek-v4-flash"
    assert model._post_url() == "https://api.deepseek.com/chat/completions"


def test_deepseek_model_accepts_config_overrides() -> None:
    model = DeepSeekModel(
        deepseek_api_key="deepseek-secret",
        model_name="deepseek-v4-pro",
        deepseek_endpoint="https://example.com/chat/completions",
        max_output_tokens=1234,
    )

    assert model.config.deepseek_api_key == "deepseek-secret"
    assert model.config.model_name == "deepseek-v4-pro"
    assert model._post_url() == "https://example.com/chat/completions"


def test_deepseek_payload_uses_chat_completions_json_object() -> None:
    model = DeepSeekModel(deepseek_api_key="deepseek-secret", max_output_tokens=1234)

    payload = model._build_payload(
        [
            {"role": "system", "content": "Respond with JSON."},
            {"role": "user", "content": [{"type": "input_text", "text": "next step"}]},
        ]
    )

    assert payload["model"] == "deepseek-v4-flash"
    assert payload["stream"] is False
    assert payload["max_tokens"] == 1234
    assert payload["response_format"] == {"type": "json_object"}
    assert payload["messages"] == [
        {"role": "system", "content": "Respond with JSON."},
        {"role": "user", "content": "next step"},
    ]


def test_deepseek_text_payload_omits_response_format() -> None:
    model = DeepSeekModel(deepseek_api_key="deepseek-secret")

    payload = model._build_text_payload([{"role": "user", "content": "summarize"}])

    assert "response_format" not in payload
    assert payload["messages"] == [{"role": "user", "content": "summarize"}]


def test_deepseek_extracts_text_usage_and_redacts_key() -> None:
    model = DeepSeekModel(deepseek_api_key="deepseek-secret")
    response = {
        "choices": [{"message": {"content": "{\"done\": true}"}}],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
            "completion_tokens_details": {"reasoning_tokens": 2},
        },
    }

    assert model._extract_text(response) == '{"done": true}'
    assert model._usage_metrics_from_payload(response) == {
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15,
        "cached_input_tokens": 0,
        "reasoning_output_tokens": 2,
    }
    assert model.serialize()["model"]["config"]["deepseek_api_key"] == "<redacted>"
