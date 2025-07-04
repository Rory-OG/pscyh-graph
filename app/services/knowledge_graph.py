from typing import List, Dict, Any, Tuple
from ..core.database import db
from ..models.schemas import KnowledgeGraphNode, KnowledgeGraphRelationship, KnowledgeGraphResponse
import logging

logger = logging.getLogger(__name__)

class KnowledgeGraphService:
    def __init__(self):
        self.initialize_constraints()
    
    def initialize_constraints(self):
        """Initialize database constraints and indexes"""
        queries = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Concept) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Note) REQUIRE n.id IS UNIQUE",
            "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.name)",
            "CREATE INDEX IF NOT EXISTS FOR (n:Concept) ON (n.name)",
        ]
        
        for query in queries:
            try:
                db.execute_query(query)
            except Exception as e:
                logger.warning(f"Failed to execute constraint query: {e}")
    
    def create_entity(self, name: str, entity_type: str, properties: Dict[str, Any] = None) -> str:
        """Create a new entity in the knowledge graph"""
        if properties is None:
            properties = {}
        
        entity_id = f"{entity_type}_{name}".replace(" ", "_").lower()
        properties.update({
            "id": entity_id,
            "name": name,
            "type": entity_type,
            "created_at": "datetime()"
        })
        
        query = f"""
        MERGE (e:Entity::{entity_type} {{id: $id}})
        SET e += $properties
        RETURN e.id as id
        """
        
        result = db.execute_query(query, {"id": entity_id, "properties": properties})
        return result[0]["id"] if result else entity_id
    
    def create_relationship(self, start_entity: str, end_entity: str, 
                          relationship_type: str, properties: Dict[str, Any] = None) -> bool:
        """Create a relationship between two entities"""
        if properties is None:
            properties = {}
        
        properties["created_at"] = "datetime()"
        
        query = f"""
        MATCH (a:Entity {{id: $start_id}})
        MATCH (b:Entity {{id: $end_id}})
        MERGE (a)-[r:{relationship_type}]->(b)
        SET r += $properties
        RETURN r
        """
        
        try:
            result = db.execute_query(query, {
                "start_id": start_entity,
                "end_id": end_entity,
                "properties": properties
            })
            return len(result) > 0
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            return False
    
    def get_knowledge_graph(self, limit: int = 100) -> KnowledgeGraphResponse:
        """Get the current knowledge graph structure"""
        # Get nodes
        nodes_query = """
        MATCH (n:Entity)
        RETURN id(n) as node_id, n.id as id, labels(n) as labels, properties(n) as properties
        LIMIT $limit
        """
        
        # Get relationships
        relationships_query = """
        MATCH (a:Entity)-[r]->(b:Entity)
        RETURN id(r) as rel_id, type(r) as type, 
               a.id as start_node_id, b.id as end_node_id, 
               properties(r) as properties
        LIMIT $limit
        """
        
        nodes_result = db.execute_query(nodes_query, {"limit": limit})
        relationships_result = db.execute_query(relationships_query, {"limit": limit})
        
        nodes = [
            KnowledgeGraphNode(
                id=node["id"],
                labels=node["labels"],
                properties=node["properties"]
            )
            for node in nodes_result
        ]
        
        relationships = [
            KnowledgeGraphRelationship(
                id=str(rel["rel_id"]),
                type=rel["type"],
                start_node_id=rel["start_node_id"],
                end_node_id=rel["end_node_id"],
                properties=rel["properties"]
            )
            for rel in relationships_result
        ]
        
        return KnowledgeGraphResponse(nodes=nodes, relationships=relationships)
    
    def search_entities(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for entities in the knowledge graph"""
        search_query = """
        MATCH (n:Entity)
        WHERE n.name CONTAINS $query OR any(prop in keys(n) WHERE n[prop] CONTAINS $query)
        RETURN n.id as id, n.name as name, n.type as type, properties(n) as properties
        LIMIT $limit
        """
        
        return db.execute_query(search_query, {"query": query, "limit": limit})
    
    def get_entity_connections(self, entity_id: str) -> Dict[str, Any]:
        """Get all connections for a specific entity"""
        query = """
        MATCH (e:Entity {id: $entity_id})
        OPTIONAL MATCH (e)-[r1]->(connected)
        OPTIONAL MATCH (connected2)-[r2]->(e)
        RETURN e as entity,
               collect(DISTINCT {relationship: r1, connected: connected, direction: 'outgoing'}) as outgoing,
               collect(DISTINCT {relationship: r2, connected: connected2, direction: 'incoming'}) as incoming
        """
        
        result = db.execute_query(query, {"entity_id": entity_id})
        return result[0] if result else {}

# Global service instance
kg_service = KnowledgeGraphService()