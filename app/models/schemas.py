from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    timestamp: Optional[datetime] = None

class ChatResponse(BaseModel):
    response: str
    entities_extracted: List[Dict[str, Any]]
    relationships_created: List[Dict[str, Any]]
    timestamp: datetime

class Entity(BaseModel):
    id: str
    label: str
    properties: Dict[str, Any]

class Relationship(BaseModel):
    id: str
    type: str
    start_node: str
    end_node: str
    properties: Dict[str, Any]

class KnowledgeGraphNode(BaseModel):
    id: str
    labels: List[str]
    properties: Dict[str, Any]

class KnowledgeGraphRelationship(BaseModel):
    id: str
    type: str
    start_node_id: str
    end_node_id: str
    properties: Dict[str, Any]

class KnowledgeGraphResponse(BaseModel):
    nodes: List[KnowledgeGraphNode]
    relationships: List[KnowledgeGraphRelationship]

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_count: int