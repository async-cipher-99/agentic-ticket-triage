from __future__ import annotations

from typing import Dict, List


def detect_language(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ["hola", "gracias", "mi paquete", "necesitamos", "por favor"]):
        return "es"
    if any(token in lowered for token in ["wir", "für", "audit", "danke", "benötigen"]):
        return "de"
    if any(token in lowered for token in ["nous", "besoin", "ligne", "pièces", "délai"]):
        return "fr"
    return "en"


def translate_if_needed(text: str, target_lang: str) -> str:
    return text if target_lang == "en" else f"[{target_lang}] {text}"


def supported_languages() -> Dict[str, List[str]]:
    return {
        "acme_corp": ["en", "es"],
        "globex_manufacturing": ["en", "de", "fr"],
    }
