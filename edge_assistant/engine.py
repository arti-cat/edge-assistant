from __future__ import annotations
from contextlib import suppress
from typing import Any, Dict, Iterable, List, Optional
import os
from pathlib import Path


class Engine:
    """Light wrapper around the OpenAI Responses client.

    The OpenAI client is created lazily so importing the CLI module
    (for --help or tests) does not require OPENAI_API_KEY to be set.
    """

    def __init__(self, model_default: str = "gpt-4o-mini"):
        self._client_inst = None
        self.model_default = model_default
        self._load_dotenv()

    def _load_dotenv(self):
        """Load environment variables from .env file if it exists."""
        try:
            from dotenv import load_dotenv
            
            # Look for .env file in current directory and parent directories
            env_path = Path.cwd() / ".env"
            if env_path.exists():
                load_dotenv(env_path)
            else:
                # Check parent directories up to project root
                current = Path.cwd()
                for parent in current.parents:
                    env_path = parent / ".env"
                    if env_path.exists():
                        load_dotenv(env_path)
                        break
                    # Stop at git root or when we find pyproject.toml
                    if (parent / ".git").exists() or (parent / "pyproject.toml").exists():
                        break
        except ImportError:
            # python-dotenv not installed, skip silently
            pass

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
    def upload_for_kb(self, path) -> str:
        with open(path, "rb") as f:
            file = self._get_client().files.create(file=f, purpose="file_search")
        return file.id

    def analyze_image(self, image_path: str, user_prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None):
        """Analyze an image with optional system and user prompts using vision capabilities."""
        import base64
        from pathlib import Path
        
        # Read and encode image
        img_path = Path(image_path)
        if not img_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        with open(img_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Determine image format
        file_extension = img_path.suffix.lower()
        if file_extension in ['.jpg', '.jpeg']:
            mime_type = "image/jpeg"
        elif file_extension == '.png':
            mime_type = "image/png"
        elif file_extension == '.gif':
            mime_type = "image/gif"
        elif file_extension == '.webp':
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"  # default fallback
        
        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({
            "role": "user", 
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}"
                    }
                },
                {
                    "type": "text",
                    "text": user_prompt
                }
            ]
        })
        
        # Use vision model by default
        vision_model = model or "gpt-4o"
        
        # Send to OpenAI via responses API
        response = self._get_client().chat.completions.create(
            model=vision_model,
            messages=messages,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
