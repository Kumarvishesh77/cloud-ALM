# cloud-ALM
SAP CLOUD ALM

## Claude AI Integration
This repository now includes a sample integration between Claude AI and SAP Cloud ALM.

### What is included
- `cloud_alm_claude.py`: Python Claude and Cloud ALM client wrappers
- `main.py`: Python CLI for summaries and issue generation
- `requirements.txt`: Python dependencies
- `package.json`: Node.js project manifest
- `src/cloudAlmClaude.js`: Node.js Claude and Cloud ALM client wrappers
- `src/index.js`: Node.js CLI entrypoint
- `.env.example`: environment settings for Claude and SAP Cloud ALM

### Setup
1. Copy `.env.example` to `.env`
2. Set `ANTHROPIC_API_KEY`, `SAP_CLOUD_ALM_API_BASE_URL`, and `SAP_CLOUD_ALM_API_TOKEN`

#### Python
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Node.js
3. Install Node.js dependencies (Node 18+):
   ```bash
   npm install
   ```

### Usage
- Summarize an ALM work item:
  ```bash
  python main.py summarize <work_item_id>
  ```
- Send a custom text prompt to Claude:
  ```bash
  python main.py prompt "Describe this issue in professional language"
  ```
- Generate an issue description with a title:
  ```bash
  python main.py prompt "Detailed issue description text" --title "Issue title"
  ```

### Notes
- The Cloud ALM client uses placeholder REST endpoints such as `/workitems/{id}` and `/workitems/{id}/comments`.
- Adjust endpoint URLs and payload shapes to match your SAP Cloud ALM API.
