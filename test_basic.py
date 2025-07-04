#!/usr/bin/env python3
"""
Basic test script for Knowledge Management Agent
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

async def test_basic_functionality():
    """Test basic functionality without database"""
    print("🧪 Testing Knowledge Management Agent...")
    print("=" * 50)
    
    # Test imports
    try:
        from app.services.chat_agent import ChatAgent
        from app.services.knowledge_graph import KnowledgeGraphService
        from app.models.schemas import ChatMessage, ChatResponse
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test chat agent initialization
    try:
        agent = ChatAgent()
        print("✅ Chat agent initialized successfully")
    except Exception as e:
        print(f"❌ Chat agent initialization failed: {e}")
        return False
    
    # Test entity extraction
    try:
        test_text = "Machine Learning is a subset of Artificial Intelligence"
        entities = agent.extract_entities(test_text)
        print(f"✅ Entity extraction working: found {len(entities)} entities")
        for entity in entities:
            print(f"   - {entity['text']} ({entity['label']})")
    except Exception as e:
        print(f"❌ Entity extraction failed: {e}")
        return False
    
    # Test relationship extraction
    try:
        relationships = agent.extract_relationships(test_text, entities)
        print(f"✅ Relationship extraction working: found {len(relationships)} relationships")
        for rel in relationships:
            print(f"   - {rel['start_entity']} -> {rel['relationship_type']} -> {rel['end_entity']}")
    except Exception as e:
        print(f"❌ Relationship extraction failed: {e}")
        return False
    
    print("\n🎉 Basic functionality tests passed!")
    print("\nNext steps:")
    print("1. Start Neo4j database")
    print("2. Run: uvicorn app.main:app --reload")
    print("3. Open: http://localhost:8000")
    
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(test_basic_functionality())
        if not result:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)