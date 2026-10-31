import json
import re
from typing import Any

from google import genai
from google.genai import types

from config import Settings, settings


class LLMError(RuntimeError):
    """User-safe error raised for expected provider failures."""


class LLMClient:
    def __init__(self, configuration: Settings = settings):
        self.configuration = configuration

        if not configuration.is_configured:
            raise LLMError(
                "LLM API configuration is missing. "
                "Add LLM_API_KEY and LLM_MODEL."
            )

        try:
            # Gemini client
            self.client = genai.Client(
                api_key=configuration.api_key,
                http_options=types.HttpOptions(
                    timeout=configuration.timeout_seconds * 1000
                ),
            )

        except Exception as exc:
            print("\n========== GEMINI CLIENT ERROR ==========")
            print(type(exc).__name__)
            print(str(exc))
            print("=========================================\n")

            raise LLMError(
                "Unable to initialize the Gemini API client. "
                "Check your API key."
            ) from exc

    def complete_json(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> Any:

        try:
            response = self.client.models.generate_content(
                model=self.configuration.model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.4,
                    response_mime_type="application/json",
                ),
            )

            content = (response.text or "").strip()

            if not content:
                raise LLMError(
                    "The LLM returned an empty response."
                )

            # Strip markdown code blocks if the model wrapped output
            if "```" in content:
                match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
                if match:
                    content = match.group(1).strip()

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Robust extraction: find outer boundaries
                start_brace = content.find("{")
                start_bracket = content.find("[")
                if start_brace != -1 and (start_bracket == -1 or start_brace < start_bracket):
                    end_brace = content.rfind("}")
                    if end_brace != -1:
                        return json.loads(content[start_brace:end_brace + 1])
                elif start_bracket != -1:
                    end_bracket = content.rfind("]")
                    if end_bracket != -1:
                        return json.loads(content[start_bracket:end_bracket + 1])
                raise

        except json.JSONDecodeError as exc:
            raise LLMError(
                "The LLM returned invalid JSON."
            ) from exc

        except Exception as exc:
            print("\n========== GEMINI ERROR ==========")
            print(type(exc).__name__)
            print(str(exc))
            print("==================================\n")

            message = str(exc).lower()

            if "429" in message or "resource_exhausted" in message:
                detail = (
                    "Gemini API rate limit reached. "
                    "Please wait and try again."
                )

            elif "401" in message or "403" in message:
                detail = (
                    "Gemini API authentication failed. "
                    "Check your API key and API project."
                )

            elif "404" in message or "not found" in message:
                detail = (
                    "The Gemini model was not found. "
                    "Check the LLM_MODEL value."
                )

            elif "timeout" in message:
                detail = (
                    "The Gemini request timed out. "
                    "Please try again."
                )

            elif "api key" in message:
                detail = (
                    "There is a problem with your Gemini API key. "
                    "Check your .env file."
                )

            else:
                detail = (
                    "Unable to reach Gemini API right now. "
                    "Check your API configuration and try again."
                )

            raise LLMError(detail) from exc
