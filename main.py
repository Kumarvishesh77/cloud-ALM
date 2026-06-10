import argparse
import os

from cloud_alm_claude import ClaudeClient, CloudALMClient, summarize_cloud_alm_work_item


def main() -> None:
    parser = argparse.ArgumentParser(description="Claude AI integration for Cloud ALM")
    subparsers = parser.add_subparsers(dest="command")

    prompt_parser = subparsers.add_parser("prompt", help="Send a custom prompt to Claude")
    prompt_parser.add_argument("text", help="Text to summarize or transform")
    prompt_parser.add_argument("--title", help="Title for issue description generation")

    summary_parser = subparsers.add_parser("summarize", help="Summarize a Cloud ALM work item")
    summary_parser.add_argument("work_item_id", help="Cloud ALM work item ID to summarize")

    args = parser.parse_args()

    if args.command == "prompt":
        claude = ClaudeClient()
        if args.title:
            output = claude.generate_issue_description(args.title, args.text)
        else:
            output = claude.summarize(args.text)
        print(output)
    elif args.command == "summarize":
        print(summarize_cloud_alm_work_item(args.work_item_id))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
