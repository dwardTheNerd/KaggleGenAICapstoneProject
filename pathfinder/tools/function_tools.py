from google.adk.tools.function_tool import FunctionTool
from pathfinder.helpers.notion_helper import create_notion_page_from_md as md2notionpage
from pathfinder.helpers.notion_helper import search_pages_by_title

def create_notion_page(markdown_text, title, parent_page_id,):
    """
    Create a notion page from markdown text

    Args:
        markdown_text: String of the markdown text content to be written to the new page.
        title: Title for the new page.
        parent_page_id: The ID of the parent page under which the new page will be created.

    Return:
        URL of the created page
    """
    return md2notionpage(markdown_text=markdown_text, title=title, parent_page_id=parent_page_id)

def search_notion_pages(query):
    """
    Perform a search by title for Notion pages

    Args:
        query: Search string to perform the search
    
    Return:
        List of dict, with each dict containing basic page properties (id, object, title, url)
    """
    return search_pages_by_title(query)

create_notion_page_tool = FunctionTool(create_notion_page)
search_notion_pages_by_title_tool = FunctionTool(search_notion_pages)