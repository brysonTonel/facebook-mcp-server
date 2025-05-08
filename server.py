from mcp.server.fastmcp import FastMCP
from manager import Manager
from typing import Any

mcp = FastMCP("Demo")
manager = Manager()

@mcp.tool()
def post_to_facebook(message: str) -> dict[str, Any]:
    """Create a new Facebook Page post with a text message.
    Input: message (str)
    Output: dict with post ID and creation status
    """
    return manager.post_to_facebook(message)

@mcp.tool()
def reply_to_comment(post_id: str, comment_id: str, message: str) -> dict[str, Any]:
    """Reply to a specific comment on a Facebook post.
    Input: post_id (str), comment_id (str), message (str)
    Output: dict with reply creation status
    """
    return manager.reply_to_comment(post_id, comment_id, message)

@mcp.tool()
def get_page_posts() -> dict[str, Any]:
    """Fetch the most recent posts on the Page.
    Input: None
    Output: dict with list of post objects and metadata
    """
    return manager.get_page_posts()

@mcp.tool()
def get_post_comments(post_id: str) -> dict[str, Any]:
    """Retrieve all comments for a given post.
    Input: post_id (str)
    Output: dict with comment objects
    """
    return manager.get_post_comments(post_id)

@mcp.tool()
def delete_post(post_id: str) -> dict[str, Any]:
    """Delete a specific post from the Facebook Page.
    Input: post_id (str)
    Output: dict with deletion result
    """
    return manager.delete_post(post_id)

@mcp.tool()
def delete_comment(comment_id: str) -> dict[str, Any]:
    """Delete a specific comment from the Page.
    Input: comment_id (str)
    Output: dict with deletion result
    """
    return manager.delete_comment(comment_id)

@mcp.tool()
def delete_comment_from_post(post_id: str, comment_id: str) -> dict[str, Any]:
    """Alias to delete a comment on a post.
    Input: post_id (str), comment_id (str)
    Output: dict with deletion result
    """
    return manager.delete_comment_from_post(post_id, comment_id)

@mcp.tool()
def filter_negative_comments(comments: dict[str, Any]) -> list[dict[str, Any]]:
    """Filter comments for basic negative sentiment.
    Input: comments (dict)
    Output: list of flagged negative comments
    """
    return manager.filter_negative_comments(comments)

@mcp.tool()
def get_number_of_comments(post_id: str) -> int:
    """Count the number of comments on a given post.
    Input: post_id (str)
    Output: integer count of comments
    """
    return manager.get_number_of_comments(post_id)

@mcp.tool()
def get_number_of_likes(post_id: str) -> int:
    """Return the number of likes on a post.
    Input: post_id (str)
    Output: integer count of likes
    """
    return manager.get_number_of_likes(post_id)

@mcp.tool()
def get_post_insights(post_id: str) -> dict[str, Any]:
    """Fetch all insights metrics (impressions, reactions, clicks, etc).
    Input: post_id (str)
    Output: dict with multiple metrics and their values
    """
    return manager.get_post_insights(post_id)