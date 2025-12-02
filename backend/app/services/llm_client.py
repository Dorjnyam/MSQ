"""Shared Gemini client and model configuration."""

from google import genai

from app.config import settings

GEMINI_MODEL = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

