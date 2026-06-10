import os
from typing import Any, Dict, Optional

import anthropic
import requests
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3.5")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
        self.client = anthropic.Client(api_key=self.api_key)

    def summarize(self, text: str, context: str = "") -> str:
        prompt = (
            anthropic.HUMAN_PROMPT
            + "You are a SAP Cloud ALM integration assistant. Generate a concise summary of the following work item details and highlight any recommended actions."
            + "\n\nContext:\n"
            + context
            + "\n\nWork item content:\n"
            + text
            + "\n\nSummary:"
            + anthropic.AI_PROMPT
        )
        response = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=400,
            temperature=0.3,
        )
        return response.completion.strip()

    def generate_issue_description(self, title: str, details: str) -> str:
        prompt = (
            anthropic.HUMAN_PROMPT
            + "You are a SAP Cloud ALM integration assistant. Create a clear, professional issue description that can be posted into SAP Cloud ALM."
            + "\n\nTitle:\n"
            + title
            + "\n\nDetails:\n"
            + details
            + "\n\nIssue description:"
            + anthropic.AI_PROMPT
        )
        response = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=400,
            temperature=0.4,
        )
        return response.completion.strip()


class CloudALMClient:
    def __init__(self, base_url: Optional[str] = None, api_token: Optional[str] = None):
        self.base_url = base_url or os.getenv("SAP_CLOUD_ALM_API_BASE_URL")
        self.api_token = api_token or os.getenv("SAP_CLOUD_ALM_API_TOKEN")
        if not self.base_url or not self.api_token:
            raise ValueError("SAP_CLOUD_ALM_API_BASE_URL and SAP_CLOUD_ALM_API_TOKEN are required")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def fetch_work_item(self, work_item_id: str) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/workitems/{work_item_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def create_comment(self, work_item_id: str, comment: str) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/workitems/{work_item_id}/comments"
        payload = {"text": comment}
        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def create_work_item(self, title: str, description: str) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/workitems"
        payload = {"title": title, "description": description}
        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()


def summarize_cloud_alm_work_item(work_item_id: str) -> str:
    cloud_alm = CloudALMClient()
    claude = ClaudeClient()
    work_item = cloud_alm.fetch_work_item(work_item_id)

    title = work_item.get("title", "")
    description = work_item.get("description", "")
    details = f"Title: {title}\nDescription: {description}"

    summary = claude.summarize(details, context="SAP Cloud ALM work item")
    return summary
