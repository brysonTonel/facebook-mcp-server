from flask import Flask, request, jsonify
import asyncio
import json
import logging
from functools import wraps
import traceback
from manager import Manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class FacebookMCPWrapper:
    def __init__(self):
        # Initialize your Manager which handles the Facebook API
        self.manager = Manager()
    
    def call_tool(self, tool_name, arguments):
        """
        Route tool calls to your Manager methods
        """
        try:
            # Map tool names to manager methods
            tool_mapping = {
                # Post operations
                "post_to_facebook": lambda args: self.manager.post_to_facebook(args.get('message')),
                "post_image_to_facebook": lambda args: self.manager.post_image_to_facebook(
                    args.get('image_url'), args.get('caption', '')
                ),
                "schedule_post": lambda args: self.manager.schedule_post(
                    args.get('message'), args.get('publish_time')
                ),
                "update_post": lambda args: self.manager.update_post(
                    args.get('post_id'), args.get('new_message')
                ),
                "delete_post": lambda args: self.manager.delete_post(args.get('post_id')),
                
                # Comment operations
                "reply_to_comment": lambda args: self.manager.reply_to_comment(
                    args.get('post_id'), args.get('comment_id'), args.get('message')
                ),
                "delete_comment": lambda args: self.manager.delete_comment(args.get('comment_id')),
                "delete_comment_from_post": lambda args: self.manager.delete_comment_from_post(
                    args.get('post_id'), args.get('comment_id')
                ),
                "filter_negative_comments": lambda args: self.manager.filter_negative_comments(
                    args.get('comments', {})
                ),
                
                # Get operations
                "get_page_posts": lambda args: self.manager.get_page_posts(),
                "get_post_comments": lambda args: self.manager.get_post_comments(args.get('post_id')),
                "get_number_of_comments": lambda args: self.manager.get_number_of_comments(args.get('post_id')),
                "get_number_of_likes": lambda args: self.manager.get_number_of_likes(args.get('post_id')),
                "get_post_top_commenters": lambda args: self.manager.get_post_top_commenters(args.get('post_id')),
                "get_page_fan_count": lambda args: self.manager.get_page_fan_count(),
                "get_post_share_count": lambda args: self.manager.get_post_share_count(args.get('post_id')),
                
                # Insights operations
                "get_post_insights": lambda args: self.manager.get_post_insights(args.get('post_id')),
                "get_post_impressions": lambda args: self.manager.get_post_impressions(args.get('post_id')),
                "get_post_impressions_unique": lambda args: self.manager.get_post_impressions_unique(args.get('post_id')),
                "get_post_impressions_paid": lambda args: self.manager.get_post_impressions_paid(args.get('post_id')),
                "get_post_impressions_organic": lambda args: self.manager.get_post_impressions_organic(args.get('post_id')),
                "get_post_engaged_users": lambda args: self.manager.get_post_engaged_users(args.get('post_id')),
                "get_post_clicks": lambda args: self.manager.get_post_clicks(args.get('post_id')),
                
                # Reaction operations
                "get_post_reactions_like_total": lambda args: self.manager.get_post_reactions_like_total(args.get('post_id')),
                "get_post_reactions_love_total": lambda args: self.manager.get_post_reactions_love_total(args.get('post_id')),
                "get_post_reactions_wow_total": lambda args: self.manager.get_post_reactions_wow_total(args.get('post_id')),
                "get_post_reactions_haha_total": lambda args: self.manager.get_post_reactions_haha_total(args.get('post_id')),
                "get_post_reactions_sorry_total": lambda args: self.manager.get_post_reactions_sorry_total(args.get('post_id')),
                "get_post_reactions_anger_total": lambda args: self.manager.get_post_reactions_anger_total(args.get('post_id')),
                
                # Messaging
                "send_dm_to_user": lambda args: self.manager.send_dm_to_user(
                    args.get('user_id'), args.get('message')
                ),
            }
            
            if tool_name not in tool_mapping:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            # Execute the tool
            result = tool_mapping[tool_name](arguments)
            return result
        
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {str(e)}")
            raise
    
    def list_tools(self):
        """List all available tools with their descriptions and parameters"""
        return [
            # Post operations
            {
                "name": "post_to_facebook",
                "description": "Create a new Facebook Page post with a text message",
                "parameters": {
                    "message": {"type": "string", "required": True, "description": "The message to post"}
                }
            },
            {
                "name": "post_image_to_facebook",
                "description": "Post an image with a caption to the Facebook page",
                "parameters": {
                    "image_url": {"type": "string", "required": True, "description": "URL of the image to post"},
                    "caption": {"type": "string", "required": False, "description": "Caption for the image"}
                }
            },
            {
                "name": "schedule_post",
                "description": "Schedule a new post for future publishing",
                "parameters": {
                    "message": {"type": "string", "required": True, "description": "The message to schedule"},
                    "publish_time": {"type": "integer", "required": True, "description": "Unix timestamp for when to publish"}
                }
            },
            {
                "name": "update_post",
                "description": "Update an existing post's message",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post to update"},
                    "new_message": {"type": "string", "required": True, "description": "New message content"}
                }
            },
            {
                "name": "delete_post",
                "description": "Delete a specific post from the Facebook Page",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post to delete"}
                }
            },
            
            # Comment operations
            {
                "name": "reply_to_comment",
                "description": "Reply to a specific comment on a Facebook post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"},
                    "comment_id": {"type": "string", "required": True, "description": "ID of the comment to reply to"},
                    "message": {"type": "string", "required": True, "description": "Reply message"}
                }
            },
            {
                "name": "delete_comment",
                "description": "Delete a specific comment from the Page",
                "parameters": {
                    "comment_id": {"type": "string", "required": True, "description": "ID of the comment to delete"}
                }
            },
            {
                "name": "delete_comment_from_post",
                "description": "Delete a comment from a specific post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"},
                    "comment_id": {"type": "string", "required": True, "description": "ID of the comment to delete"}
                }
            },
            {
                "name": "filter_negative_comments",
                "description": "Filter comments for basic negative sentiment",
                "parameters": {
                    "comments": {"type": "object", "required": True, "description": "Comments object to filter"}
                }
            },
            
            # Get operations
            {
                "name": "get_page_posts",
                "description": "Fetch the most recent posts on the Page",
                "parameters": {}
            },
            {
                "name": "get_post_comments",
                "description": "Retrieve all comments for a given post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_number_of_comments",
                "description": "Count the number of comments on a given post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_number_of_likes",
                "description": "Return the number of likes on a post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_top_commenters",
                "description": "Get the top commenters on a post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_page_fan_count",
                "description": "Get the Page's total fan/like count",
                "parameters": {}
            },
            {
                "name": "get_post_share_count",
                "description": "Get the number of shares for a post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            
            # Insights operations
            {
                "name": "get_post_insights",
                "description": "Fetch all insights metrics (impressions, reactions, clicks, etc)",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_impressions",
                "description": "Fetch total impressions of a post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_impressions_unique",
                "description": "Fetch unique impressions of a post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_impressions_paid",
                "description": "Fetch paid impressions of a post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_impressions_organic",
                "description": "Fetch organic impressions of a post",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_engaged_users",
                "description": "Fetch number of engaged users",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_clicks",
                "description": "Fetch number of post clicks",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            
            # Reaction operations
            {
                "name": "get_post_reactions_like_total",
                "description": "Fetch number of 'Like' reactions",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_reactions_love_total",
                "description": "Fetch number of 'Love' reactions",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_reactions_wow_total",
                "description": "Fetch number of 'Wow' reactions",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_reactions_haha_total",
                "description": "Fetch number of 'Haha' reactions",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_reactions_sorry_total",
                "description": "Fetch number of 'Sorry' reactions",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            {
                "name": "get_post_reactions_anger_total",
                "description": "Fetch number of 'Anger' reactions",
                "parameters": {
                    "post_id": {"type": "string", "required": True, "description": "ID of the post"}
                }
            },
            
            # Messaging
            {
                "name": "send_dm_to_user",
                "description": "Send a direct message to a user",
                "parameters": {
                    "user_id": {"type": "string", "required": True, "description": "ID of the user to message"},
                    "message": {"type": "string", "required": True, "description": "Message to send"}
                }
            }
        ]

# Initialize the wrapper
mcp_wrapper = FacebookMCPWrapper()

def sync_route(f):
    """Decorator to handle synchronous routes in Flask"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in route: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    return wrapper

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'facebook-mcp-wrapper',
        'version': '1.0.0'
    })

@app.route('/tools', methods=['GET'])
def list_tools():
    """List available MCP tools"""
    try:
        tools = mcp_wrapper.list_tools()
        return jsonify({
            'success': True,
            'tools': tools,
            'count': len(tools)
        })
    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tools/<tool_name>', methods=['POST'])
@sync_route
def execute_tool(tool_name):
    """Execute a specific MCP tool"""
    # Get arguments from request body
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body must be valid JSON'
        }), 400
    
    arguments = data.get('arguments', {})
    
    # Log the request
    logger.info(f"Executing tool: {tool_name} with arguments: {arguments}")
    
    try:
        # Execute the tool
        result = mcp_wrapper.call_tool(tool_name, arguments)
        
        return jsonify({
            'success': True,
            'tool': tool_name,
            'data': result
        })
    
    except ValueError as e:
        # Tool not found
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    
    except Exception as e:
        # Other errors
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tools/batch', methods=['POST'])
@sync_route
def execute_batch():
    """Execute multiple tools in batch"""
    data = request.get_json()
    if not data or 'tools' not in data:
        return jsonify({
            'success': False,
            'error': 'Request must contain "tools" array'
        }), 400
    
    results = []
    for tool_request in data['tools']:
        tool_name = tool_request.get('name')
        arguments = tool_request.get('arguments', {})
        
        try:
            result = mcp_wrapper.call_tool(tool_name, arguments)
            results.append({
                'tool': tool_name,
                'success': True,
                'data': result
            })
        except Exception as e:
            results.append({
                'tool': tool_name,
                'success': False,
                'error': str(e)
            })
    
    return jsonify({
        'success': True,
        'results': results
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    logger.info("Starting Facebook MCP HTTP Wrapper...")
    logger.info(f"Available tools: {len(mcp_wrapper.list_tools())}")
    app.run(host='0.0.0.0', port=5000, debug=True)