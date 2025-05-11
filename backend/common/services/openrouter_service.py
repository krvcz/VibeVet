import logging
from decimal import Decimal
import json
from typing import Dict, Any
from django.conf import settings
from django.core.exceptions import ValidationError
import requests
from requests.exceptions import RequestException

logger = logging.getLogger('common')

class OpenRouterValidationError(ValidationError):
    """Custom exception for OpenRouter validation errors"""

class OpenRouterProcessingError(Exception):
    """Custom exception for OpenRouter processing errors"""

class OpenRouterService:
    """Service for handling communication with OpenRouter API"""
    
    def __init__(
        self, 
        api_url: str = None,
        api_key: str = None,
        default_model: str = "openai/gpt-3.5-turbo",
        default_params: Dict[str, Any] = None
    ):
        """Initialize the OpenRouter service with configuration."""
        self.api_url = api_url or settings.OPENROUTER_API_URL
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.default_model = default_model
        self.default_params = default_params or {
            "temperature": 0.7,
            "max_tokens": 1500,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "localhost"
        }
        
    def send_openrouter_request(
        self,
        system_message: str,
        user_message: str,
        response_format: dict,
        model_name: str = None,
        model_params: dict = None
    ) -> dict:
        """Send a request to OpenRouter API."""
        try:
            if response_format is None:
                payload = self._prepare_payload_plain_text(
                    system_message,
                    user_message,
                    model_name or self.default_model,
                    model_params or self.default_params
                )
            else:
                payload = self._prepare_payload_json_schema(
                    system_message,
                    user_message,
                    response_format,
                    model_name or self.default_model,
                    model_params or self.default_params
                )
            
            logger.info(
                "Sending OpenRouter request for model %s: %s",
                payload["model"],
                user_message[:100]
            )
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(
                    "OpenRouter API error %d: %s",
                    response.status_code,
                    response.text
                )
                raise OpenRouterProcessingError(
                    f"API returned status code {response.status_code}"
                )
                
            result = response.json()

            return self.parse_response(result, response_format)
            
        except RequestException as e:
            logger.error("OpenRouter request failed: %s", str(e))
            raise OpenRouterProcessingError("Failed to connect to OpenRouter API") from e
        except ValueError as e:
            logger.error("OpenRouter response parsing failed: %s", str(e))
            raise OpenRouterProcessingError("Failed to parse OpenRouter response") from e
        except Exception as e:
            logger.error("Unexpected error in OpenRouter request: %s", str(e))
            raise

    def parse_response(self, response: dict, response_format: dict) -> dict:
        """Parse and validate the API response."""
        try:
            # Extract the actual response content from the OpenRouter response structure
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not content:
                raise OpenRouterValidationError("Empty response from OpenRouter API")
            
            if response_format is None:
                # If no response format is specified, return the raw content
                return content
                
            # Parse the content as JSON
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error("Failed to parse response JSON: %s\nContent: %s", str(e), content)
                raise OpenRouterValidationError("Invalid JSON in response") from e
            
            # Validate against the schema
            schema = response_format["json_schema"]["schema"]
            self._validate_against_schema(parsed_content, schema)
            
            return parsed_content
            
        except KeyError as e:
            logger.error("Missing required field in response: %s", str(e))
            raise OpenRouterValidationError("Response missing required field") from e
        except Exception as e:
            logger.error("Response validation failed: %s", str(e))
            raise OpenRouterValidationError("Response validation failed") from e

    def _prepare_payload_json_schema(
        self,
        system_message: str,
        user_message: str,
        response_format: dict,
        model_name: str,
        model_params: dict
    ) -> dict:
        """Prepare the API request payload."""
        if not system_message or not user_message:
            raise OpenRouterValidationError("Both system_message and user_message are required")
            
        # Format response requirements into the system message
        format_instructions = json.dumps(response_format["json_schema"], indent=2)
        system_message = f"{system_message}\n\nYour response must strictly follow this JSON schema:\n{format_instructions}"
        
        return {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "response_format": response_format,
            **model_params
        }
    
    def _prepare_payload_plain_text(
        self,
        system_message: str,
        user_message: str,
        model_name: str,
        model_params: dict
    ) -> dict:
        """Prepare the API request payload."""
        if not system_message or not user_message:
            raise OpenRouterValidationError("Both system_message and user_message are required")
        
        return {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            **model_params
        }

    def _validate_against_schema(self, data: dict, schema: dict) -> None:
        """Validate response data against the schema."""
        if not isinstance(data, dict):
            raise OpenRouterValidationError("Response data must be an object")
            
        properties = schema.get("properties", {})
        required = schema.get("required", list(properties.keys()))
        
        # Check required fields
        for field in required:
            if field not in data:
                raise OpenRouterValidationError(f"Missing required field: {field}")
        
        # Validate property types and constraints
        for field, value in data.items():
            if field not in properties:
                if not schema.get("additionalProperties", True):
                    raise OpenRouterValidationError(f"Additional property not allowed: {field}")
                continue
                
            field_schema = properties[field]
            field_type = field_schema.get("type")
            
            if field_type == "number":
                if not isinstance(value, (int, float, Decimal)):
                    raise OpenRouterValidationError(
                        f"Field {field} should be a number, got {type(value).__name__}"
                    )
                    
                # Validate number constraints
                if "minimum" in field_schema and value < field_schema["minimum"]:
                    raise OpenRouterValidationError(
                        f"Field {field} must be >= {field_schema['minimum']}"
                    )
                if "maximum" in field_schema and value > field_schema["maximum"]:
                    raise OpenRouterValidationError(
                        f"Field {field} must be <= {field_schema['maximum']}"
                    )
                    
            elif field_type == "string":
                if not isinstance(value, str):
                    raise OpenRouterValidationError(
                        f"Field {field} should be a string, got {type(value).__name__}"
                    )
                    
                # Validate string constraints
                if "enum" in field_schema and value not in field_schema["enum"]:
                    raise OpenRouterValidationError(
                        f"Field {field} must be one of: {', '.join(field_schema['enum'])}"
                    )