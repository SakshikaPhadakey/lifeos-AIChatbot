"""
Professional Vector Store with Persistent Qdrant + Parquet Metadata
Implements hybrid search: semantic embedding + metadata filtering
"""
import sys
import os
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import pandas as pd
import json


class ProfessionalVectorStore:
    """
    Hybrid search system combining:
    - Vector embeddings (semantic meaning)
    - Metadata filters (business type, category, cost, etc.)
    - Parquet storage (efficient columnar storage)
    """

    def __init__(self, qdrant_path="./qdrant_storage", metadata_path="./data"):
        """
        Args:
            qdrant_path: Path to persistent Qdrant storage
            metadata_path: Path to parquet metadata files
        """
        self.qdrant_path = qdrant_path
        self.metadata_path = metadata_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding_dim = 384
        self.collection_name = "lifeos_professional"
        
        # Create directories if they don't exist
        Path(self.qdrant_path).mkdir(parents=True, exist_ok=True)
        Path(self.metadata_path).mkdir(parents=True, exist_ok=True)
        
        # Initialize persistent Qdrant
        self.client = QdrantClient(path=self.qdrant_path)
        
        # Check if collection exists, if not create it
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config={"size": self.embedding_dim, "distance": "Cosine"}
            )
        
        # Load or create metadata dataframe
        self.metadata_file = os.path.join(self.metadata_path, "knowledge_metadata.parquet")
        self.load_metadata()

    def load_metadata(self):
        """Load existing metadata or create empty dataframe"""
        if os.path.exists(self.metadata_file):
            self.metadata_df = pd.read_parquet(self.metadata_file)
        else:
            self.metadata_df = pd.DataFrame(columns=[
                'id', 'text', 'business_type', 'category', 'cost_estimate',
                'timeline_days', 'difficulty_level', 'keywords', 'source'
            ])

    def save_metadata(self):
        """Persist metadata to parquet"""
        self.metadata_df.to_parquet(self.metadata_file, index=False)

    def add_knowledge(self, id, text, business_type, category, cost_estimate=0, 
                     timeline_days=0, difficulty_level="medium", keywords=None, source="system"):
        """
        Add knowledge with rich metadata
        
        Args:
            id: Unique identifier
            text: Knowledge text
            business_type: Business category (Bakery, Restaurant, etc.)
            category: Subcategory (License, Document, Regulation, etc.)
            cost_estimate: Estimated cost in INR
            timeline_days: Timeline in days
            difficulty_level: easy/medium/hard
            keywords: List of searchable keywords
            source: Source of information
        """
        # Create embedding
        vector = self.model.encode(text).tolist()
        
        # Prepare metadata payload for Qdrant
        payload = {
            "text": text,
            "business_type": business_type,
            "category": category,
            "cost_estimate": float(cost_estimate),
            "timeline_days": int(timeline_days),
            "difficulty_level": difficulty_level,
            "keywords": keywords or [],
            "source": source
        }
        
        # Add to Qdrant
        point = PointStruct(id=id, vector=vector, payload=payload)
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        
        # Add to metadata dataframe
        new_row = {
            'id': id,
            'text': text,
            'business_type': business_type,
            'category': category,
            'cost_estimate': cost_estimate,
            'timeline_days': timeline_days,
            'difficulty_level': difficulty_level,
            'keywords': str(keywords or []),
            'source': source
        }
        
        # Check if id already exists
        if id in self.metadata_df['id'].values:
            self.metadata_df = self.metadata_df[self.metadata_df['id'] != id]
        
        self.metadata_df = pd.concat([self.metadata_df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_metadata()

    def hybrid_search(self, query, business_type=None, category=None, 
                     max_results=5, min_score=0.3):
        """
        Hybrid search combining semantic similarity + metadata filtering
        
        Args:
            query: Search query
            business_type: Filter by business type (optional)
            category: Filter by category (optional)
            max_results: Number of results
            min_score: Minimum similarity score (0-1)
            
        Returns:
            List of dicts with text, metadata, and score
        """
        # Create query embedding
        query_vector = self.model.encode(query).tolist()
        
        # Build filter conditions if provided
        filters = None
        if business_type or category:
            conditions = []
            if business_type:
                conditions.append(
                    FieldCondition(
                        key="business_type",
                        match=MatchValue(value=business_type)
                    )
                )
            if category:
                conditions.append(
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category)
                    )
                )
            # Combine conditions
            from qdrant_client.models import Filter
            filters = Filter(must=conditions) if conditions else None
        
        # Search with filters
        results = self.client.search_points(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=filters,
            limit=max_results * 2,  # Get more candidates for filtering
            with_payload=True,
            with_vectors=False
        )
        
        # Filter by min_score and format results
        formatted_results = []
        for point in results.points if hasattr(results, 'points') else results:
            if point.score >= min_score:
                formatted_results.append({
                    "id": point.id,
                    "text": point.payload["text"],
                    "score": round(point.score, 3),
                    "business_type": point.payload["business_type"],
                    "category": point.payload["category"],
                    "cost_estimate": point.payload["cost_estimate"],
                    "timeline_days": point.payload["timeline_days"],
                    "difficulty_level": point.payload["difficulty_level"],
                    "keywords": point.payload["keywords"],
                    "source": point.payload["source"]
                })
        
        return formatted_results[:max_results]

    def semantic_search(self, query, max_results=5, min_score=0.3):
        """Simple semantic search without filters"""
        return self.hybrid_search(query, max_results=max_results, min_score=min_score)

    def filter_by_business_type(self, business_type):
        """Get all knowledge for a specific business type"""
        filtered = self.metadata_df[self.metadata_df['business_type'] == business_type]
        return filtered.to_dict('records')

    def get_statistics(self):
        """Get dataset statistics"""
        stats = {
            "total_documents": len(self.metadata_df),
            "business_types": self.metadata_df['business_type'].unique().tolist(),
            "categories": self.metadata_df['category'].unique().tolist(),
            "avg_cost": float(self.metadata_df['cost_estimate'].mean()),
            "avg_timeline": float(self.metadata_df['timeline_days'].mean()),
            "difficulty_distribution": self.metadata_df['difficulty_level'].value_counts().to_dict()
        }
        return stats

    def clear_all(self):
        """Clear all data (use carefully!)"""
        self.client.delete_collection(self.collection_name)
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={"size": self.embedding_dim, "distance": "Cosine"}
        )
        self.metadata_df = pd.DataFrame(columns=[
            'id', 'text', 'business_type', 'category', 'cost_estimate',
            'timeline_days', 'difficulty_level', 'keywords', 'source'
        ])
        self.save_metadata()
        print("✓ Vector store cleared")


if __name__ == "__main__":
    # Test the professional vector store
    print("Testing Professional Vector Store...")
    
    store = ProfessionalVectorStore()
    
    # Add sample data
    store.add_knowledge(
        id=1,
        text="Restaurant requires FSSAI registration for food safety compliance",
        business_type="Restaurant",
        category="License",
        cost_estimate=5000,
        timeline_days=30,
        difficulty_level="medium",
        keywords=["FSSAI", "food", "license"],
        source="government"
    )
    
    # Test search
    results = store.hybrid_search("restaurant food license", business_type="Restaurant")
    print(f"\nSearch Results: {results}")
    
    # Test statistics
    stats = store.get_statistics()
    print(f"\nStatistics: {stats}")
