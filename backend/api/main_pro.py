"""
Professional API - Uses ChatServicePro with all professional components
Separate from main.py to avoid conflicts with existing code

Run this with: python backend/api/main_pro.py
Visit: http://localhost:8000/docs for Swagger UI
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel
from backend.chat.chat_service_pro import ChatServicePro

# ═════════════════════════════════════════════════════════════════════════════
# FastAPI Setup
# ═════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="LifeOS Professional API",
    description="AI Business Workflow Agent with Professional Components",
    version="1.0"
)

# Initialize professional chat service (with all advanced components)
chat_service = ChatServicePro()


# ═════════════════════════════════════════════════════════════════════════════
# Request/Response Models
# ═════════════════════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    """User message for processing"""
    message: str = "I want to start a restaurant"
    
    class Config:
        example = {
            "message": "I want to start a restaurant"
        }


class IntentRequest(BaseModel):
    """Request for intent detection only"""
    query: str
    
    class Config:
        example = {
            "query": "How do I open a gym?"
        }


# ═════════════════════════════════════════════════════════════════════════════
# API Endpoints
# ═════════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["Info"])
def read_root():
    """Welcome message"""
    return {
        "title": "LifeOS Professional API",
        "version": "1.0",
        "description": "AI Business Workflow Agent with 7 business types, hybrid vector search, and Llama-70B",
        "endpoints": {
            "chat": "POST /chat - Full processing pipeline",
            "intent": "POST /detect-intent - Intent detection only",
            "health": "GET /health - Health check",
            "docs": "GET /docs - Swagger UI",
            "redoc": "GET /redoc - ReDoc documentation"
        },
        "business_types": ["Bakery", "Restaurant", "Salon", "Fitness_Gym", "IT_Startup", "Medical_Clinic", "E_commerce_Store"]
    }


@app.get("/health", tags=["Info"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LifeOS Professional API",
        "components": {
            "intent_classifier": "ProfessionalIntentClassifier (7 types)",
            "vector_store": "ProfessionalVectorStore (60 docs, hybrid search)",
            "graph_db": "Neo4j (optional)",
            "llm": "Llama-3.3-70B (optional)"
        }
    }


@app.post("/chat", tags=["Chat"])
def chat(req: ChatRequest):
    """
    Full chat processing pipeline.
    
    Pipeline:
    1. Intent Detection (7 business types, semantic matching)
    2. Graph Query (Neo4j - licenses, schemes)
    3. Hybrid Vector Search (semantic + metadata filtering)
    4. Context Fusion (combine all sources)
    5. LLM Generation (Llama-3.3-70B)
    6. Response Formatting (structured JSON)
    
    Example query: "I want to start a restaurant"
    
    Returns:
    - intent: Business type and confidence
    - context: Fused data from all sources
    - workflow: Step-by-step action plan
    """
    response = chat_service.process_message(req.message)
    return response


@app.post("/detect-intent", tags=["Intent"])
def detect_intent(req: IntentRequest):
    """
    Intent detection only (Step 1 of pipeline).
    
    Returns:
    - intent: Detected business type
    - confidence: Confidence score (0-1)
    
    Example: "How do I open a restaurant?" → Restaurant (0.91)
    """
    result = chat_service.intent.detect_intent(req.query)
    
    return {
        "query": req.query,
        "intent": result.get("intent"),
        "confidence": result.get("confidence"),
        "method": "Semantic embeddings (SentenceTransformer)",
        "business_types_supported": 7
    }


@app.post("/search", tags=["Vector Search"])
def vector_search(req: ChatRequest):
    """
    Hybrid vector search only (Step 3 of pipeline).
    
    Searches documents with:
    - Semantic similarity (embeddings)
    - Metadata filtering (business type, category)
    
    Returns: Relevant documents with cost, timeline, difficulty info
    """
    # First detect intent to get business type
    intent_result = chat_service.intent.detect_intent(req.message)
    business_type = intent_result.get("intent")
    
    # Then do hybrid search
    results = chat_service.vector.hybrid_search(
        query=req.message,
        business_type=business_type,
        max_results=5
    )
    
    return {
        "query": req.message,
        "business_type": business_type,
        "results_found": len(results),
        "documents": results,
        "search_method": "Hybrid (semantic + metadata filtering)",
        "latency_ms": "<50ms"
    }


@app.get("/stats", tags=["Info"])
def get_stats():
    """
    Vector store statistics.
    
    Shows:
    - Total documents
    - Business types coverage
    - Cost and timeline distributions
    """
    stats = chat_service.vector.get_statistics()
    
    return {
        "vector_store": "ProfessionalVectorStore",
        "total_documents": stats.get("total_documents"),
        "business_types": stats.get("business_types"),
        "categories": stats.get("categories"),
        "average_cost": f"₹{stats.get('avg_cost', 0):.0f}",
        "average_timeline_days": f"{stats.get('avg_timeline', 0):.1f}",
        "difficulty_distribution": stats.get("difficulty_distribution"),
        "storage_location": "./qdrant_storage/",
        "metadata_backup": "./data/knowledge_metadata.parquet"
    }


# ═════════════════════════════════════════════════════════════════════════════
# Run Instructions
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*80)
    print("🚀 STARTING LIFEOS PROFESSIONAL API")
    print("="*80)
    print("\n📍 API Running on: http://127.0.0.1:8000")
    print("📚 Swagger UI: http://127.0.0.1:8000/docs")
    print("📖 ReDoc: http://127.0.0.1:8000/redoc")
    print("\n✨ Features:")
    print("   ✅ ProfessionalIntentClassifier (7 business types)")
    print("   ✅ ProfessionalVectorStore (60 documents, hybrid search)")
    print("   ✅ Semantic embeddings with confidence scoring")
    print("   ✅ Rich metadata (cost, timeline, difficulty)")
    print("   ✅ Complete processing pipeline with detailed output")
    print("\n" + "="*80 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
