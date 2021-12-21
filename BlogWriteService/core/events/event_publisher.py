from fastapi import Request
from .published import *
from .models import *
from core.posts.models import BlogPost
from core.comments.models import Comment
from common.broker.client import BrokerClient
from common.enums import *


class EventPublisher:
    
    def __init__(self, request: Request):
        self.broker: BrokerClient = request.app.broker_client
        
    async def _publish_event(self, body: str, routing_key: str, message_id: str):
        await self.broker.send_message(body, routing_key, 'blog_write', message_id)
        
    async def publish_blog_post_created(self, instance: BlogPost):
        message_schema = BlogPostCreated.from_orm(instance)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_blog_post_updated(self, instance: BlogPost):
        message_schema = BlogPostUpdated.from_orm(instance)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_blog_post_deleted(self, post_id: int):
        message_schema = BlogPostDeleted(post_id=post_id)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_comment_created(self, instance: Comment):
        message_schema = CommentCreated.from_orm(instance)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_comment_updated(self, instance: Comment):
        message_schema = CommentUpdated.from_orm(instance)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_comment_deleted(self, post_id: int, comment_id: int):
        message_schema = CommentDeleted(post_id=post_id, comment_id=comment_id)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)