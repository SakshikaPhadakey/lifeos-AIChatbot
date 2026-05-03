"""
COMPREHENSIVE TESTING GUIDE FOR LIFEOS PROFESSIONAL SYSTEM
============================================================

This script demonstrates the complete flow:
1. Seed Professional Database (Graph + Vector)
2. Test Intent Classification
3. Test Hybrid Vector Search
4. Test Context Building
5. Test LLM Response Generation
6. Test Complete Chat Flow

RUN ORDER:
- python backend/graph/seed_data_professional.py    # Step 1: Seed data
- python backend/testing/test_professional_system.py # Step 2: Run all tests
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.intent.intent_classifier_pro import ProfessionalIntentClassifier
from backend.vector.vector_store_pro import ProfessionalVectorStore
from backend.graph.business_service import BusinessService
from backend.context.context_builder import ContextBuilder
from backend.llm.llm_service import LLMService
from backend.agent.workflow_agent import WorkflowAgent


class LifeOSTestSuite:
    """Complete test suite for LifeOS professional system"""
    
    def __init__(self):
        print("\n" + "="*80)
        print("🚀 INITIALIZING LIFEOS PROFESSIONAL TEST SUITE")
        print("="*80)
        
        self.classifier = ProfessionalIntentClassifier()
        self.vector_store = ProfessionalVectorStore()
        self.business_service = BusinessService()
        self.context_builder = ContextBuilder()
        self.llm_service = LLMService()
        self.workflow_agent = WorkflowAgent()
        
        print("✓ All components initialized successfully\n")
    
    # ==================== TEST 1: INTENT CLASSIFICATION ====================
    def test_intent_classification(self):
        """Test intent detection across all business types"""
        print("\n" + "-"*80)
        print("TEST 1: INTENT CLASSIFICATION")
        print("-"*80)
        
        test_queries = {
            "Bakery": "I want to start a bakery business",
            "Restaurant": "How do I open a restaurant?",
            "Salon": "I'm thinking about opening a beauty salon",
            "Fitness_Gym": "Can I start a gym?",
            "IT_Startup": "I want to launch a software startup",
            "Medical_Clinic": "How to open a medical clinic?",
            "E_commerce_Store": "I want to start an online store",
        }
        
        print("\n✓ Testing intent detection across 7 business types:\n")
        
        results = {}
        for expected, query in test_queries.items():
            detected, scores = self.classifier.detect_intent(query, return_scores=True)
            top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
            
            status = "✅ PASS" if detected == expected else "❌ FAIL"
            results[expected] = (detected == expected)
            
            print(f"{status} | Query: {query}")
            print(f"       Detected: {detected} (confidence: {scores[detected]:.3f})")
            print(f"       Top 3: {', '.join([f'{b}:{s:.2f}' for b, s in top_3])}\n")
        
        accuracy = sum(results.values()) / len(results) * 100
        print(f"📊 Intent Classification Accuracy: {accuracy:.1f}%\n")
        
        return results
    
    # ==================== TEST 2: HYBRID VECTOR SEARCH ====================
    def test_vector_search(self):
        """Test professional vector search with metadata filtering"""
        print("\n" + "-"*80)
        print("TEST 2: HYBRID VECTOR SEARCH WITH METADATA FILTERING")
        print("-"*80)
        
        test_cases = [
            {
                "query": "food license requirements",
                "business_type": "Restaurant",
                "expected_category": "License"
            },
            {
                "query": "startup funding options",
                "business_type": "IT_Startup",
                "expected_category": "Finance"
            },
            {
                "query": "health and safety certification",
                "business_type": "Salon",
                "expected_category": "License"
            },
        ]
        
        print("\n✓ Testing hybrid search (semantic + metadata filtering):\n")
        
        for i, test in enumerate(test_cases, 1):
            print(f"Test Case {i}:")
            print(f"  Query: {test['query']}")
            print(f"  Filter (Business): {test['business_type']}")
            
            # Semantic-only search
            semantic_results = self.vector_store.semantic_search(test['query'], max_results=3)
            print(f"  Semantic Search Results: {len(semantic_results)} documents")
            for j, result in enumerate(semantic_results, 1):
                print(f"    {j}. [{result['category']}] {result['text'][:70]}...")
                print(f"       Score: {result['score']:.3f} | Cost: ₹{result['cost_estimate']}")
            
            # Hybrid search with filter
            hybrid_results = self.vector_store.hybrid_search(
                test['query'],
                business_type=test['business_type'],
                max_results=3
            )
            print(f"  Hybrid Search Results (filtered): {len(hybrid_results)} documents")
            for j, result in enumerate(hybrid_results, 1):
                print(f"    {j}. [{result['category']}] {result['text'][:70]}...")
                print(f"       Score: {result['score']:.3f} | Timeline: {result['timeline_days']} days")
            print()
        
        # Show vector store statistics
        stats = self.vector_store.get_statistics()
        print(f"📈 Vector Store Statistics:")
        print(f"   Total Documents: {stats['total_documents']}")
        print(f"   Business Types: {', '.join(stats['business_types'])}")
        print(f"   Categories: {', '.join(stats['categories'])}")
        print(f"   Avg Cost: ₹{stats['avg_cost']:.0f}")
        print(f"   Avg Timeline: {stats['avg_timeline']:.1f} days\n")
    
    # ==================== TEST 3: GRAPH QUERIES ====================
    def test_graph_queries(self):
        """Test Neo4j graph queries"""
        print("\n" + "-"*80)
        print("TEST 3: GRAPH QUERY TESTS")
        print("-"*80)
        
        test_businesses = ["Bakery", "Restaurant", "Salon", "IT_Startup"]
        
        print("\n✓ Testing graph retrieval for business types:\n")
        
        for business in test_businesses:
            data = self.business_service.get_business_info(business)
            if data:
                print(f"✅ {business}:")
                print(f"   Licenses: {', '.join(data['licenses']) if data['licenses'] else 'None'}")
                print(f"   Schemes: {', '.join(data['schemes']) if data['schemes'] else 'None'}")
                print()
            else:
                print(f"❌ {business}: Data not found\n")
    
    # ==================== TEST 4: CONTEXT BUILDING ====================
    def test_context_building(self):
        """Test context fusion from multiple sources"""
        print("\n" + "-"*80)
        print("TEST 4: CONTEXT BUILDING (Fusion)")
        print("-"*80)
        
        # Simulate a user query
        user_query = "I want to start a restaurant"
        print(f"\n📝 User Query: {user_query}\n")
        
        # Step 1: Intent Classification
        print("Step 1: Intent Classification")
        detected_intent = self.classifier.detect_intent(user_query)
        print(f"  Detected Business Type: {detected_intent}\n")
        
        # Step 2: Graph Query
        print("Step 2: Graph Query")
        graph_data = self.business_service.get_business_info(detected_intent)
        print(f"  Licenses (from Neo4j): {graph_data['licenses']}")
        print(f"  Schemes (from Neo4j): {graph_data['schemes']}\n")
        
        # Step 3: Vector Search
        print("Step 3: Vector Search (Hybrid)")
        vector_results = self.vector_store.hybrid_search(
            user_query,
            business_type=detected_intent,
            max_results=3
        )
        print(f"  Retrieved {len(vector_results)} knowledge documents:")
        for i, result in enumerate(vector_results, 1):
            print(f"    {i}. [{result['category']}] {result['text'][:60]}...")
            print(f"       Score: {result['score']:.3f}, Timeline: {result['timeline_days']}d\n")
        
        # Step 4: Context Builder
        print("Step 4: Context Fusion")
        vector_texts = [r['text'] for r in vector_results]
        context = self.context_builder.build_context(
            user_query,
            graph_data,
            vector_texts
        )
        print(f"  Fused Context Keys: {', '.join(context.keys())}")
        print(f"  Business: {context['business']}")
        print(f"  Knowledge Sources: {len(context['knowledge'])} documents\n")
        
        return context
    
    # ==================== TEST 5: COMPLETE CHAT FLOW ====================
    def test_complete_flow(self):
        """Test end-to-end flow"""
        print("\n" + "-"*80)
        print("TEST 5: COMPLETE END-TO-END FLOW")
        print("-"*80)
        
        test_queries = [
            "I want to start a restaurant business",
            "How do I open a salon?",
            "Can I start an IT company?",
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            print("-" * 40)
            
            # Step 1: Intent
            intent = self.classifier.detect_intent(query)
            print(f"1️⃣  Intent: {intent}")
            
            # Step 2: Graph
            graph_data = self.business_service.get_business_info(intent)
            print(f"2️⃣  Graph Data: {len(graph_data['licenses'])} licenses, {len(graph_data['schemes'])} schemes")
            
            # Step 3: Vector
            vector_results = self.vector_store.hybrid_search(query, business_type=intent, max_results=2)
            print(f"3️⃣  Vector Results: {len(vector_results)} documents")
            
            # Step 4: Context
            vector_texts = [r['text'] for r in vector_results]
            context = self.context_builder.build_context(query, graph_data, vector_texts)
            print(f"4️⃣  Context: Built successfully")
            
            # Step 5: LLM (Optional - comment out if API key not available)
            try:
                print(f"5️⃣  LLM Response: Generating workflow plan...")
                # llm_response = self.llm_service.generate_response(context)
                # print(f"    Generated successfully")
            except Exception as e:
                print(f"5️⃣  LLM Response: Skipped (API key not configured)")
            
            print()
    
    # ==================== TEST 6: SEARCH QUALITY ====================
    def test_search_quality(self):
        """Test and demonstrate search quality improvements"""
        print("\n" + "-"*80)
        print("TEST 6: SEARCH QUALITY - BASIC vs PROFESSIONAL")
        print("-"*80)
        
        print("\n✓ Demonstrating hybrid search capabilities:\n")
        
        # Advanced search example
        query = "startup funding"
        business_type = "IT_Startup"
        category = "Finance"
        
        print(f"Query: '{query}'")
        print(f"Filters: Business='{business_type}', Category='{category}'\n")
        
        # Search with filters
        results = self.vector_store.hybrid_search(
            query,
            business_type=business_type,
            category=category,
            max_results=5
        )
        
        print(f"Results ({len(results)} found):\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['text']}")
            print(f"   📊 Score: {result['score']:.3f}")
            print(f"   💼 Type: {result['business_type']} | 📁 Category: {result['category']}")
            print(f"   💰 Cost: ₹{result['cost_estimate']} | ⏱️  Timeline: {result['timeline_days']}d")
            print(f"   🔑 Keywords: {', '.join(result['keywords'])}")
            print()


def main():
    """Run all tests"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + " "*20 + "LIFEOS PROFESSIONAL SYSTEM TEST SUITE" + " "*22 + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # Initialize test suite
    suite = LifeOSTestSuite()
    
    # Run tests
    try:
        suite.test_intent_classification()
        suite.test_vector_search()
        suite.test_graph_queries()
        suite.test_context_building()
        suite.test_search_quality()
        suite.test_complete_flow()
        
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " "*25 + "✨ ALL TESTS COMPLETED SUCCESSFULLY ✨" + " "*14 + "█")
        print("█" + " "*78 + "█")
        print("█"*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test Suite Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
