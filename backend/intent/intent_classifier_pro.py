"""
Professional Intent Classifier using Semantic Embeddings
Recognizes all 7 business types with high accuracy
"""
import sys
import os

from sentence_transformers import SentenceTransformer
import numpy as np


class ProfessionalIntentClassifier:
    """
    Uses semantic embeddings to classify user intent into business types
    Based on cosine similarity scoring
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Comprehensive intent patterns for each business type
        self.intents = {
            "Bakery": [
                "start a bakery",
                "open a cake shop",
                "start a baking business",
                "open a pastry shop",
                "bread manufacturing",
                "artisan bakery",
                "bakery business",
            ],
            "Restaurant": [
                "open a restaurant",
                "start a food business",
                "start a cafe restaurant",
                "open a dining establishment",
                "restaurant business",
                "food service business",
                "casual dining",
                "fine dining restaurant",
            ],
            "Salon": [
                "open a salon",
                "beauty salon business",
                "hair salon",
                "start a beauty business",
                "hairdressing salon",
                "beauty parlor",
                "salon business",
                "hair cutting salon",
            ],
            "Fitness_Gym": [
                "open a gym",
                "fitness center",
                "gym business",
                "start a fitness studio",
                "bodybuilding gym",
                "workout center",
                "health club",
                "fitness business",
            ],
            "IT_Startup": [
                "start an IT company",
                "software development startup",
                "IT services business",
                "tech startup",
                "software startup",
                "IT consulting",
                "SaaS startup",
                "web development company",
                "app development business",
            ],
            "Medical_Clinic": [
                "open a clinic",
                "medical practice",
                "start a healthcare business",
                "diagnostic center",
                "medical clinic",
                "healthcare clinic",
                "general practice clinic",
                "doctor clinic",
            ],
            "E_commerce_Store": [
                "start online store",
                "e-commerce business",
                "online retail store",
                "start an online shop",
                "e-commerce startup",
                "online marketplace",
                "digital store",
                "online sales business",
            ],
        }
        
        # Encode all intent patterns
        self.intent_embeddings = {}
        for intent, phrases in self.intents.items():
            self.intent_embeddings[intent] = self.model.encode(phrases)

    def detect_intent(self, text, threshold=0.4, return_scores=False):
        """
        Detect business intent from user query
        
        Args:
            text: User query
            threshold: Minimum similarity score to be considered a match
            return_scores: If True, return all scores
            
        Returns:
            Best matching business type or None
            If return_scores=True, returns tuple (best_intent, scores_dict)
        """
        # Encode the query
        query_embedding = self.model.encode(text)
        
        best_intent = None
        best_score = -1
        all_scores = {}
        
        # Calculate similarity for each intent
        for intent, embeddings in self.intent_embeddings.items():
            # Calculate cosine similarity
            similarities = np.dot(embeddings, query_embedding) / (
                np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-8
            )
            
            # Get max similarity for this intent
            score = max(similarities)
            all_scores[intent] = round(float(score), 3)
            
            # Update best match
            if score > best_score:
                best_score = score
                best_intent = intent
        
        # Apply threshold
        if best_score < threshold:
            best_intent = None
        
        if return_scores:
            return best_intent, all_scores
        
        return best_intent

    def detect_intent_with_confidence(self, text, top_k=3):
        """
        Return top-k matching intents with confidence scores
        Useful for ambiguous queries
        
        Args:
            text: User query
            top_k: Number of top results to return
            
        Returns:
            List of tuples (intent, score) sorted by score
        """
        intent, scores = self.detect_intent(text, return_scores=True)
        
        # Sort by score
        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_intents[:top_k]


if __name__ == "__main__":
    # Test the classifier
    print("Testing Professional Intent Classifier...\n")
    
    classifier = ProfessionalIntentClassifier()
    
    test_queries = [
        "I want to start a bakery business",
        "How do I open a restaurant?",
        "I'm thinking about starting a salon",
        "Can I open a gym?",
        "I want to build a tech startup",
        "I'm interested in opening a medical clinic",
        "How to start an e-commerce business?",
        "I want to start a business but not sure which one",
    ]
    
    print("=" * 70)
    print("INTENT DETECTION RESULTS")
    print("=" * 70)
    
    for query in test_queries:
        intent, all_scores = classifier.detect_intent(query, return_scores=True)
        top_matches = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\nQuery: {query}")
        print(f"Detected: {intent}")
        print(f"Scores:")
        for biz_type, score in top_matches[:3]:
            marker = "✓" if biz_type == intent else " "
            print(f"  {marker} {biz_type}: {score:.3f}")
