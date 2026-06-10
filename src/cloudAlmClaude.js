import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const ANTHROPIC_MODEL = process.env.ANTHROPIC_MODEL || "claude-3.5";
const SAP_CLOUD_ALM_API_BASE_URL = process.env.SAP_CLOUD_ALM_API_BASE_URL;
const SAP_CLOUD_ALM_API_TOKEN = process.env.SAP_CLOUD_ALM_API_TOKEN;

if (!ANTHROPIC_API_KEY) {
  throw new Error("ANTHROPIC_API_KEY is required in .env");
}

if (!SAP_CLOUD_ALM_API_BASE_URL || !SAP_CLOUD_ALM_API_TOKEN) {
  throw new Error("SAP_CLOUD_ALM_API_BASE_URL and SAP_CLOUD_ALM_API_TOKEN are required in .env");
}

const anthropicClient = axios.create({
  baseURL: "https://api.anthropic.com/v1",
  headers: {
    "x-api-key": ANTHROPIC_API_KEY,
    "Content-Type": "application/json",
  },
});

const cloudAlmClient = axios.create({
  baseURL: SAP_CLOUD_ALM_API_BASE_URL.replace(/\/$/, ""),
  headers: {
    Authorization: `Bearer ${SAP_CLOUD_ALM_API_TOKEN}`,
    "Content-Type": "application/json",
  },
});

export async function summarizeText(text, context = "") {
  const prompt = `\nHuman: You are a SAP Cloud ALM integration assistant. Generate a concise summary of the following work item details and highlight any recommended actions.\n\nContext:\n${context}\n\nWork item content:\n${text}\n\nAssistant:`;
  const response = await anthropicClient.post("/complete", {
    model: ANTHROPIC_MODEL,
    prompt,
    max_tokens_to_sample: 400,
    temperature: 0.3,
  });
  return response.data?.completion?.trim() ?? "";
}

export async function generateIssueDescription(title, details) {
  const prompt = `\nHuman: You are a SAP Cloud ALM integration assistant. Create a clear, professional issue description that can be posted into SAP Cloud ALM.\n\nTitle:\n${title}\n\nDetails:\n${details}\n\nAssistant:`;
  const response = await anthropicClient.post("/complete", {
    model: ANTHROPIC_MODEL,
    prompt,
    max_tokens_to_sample: 400,
    temperature: 0.4,
  });
  return response.data?.completion?.trim() ?? "";
}

export async function fetchWorkItem(workItemId) {
  const response = await cloudAlmClient.get(`/workitems/${encodeURIComponent(workItemId)}`);
  return response.data;
}

export async function createComment(workItemId, comment) {
  const response = await cloudAlmClient.post(
    `/workitems/${encodeURIComponent(workItemId)}/comments`,
    { text: comment }
  );
  return response.data;
}

export async function createWorkItem(title, description) {
  const response = await cloudAlmClient.post("/workitems", {
    title,
    description,
  });
  return response.data;
}
