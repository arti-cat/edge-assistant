from __future__ import annotations
from contextlib import suppress
from typing import Any, Dict, Iterable, List, Optional


class Engine:
    """Light wrapper around the OpenAI Responses client.

    The OpenAI client is created lazily so importing the CLI module
    (for --help or tests) does not require OPENAI_API_KEY to be set.
    """

    def __init__(self, model_default: str = "gpt-4o-mini"):
        self._client_inst = None
        self.model_default = model_default

    def _get_client(self):
        if self._client_inst is None:
            # import here to avoid raising on module import if OPENAI_API_KEY is missing
            from openai import OpenAI

            self._client_inst = OpenAI()
        return self._client_inst

    def send(
        self,
        input: Any,
        *,
        model: Optional[str] = None,
        instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        previous_response_id: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ):
        kwargs: Dict[str, Any] = {
            "model": model or self.model_default,
            "input": input,
        }
        if instructions:     kwargs["instructions"] = instructions
        if tools:            kwargs["tools"] = tools
        if attachments:      kwargs["attachments"] = attachments
        if previous_response_id: kwargs["previous_response_id"] = previous_response_id
        if response_format:  kwargs["response_format"] = response_format

        if stream:
            text_chunks: List[str] = []
            with self._get_client().responses.stream(**kwargs) as s:
                for event in s:
                    if event.type == "response.output_text.delta":
                        print(event.delta, end="", flush=True)
                        text_chunks.append(event.delta)
                    elif event.type == "response.error":
                        raise RuntimeError(event.error)
            print()
            with suppress(Exception):
                final = s.get_final_response()
                return final
            # Fallback: create pseudo response-like object
            class R: pass
            r = R()
            r.output_text = "".join(text_chunks)
            r.id = None
            r.output = []
            return r

        return self._get_client().responses.create(**kwargs)

    # Convenience
    # Convenience
    def upload_for_kb(self, path) -> str:
        with open(path, "rb") as f:
            file = self._get_client().files.create(file=f, purpose="file_search")
        return file.id
