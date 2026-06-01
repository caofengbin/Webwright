"""DeepSeek OpenAI-compatible chat completions model backend."""

from __future__ import annotations

from typing import Any

from webwright.models.base import (
    BaseModel,
    BaseModelConfig,
    OptStr,
    _safe_int,
)

__all__ = [
    "DeepSeekModel",
    "DeepSeekModelConfig",
]


def _serialize_chat_content_part(part: dict[str, Any]) -> dict[str, Any] | None:
    part_type = part.get("type")
    if part_type in {"input_text", "output_text"}:
        return {"type": "text", "text": str(part.get("text", "") or "")}
    if part_type == "input_image":
        return {
            "type": "image_url",
            "image_url": {
                "url": str(part.get("image_url", "") or ""),
                "detail": str(part.get("detail", "high") or "high"),
            },
        }
    return None


def _serialize_chat_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []
    for message in messages:
        role = message["role"]
        if role == "exit":
            continue
        mapped_role = "system" if role == "system" else ("assistant" if role == "assistant" else "user")
        content = message.get("content", "")
        if isinstance(content, str):
            serialized.append({"role": mapped_role, "content": content})
            continue
        parts = [
            serialized_part
            for part in content
            if isinstance(part, dict)
            for serialized_part in [_serialize_chat_content_part(part)]
            if serialized_part is not None
        ]
        if mapped_role == "assistant" or all(part.get("type") == "text" for part in parts):
            serialized.append(
                {
                    "role": mapped_role,
                    "content": "\n".join(str(part.get("text", "") or "") for part in parts),
                }
            )
        else:
            serialized.append({"role": mapped_role, "content": parts})
    return serialized


def _metrics_input_from_chat_messages(chat_messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics_input: list[dict[str, Any]] = []
    for message in chat_messages:
        content = message.get("content", "")
        if isinstance(content, str):
            metrics_input.append({"content": [{"type": "input_text", "text": content}]})
            continue
        parts: list[dict[str, Any]] = []
        for part in content:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "text":
                parts.append({"type": "input_text", "text": str(part.get("text", "") or "")})
            elif part.get("type") == "image_url":
                parts.append({"type": "input_image"})
        metrics_input.append({"content": parts})
    return metrics_input


def _extract_chat_completions_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""
    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        return ""
    message = first_choice.get("message", {})
    if not isinstance(message, dict):
        return ""
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            str(part.get("text", "") or "")
            for part in content
            if isinstance(part, dict) and part.get("type") == "text"
        )
    return ""


def _usage_metrics_from_chat_completions(payload: dict[str, Any]) -> dict[str, int]:
    usage = payload.get("usage")
    if not isinstance(usage, dict):
        usage = {}
    completion_details = usage.get("completion_tokens_details")
    if not isinstance(completion_details, dict):
        completion_details = {}
    return {
        "input_tokens": _safe_int(usage.get("prompt_tokens")),
        "output_tokens": _safe_int(usage.get("completion_tokens")),
        "total_tokens": _safe_int(usage.get("total_tokens")),
        "cached_input_tokens": 0,
        "reasoning_output_tokens": _safe_int(completion_details.get("reasoning_tokens")),
    }


class DeepSeekModelConfig(BaseModelConfig):
    model_name: OptStr = "deepseek-v4-flash"
    deepseek_api_key: OptStr = ""
    deepseek_endpoint: OptStr = "https://api.deepseek.com/chat/completions"


class DeepSeekModel(BaseModel):
    _API_KEY_FIELD = "deepseek_api_key"
    _ENV_VAR = "DEEPSEEK_API_KEY"
    _LOG_SOURCE = "deepseek"
    _MAX_RATE_LIMIT_RETRIES = 5
    _MAX_TRANSIENT_RETRIES = 5
    _DEFAULT_CONFIG_CLASS = DeepSeekModelConfig

    def _request_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.deepseek_api_key}",
        }

    def _post_url(self) -> str:
        return self.config.deepseek_endpoint

    def _build_payload(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "model": self.config.model_name,
            "messages": _serialize_chat_messages(messages),
            "stream": False,
            "max_tokens": self.config.max_output_tokens,
            "response_format": {"type": "json_object"},
        }

    def _build_text_payload(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "model": self.config.model_name,
            "messages": _serialize_chat_messages(messages),
            "stream": False,
            "max_tokens": self.config.max_output_tokens,
        }

    def _request_metrics_input(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        return _metrics_input_from_chat_messages(payload.get("messages") or [])

    def _extract_text(self, payload: dict[str, Any]) -> str:
        return _extract_chat_completions_text(payload)

    def _usage_metrics_from_payload(self, payload: dict[str, Any]) -> dict[str, int]:
        return _usage_metrics_from_chat_completions(payload)
