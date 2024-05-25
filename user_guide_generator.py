import streamlit as st
from github import Github
import os
import json

from dotenv import load_dotenv

from models import completion_with_backoff

# Load environment variables from .env file
load_dotenv()

# Initialize GitHub API with token
gh_token = os.getenv("GITHUB_TOKEN")
g = Github(gh_token)  # Initialize Github object with the token
openai_api_key = os.getenv("OPENAI_API_KEY")


def extract_repo_and_pr_from_link(pr_link: str) -> tuple:
    """
    Extracts the repository path and pull request number from the given PR link.

    Args:
        pr_link (str): The link to the GitHub Pull Request.

    Returns:
        tuple: A tuple containing the repository path and pull request number.
    """
    # Split the PR link by '/'
    parts = pr_link.split("/")

    # Extract the repository path (owner/repo_name)
    repo_path = f"{parts[-4]}/{parts[-3]}"

    # Extract the pull request number
    pr_number = int(parts[-1])

    return repo_path, pr_number


def is_ui_ux_pr(pr_link: str) -> bool:
    """
    Determines if the given PR is related to UI/UX changes.

    Args:
        pr_link (str): The link to the GitHub Pull Request.

    Returns:
        bool: True if the PR is related to UI/UX, False otherwise.
    """
    # Extract the repo path and PR number from the PR link
    repo_path, pr_number = extract_repo_and_pr_from_link(pr_link)

    # Get the repo object
    repo = g.get_repo(repo_path)

    # Fetch pull request by number
    pull_request = repo.get_pull(pr_number)

    # Get the diffs of the pull request
    pull_request_diffs = [
        {"filename": file.filename, "patch": file.patch}
        for file in pull_request.get_files()
    ]

    # Get the commit messages associated with the pull request
    commit_messages = [commit.commit.message for commit in pull_request.get_commits()]

    # Format data for OpenAI prompt
    prompt = [
        {
            "role": "system",
            "content": "You are an AI assistant that determines if a pull request is related to UI/UX changes.",
        },
        {
            "role": "user",
            "content": f"Given the following pull request diffs and commit messages, determine if the pull request is related to UI/UX changes and provide your response in JSON format with 'is_ui_ux' as a boolean and 'reasoning' as a string explaining your decision:\n\nPull Request Diffs:\n{pull_request_diffs}\n\nCommit Messages:\n{commit_messages}",
        },
    ]

    # Call the OpenAI API to determine if the PR is UI/UX related
    openai_response = completion_with_backoff(prompt)

    # Parse the OpenAI response to get the classification result
    response_json = json.loads(openai_response)
    is_ui_ux = response_json["is_ui_ux"]
    reasoning = response_json["reasoning"]

    print(f"Is UI/UX related: {is_ui_ux}")
    print(f"Reasoning: {reasoning}")

    return is_ui_ux


def get_notion_api_details() -> dict:
    """
    Prompts the user for Notion API details.

    Returns:
        dict: A dictionary containing the Notion API details.
    """
    # TODO: Implement Streamlit UI to get Notion API details from user
    pass


def fetch_existing_user_guide(notion_api_details: dict) -> str:
    """
    Fetches the existing user guide from Notion.

    Args:
        notion_api_details (dict): A dictionary containing the Notion API details.

    Returns:
        str: The existing user guide content.
    """
    # TODO: Implement logic to fetch existing user guide from Notion
    pass


def update_user_guide(existing_guide: str, pr_details: dict) -> str:
    """
    Updates the user guide based on the PR details.

    Args:
        existing_guide (str): The existing user guide content.
        pr_details (dict): A dictionary containing the PR details.

    Returns:
        str: The updated user guide content.
    """
    # TODO: Implement logic to update user guide based on PR details
    pass


def post_updated_guide_to_notion(notion_api_details: dict, updated_guide: str) -> None:
    """
    Posts the updated user guide to Notion.

    Args:
        notion_api_details (dict): A dictionary containing the Notion API details.
        updated_guide (str): The updated user guide content.
    """
    # TODO: Implement logic to post updated user guide to Notion
    pass


def main():
    st.title("User Guide Generator")

    pr_link = st.text_input("Enter the PR link:")

    if pr_link:
        if is_ui_ux_pr(pr_link):
            st.success("The PR is related to UI/UX changes.")

            if st.button("Create/Update Usage Guide on Notion"):
                notion_api_details = get_notion_api_details()

                if notion_api_details:
                    existing_guide = fetch_existing_user_guide(notion_api_details)

                    pr_details = {}  # TODO: Fetch PR details from GitHub using the Github object

                    updated_guide = update_user_guide(existing_guide, pr_details)

                    st.markdown(updated_guide)

                    if st.button("Confirm and Update on Notion"):
                        post_updated_guide_to_notion(notion_api_details, updated_guide)
                        st.success("User guide updated successfully on Notion!")

        else:
            st.warning("The PR is not related to UI/UX changes.")


if __name__ == "__main__":
    main()
