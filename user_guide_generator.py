import streamlit as st
from github import Github
from notion_client import Client
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize GitHub API with token
gh_token = os.getenv('GITHUB_TOKEN')
g = Github(gh_token)  # Initialize Github object with the token
openai_api_key = os.getenv('OPENAI_API_KEY')

def is_ui_ux_pr(pr_link: str) -> bool:
    """
    Determines if the given PR is related to UI/UX changes.
    
    Args:
        pr_link (str): The link to the GitHub Pull Request.
        
    Returns:
        bool: True if the PR is related to UI/UX, False otherwise.
    """
    # TODO: Implement logic to check if PR is UI/UX related
    pass

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
                    
                    pr_details = {} # TODO: Fetch PR details from GitHub using the Github object
                    
                    updated_guide = update_user_guide(existing_guide, pr_details)
                    
                    st.markdown(updated_guide)
                    
                    if st.button("Confirm and Update on Notion"):
                        post_updated_guide_to_notion(notion_api_details, updated_guide)
                        st.success("User guide updated successfully on Notion!")
                        
        else:
            st.warning("The PR is not related to UI/UX changes.")
            
if __name__ == "__main__":
    main()
