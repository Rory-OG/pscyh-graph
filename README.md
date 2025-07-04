# Knowledge Management Agent

An interactive knowledge management system that combines conversational AI with Neo4j graph database to help you build and explore your personal knowledge graph. Share your thoughts, reflections, and notes with an intelligent agent that automatically extracts entities and relationships to create a visual knowledge graph.

## Features

🧠 **Conversational Interface**: Chat with an intelligent agent to share your thoughts and ideas
📊 **Automatic Entity Extraction**: Uses NLP to identify entities and relationships from your messages
🔗 **Knowledge Graph Visualization**: Interactive D3.js visualization of your knowledge graph
🎯 **Real-time Updates**: See your knowledge graph grow as you add new information
🔍 **Search & Discovery**: Find entities and explore connections in your knowledge base
📈 **Analytics**: Track statistics about your knowledge graph growth
🎨 **Modern UI**: Beautiful, responsive interface with real-time updates

## Architecture

- **Backend**: FastAPI with Python
- **Database**: Neo4j graph database
- **NLP**: spaCy for entity extraction and relationship identification
- **Frontend**: React with D3.js for graph visualization
- **Real-time**: WebSocket support for live updates

## Quick Start

### Option 1: Using Docker (Recommended)

1. Clone the repository and navigate to the project directory
2. Start the services:
   ```bash
   docker-compose up -d
   ```
3. Open your browser and go to `http://localhost:8000`

### Option 2: Manual Installation

1. **Prerequisites**:
   - Python 3.8+
   - Neo4j database (local or remote)
   - Node.js (for development)

2. **Setup**:
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd knowledge-management-agent
   
   # Run the setup script
   python setup.py
   
   # Or manually:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Configure Neo4j**:
   - Copy `.env.example` to `.env`
   - Update the Neo4j connection details:
     ```
     NEO4J_URI=bolt://localhost:7687
     NEO4J_USERNAME=neo4j
     NEO4J_PASSWORD=your_password
     ```

4. **Start the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Open your browser**: Go to `http://localhost:8000`

## Usage

### Chat with the Agent

1. **Start a Conversation**: Type your thoughts, reflections, or notes in the chat interface
2. **Entity Recognition**: The agent will automatically identify entities (people, concepts, dates, etc.)
3. **Relationship Extraction**: It will also detect relationships between entities
4. **Knowledge Graph Updates**: Your graph will be updated in real-time

### Example Conversations

```
User: "I've been thinking about Machine Learning and how it relates to Artificial Intelligence. 
       Neural Networks are a key component of deep learning systems."

Agent: "I've identified and added these entities to your knowledge graph: 
        Machine Learning (CONCEPT), Artificial Intelligence (CONCEPT), Neural Networks (CONCEPT), 
        deep learning (CONCEPT). I've also created these relationships: 
        Machine Learning -> RELATES_TO -> Artificial Intelligence, 
        Neural Networks -> IS_A -> deep learning. 
        Your knowledge graph has been updated with this information."
```

### Knowledge Graph Features

- **Interactive Visualization**: Drag nodes, zoom, and pan
- **Entity Types**: Different colors for different entity types
- **Search**: Find specific entities quickly
- **Statistics**: View counts of entities and relationships
- **Real-time Updates**: Graph updates as you chat

## API Endpoints

### Chat API
- `POST /api/chat/message` - Send a message to the agent
- `GET /api/chat/history` - Get conversation history
- `DELETE /api/chat/history` - Clear conversation history

### Knowledge Graph API
- `GET /api/kg/` - Get the current knowledge graph
- `POST /api/kg/search` - Search for entities
- `GET /api/kg/entity/{id}` - Get entity details and connections
- `POST /api/kg/entity` - Create an entity manually
- `POST /api/kg/relationship` - Create a relationship manually
- `GET /api/kg/stats` - Get graph statistics

## Configuration

### Environment Variables

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# OpenAI Configuration (optional, for enhanced NLP)
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
DEBUG=True
```

### Customization

- **Entity Types**: Modify `app/services/chat_agent.py` to customize entity recognition
- **Relationships**: Add new relationship patterns in the same file
- **UI**: Customize the frontend by editing `static/index.html`
- **Colors**: Change entity colors in the D3.js visualization

## Development

### Project Structure

```
knowledge-management-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   │   ├── api/
│   │   │   ├── chat.py            # Chat API endpoints
│   │   │   └── knowledge_graph.py # Knowledge graph API
│   │   ├── core/
│   │   │   ├── config.py          # Configuration settings
│   │   │   └── database.py        # Neo4j connection
│   │   ├── models/
│   │   │   └── schemas.py         # Pydantic models
│   │   └── services/
│   │       ├── chat_agent.py      # Chat agent logic
│   │       └── knowledge_graph.py # Graph operations
│   ├── static/
│   │   └── index.html             # Frontend application
│   ├── requirements.txt           # Python dependencies
│   ├── docker-compose.yml         # Docker setup
│   ├── Dockerfile                 # Container definition
│   └── README.md                  # This file
```

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **Neo4j Connection Error**:
   - Check that Neo4j is running
   - Verify connection details in `.env`
   - Ensure Neo4j is accessible on the specified port

2. **SpaCy Model Not Found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Port Already in Use**:
   - Change the port in `docker-compose.yml` or when running uvicorn
   - Kill existing processes using the port

4. **Graph Not Displaying**:
   - Check browser console for JavaScript errors
   - Ensure the API is returning data
   - Verify D3.js is loaded correctly

### Performance Tips

- **Large Graphs**: Limit the number of nodes returned with the `limit` parameter
- **Memory Usage**: Restart the application periodically for large datasets
- **Neo4j Tuning**: Configure Neo4j memory settings for better performance

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with FastAPI, Neo4j, React, and D3.js
- Uses spaCy for natural language processing
- Inspired by knowledge management and personal knowledge graphs

---

## Next Steps

- Add support for file uploads (PDFs, documents)
- Implement user authentication and multi-user support
- Add export functionality (JSON, CSV, GraphML)
- Integrate with external APIs (Wikipedia, Google Knowledge Graph)
- Add more sophisticated NLP models
- Implement graph analysis algorithms
- Add mobile app support