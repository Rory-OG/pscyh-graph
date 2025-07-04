import re
import spacy
from typing import List, Dict, Any, Tuple
from datetime import datetime
from .knowledge_graph import kg_service
from ..models.schemas import ChatResponse
import logging

logger = logging.getLogger(__name__)

class ChatAgent:
    def __init__(self):
        self.nlp = None
        self.load_nlp_model()
        self.conversation_history = []
    
    def load_nlp_model(self):
        """Load spaCy NLP model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("SpaCy model not found. Using basic NLP processing.")
            self.nlp = None
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text using NLP"""
        entities = []
        
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "confidence": 1.0  # spaCy doesn't provide confidence scores directly
                })
        else:
            # Basic entity extraction using patterns
            entities.extend(self._extract_basic_entities(text))
        
        return entities
    
    def _extract_basic_entities(self, text: str) -> List[Dict[str, Any]]:
        """Basic entity extraction using regex patterns"""
        entities = []
        
        # Extract potential concepts (capitalized words/phrases)
        concept_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        concepts = re.findall(concept_pattern, text)
        
        for concept in concepts:
            entities.append({
                "text": concept,
                "label": "CONCEPT",
                "start": text.find(concept),
                "end": text.find(concept) + len(concept),
                "confidence": 0.8
            })
        
        # Extract dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'
        dates = re.findall(date_pattern, text)
        
        for date in dates:
            entities.append({
                "text": date,
                "label": "DATE",
                "start": text.find(date),
                "end": text.find(date) + len(date),
                "confidence": 0.9
            })
        
        return entities
    
    def extract_relationships(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relationships between entities"""
        relationships = []
        
        # Simple relationship extraction based on common patterns
        relationship_patterns = [
            (r'(\w+)\s+is\s+(?:a|an)\s+(\w+)', "IS_A"),
            (r'(\w+)\s+relates\s+to\s+(\w+)', "RELATES_TO"),
            (r'(\w+)\s+connects\s+to\s+(\w+)', "CONNECTS_TO"),
            (r'(\w+)\s+influences\s+(\w+)', "INFLUENCES"),
            (r'(\w+)\s+causes\s+(\w+)', "CAUSES"),
            (r'(\w+)\s+depends\s+on\s+(\w+)', "DEPENDS_ON"),
        ]
        
        for pattern, rel_type in relationship_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                relationships.append({
                    "start_entity": match[0],
                    "end_entity": match[1],
                    "relationship_type": rel_type,
                    "confidence": 0.7
                })
        
        return relationships
    
    def process_message(self, message: str) -> ChatResponse:
        """Process a chat message and update knowledge graph"""
        timestamp = datetime.now()
        
        # Extract entities and relationships
        entities = self.extract_entities(message)
        relationships = self.extract_relationships(message, entities)
        
        # Create entities in knowledge graph
        entities_created = []
        for entity in entities:
            entity_id = kg_service.create_entity(
                name=entity["text"],
                entity_type=entity["label"],
                properties={
                    "confidence": entity["confidence"],
                    "source": "chat",
                    "extracted_at": timestamp.isoformat()
                }
            )
            entities_created.append({
                "id": entity_id,
                "name": entity["text"],
                "type": entity["label"]
            })
        
        # Create relationships in knowledge graph
        relationships_created = []
        for rel in relationships:
            # Find matching entities
            start_entity_id = None
            end_entity_id = None
            
            for entity in entities_created:
                if entity["name"].lower() == rel["start_entity"].lower():
                    start_entity_id = entity["id"]
                if entity["name"].lower() == rel["end_entity"].lower():
                    end_entity_id = entity["id"]
            
            if start_entity_id and end_entity_id:
                success = kg_service.create_relationship(
                    start_entity_id,
                    end_entity_id,
                    rel["relationship_type"],
                    {
                        "confidence": rel["confidence"],
                        "source": "chat",
                        "extracted_at": timestamp.isoformat()
                    }
                )
                if success:
                    relationships_created.append({
                        "start_entity": start_entity_id,
                        "end_entity": end_entity_id,
                        "type": rel["relationship_type"]
                    })
        
        # Generate response
        response = self.generate_response(message, entities_created, relationships_created)
        
        # Store conversation history
        self.conversation_history.append({
            "message": message,
            "response": response,
            "entities": entities_created,
            "relationships": relationships_created,
            "timestamp": timestamp
        })
        
        return ChatResponse(
            response=response,
            entities_extracted=entities_created,
            relationships_created=relationships_created,
            timestamp=timestamp
        )
    
    def generate_response(self, message: str, entities: List[Dict[str, Any]], 
                         relationships: List[Dict[str, Any]]) -> str:
        """Generate a response based on the processed message"""
        if not entities and not relationships:
            return f"I've noted your reflection: '{message}'. I didn't identify any specific entities or relationships to add to the knowledge graph, but your thought has been recorded."
        
        response_parts = []
        
        if entities:
            entity_names = [e["name"] for e in entities]
            response_parts.append(f"I've identified and added these entities to your knowledge graph: {', '.join(entity_names)}")
        
        if relationships:
            rel_descriptions = [f"{r['start_entity']} -> {r['type']} -> {r['end_entity']}" for r in relationships]
            response_parts.append(f"I've also created these relationships: {', '.join(rel_descriptions)}")
        
        response_parts.append("Your knowledge graph has been updated with this information. Would you like to explore any connections or add more details?")
        
        return " ".join(response_parts)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history"""
        return self.conversation_history

# Global agent instance
chat_agent = ChatAgent()