from fastapi import APIRouter, HTTPException
from ..models.schemas import KnowledgeGraphResponse, SearchRequest, SearchResponse
from ..services.knowledge_graph import kg_service
from typing import List, Dict, Any

router = APIRouter()

@router.get("/", response_model=KnowledgeGraphResponse)
async def get_knowledge_graph(limit: int = 100):
    """Get the current knowledge graph"""
    try:
        return kg_service.get_knowledge_graph(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=SearchResponse)
async def search_entities(request: SearchRequest):
    """Search for entities in the knowledge graph"""
    try:
        results = kg_service.search_entities(request.query, request.limit)
        return SearchResponse(results=results, total_count=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/entity/{entity_id}")
async def get_entity_details(entity_id: str):
    """Get details and connections for a specific entity"""
    try:
        connections = kg_service.get_entity_connections(entity_id)
        return {"entity_id": entity_id, "connections": connections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/entity")
async def create_entity(name: str, entity_type: str, properties: Dict[str, Any] = None):
    """Manually create an entity"""
    try:
        entity_id = kg_service.create_entity(name, entity_type, properties)
        return {"entity_id": entity_id, "message": "Entity created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/relationship")
async def create_relationship(start_entity: str, end_entity: str, 
                            relationship_type: str, properties: Dict[str, Any] = None):
    """Manually create a relationship between entities"""
    try:
        success = kg_service.create_relationship(start_entity, end_entity, relationship_type, properties)
        if success:
            return {"message": "Relationship created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create relationship")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_graph_stats():
    """Get statistics about the knowledge graph"""
    try:
        stats_query = """
        MATCH (n:Entity)
        OPTIONAL MATCH (n)-[r]-()
        RETURN 
            count(DISTINCT n) as total_entities,
            count(DISTINCT r) as total_relationships,
            collect(DISTINCT labels(n)) as entity_types
        """
        
        from ..core.database import db
        result = db.execute_query(stats_query)
        if result:
            stats = result[0]
            return {
                "total_entities": stats["total_entities"],
                "total_relationships": stats["total_relationships"] // 2,  # Divide by 2 because each relationship is counted twice
                "entity_types": [label for sublist in stats["entity_types"] for label in sublist if label != "Entity"]
            }
        return {"total_entities": 0, "total_relationships": 0, "entity_types": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))