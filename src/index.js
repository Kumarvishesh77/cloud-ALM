import { argv } from "process";
import {
  summarizeText,
  generateIssueDescription,
  fetchWorkItem,
} from "./cloudAlmClaude.js";

const [, , command, ...args] = argv;

async function run() {
  if (command === "prompt") {
    const text = args[0];
    const titleIndex = args.indexOf("--title");
    let title;
    let promptText = text;

    if (titleIndex !== -1) {
      title = args[titleIndex + 1];
      promptText = args.slice(0, titleIndex).join(" ");
    }

    if (!promptText) {
      console.error("Usage: node src/index.js prompt <text> [--title <title>]");
      process.exit(1);
    }

    if (title) {
      const result = await generateIssueDescription(title, promptText);
      console.log(result);
    } else {
      const result = await summarizeText(promptText);
      console.log(result);
    }
  } else if (command === "summarize") {
    const workItemId = args[0];
    if (!workItemId) {
      console.error("Usage: node src/index.js summarize <work_item_id>");
      process.exit(1);
    }
    const workItem = await fetchWorkItem(workItemId);
    const content = `Title: ${workItem.title || ""}\nDescription: ${workItem.description || ""}`;
    const summary = await summarizeText(content, "SAP Cloud ALM work item");
    console.log(summary);
  } else {
    console.error("Commands: prompt, summarize");
    console.error("Example: node src/index.js prompt \"Describe this issue\"");
    process.exit(1);
  }
}

run().catch((error) => {
  console.error(error?.response?.data ?? error.message ?? error);
  process.exit(1);
});
