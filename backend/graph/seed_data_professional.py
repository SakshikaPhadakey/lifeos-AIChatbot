"""
Professional Seed Data - Multiple Business Types with Rich Metadata
Includes: Bakery, Restaurant, Salon, Gym, IT Startup, Medical Clinic, E-commerce Store
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.graph.connection import conn
from backend.vector.vector_store_pro import ProfessionalVectorStore


# ==================== GRAPH SCHEMA ====================
BUSINESS_NODES = {
    "Bakery": {
        "description": "Artisan bakery selling breads, pastries, and cakes",
        "startup_cost": "₹2,00,000 - ₹5,00,000",
        "licenses": ["FSSAI License", "GST Registration", "Municipal Trade License"],
        "schemes": ["Mudra Loan", "PMEGP Scheme"],
    },
    "Restaurant": {
        "description": "Full-service restaurant with dine-in and takeaway",
        "startup_cost": "₹5,00,000 - ₹15,00,000",
        "licenses": ["FSSAI License", "GST Registration", "Municipal Trade License", "Liquor License"],
        "schemes": ["Mudra Loan", "PMEGP Scheme", "CGTMSE"],
    },
    "Salon": {
        "description": "Hair and beauty salon offering cuts, coloring, and treatments",
        "startup_cost": "₹1,50,000 - ₹3,00,000",
        "licenses": ["GST Registration", "Municipal Trade License", "Health Certificate"],
        "schemes": ["Mudra Loan", "PMEGP Scheme"],
    },
    "Fitness_Gym": {
        "description": "Gym facility with equipment, classes, and personal training",
        "startup_cost": "₹3,00,000 - ₹8,00,000",
        "licenses": ["GST Registration", "Municipal Trade License", "Health Certificate"],
        "schemes": ["Mudra Loan"],
    },
    "IT_Startup": {
        "description": "Software development and IT services company",
        "startup_cost": "₹2,00,000 - ₹10,00,000",
        "licenses": ["GST Registration", "PAN Registration", "IT/ITeS Promotion Scheme"],
        "schemes": ["Startup India", "Mudra Loan", "NASSCOM Incubation Program"],
    },
    "Medical_Clinic": {
        "description": "General medical clinic with outpatient services",
        "startup_cost": "₹5,00,000 - ₹20,00,000",
        "licenses": ["Medical Registration", "GST Registration", "Health Department Approval", "Environmental Clearance"],
        "schemes": ["Ayushman Bharat", "Health Insurance"],
    },
    "E_commerce_Store": {
        "description": "Online retail store selling products",
        "startup_cost": "₹1,00,000 - ₹5,00,000",
        "licenses": ["GST Registration", "PAN Registration", "Goods License"],
        "schemes": ["Mudra Loan", "Startup India"],
    },
}


def seed_graph_database():
    """Populate Neo4j with business, licenses, schemes, and relationships"""
    print("\n📊 Seeding Neo4j Graph Database...")
    
    # Clear existing data (optional - comment out if you want to preserve)
    # conn.run_query("MATCH (n) DETACH DELETE n")
    # print("✓ Cleared existing data")
    
    queries = []
    
    # ==================== BUSINESS NODES ====================
    for business_name in BUSINESS_NODES.keys():
        queries.append(f"MERGE (:Business {{name:'{business_name}'}})") 
    
    # ==================== LICENSE NODES ====================
    unique_licenses = set()
    for business in BUSINESS_NODES.values():
        unique_licenses.update(business["licenses"])
    
    for license_name in unique_licenses:
        queries.append(f"MERGE (:License {{name:'{license_name}'}})") 
    
    # ==================== SCHEME NODES ====================
    unique_schemes = set()
    for business in BUSINESS_NODES.values():
        unique_schemes.update(business["schemes"])
    
    for scheme_name in unique_schemes:
        queries.append(f"MERGE (:Scheme {{name:'{scheme_name}'}})") 
    
    # ==================== RELATIONSHIPS ====================
    for business_name, details in BUSINESS_NODES.items():
        # License relationships
        for license_name in details["licenses"]:
            queries.append(f"""
            MATCH (b:Business {{name:'{business_name}'}}), (l:License {{name:'{license_name}'}})
            MERGE (b)-[:REQUIRES]->(l)
            """)
        
        # Scheme relationships
        for scheme_name in details["schemes"]:
            queries.append(f"""
            MATCH (b:Business {{name:'{business_name}'}}), (s:Scheme {{name:'{scheme_name}'}})
            MERGE (b)-[:ELIGIBLE_FOR]->(s)
            """)
    
    # Execute all queries
    for query in queries:
        try:
            conn.run_query(query)
        except Exception as e:
            print(f"⚠️  Error in query: {e}")
    
    print("✓ Graph database seeded successfully")


def seed_vector_database():
    """Populate professional vector store with rich knowledge"""
    print("\n🔍 Seeding Professional Vector Store...")
    
    vector_store = ProfessionalVectorStore()
    
    # Clear previous data
    vector_store.clear_all()
    
    # ==================== BAKERY KNOWLEDGE ====================
    bakery_knowledge = [
        {
            "id": 1,
            "text": "FSSAI License is mandatory for bakeries to ensure food safety standards. Application process takes 15-30 days.",
            "business_type": "Bakery",
            "category": "License",
            "cost": 2000,
            "timeline": 30,
            "difficulty": "medium",
            "keywords": ["FSSAI", "food", "safety"],
            "source": "FSSAI Official"
        },
        {
            "id": 2,
            "text": "GST Registration is required for bakeries with annual turnover > ₹40,00,000. Registration is free and online.",
            "business_type": "Bakery",
            "category": "License",
            "cost": 0,
            "timeline": 3,
            "difficulty": "easy",
            "keywords": ["GST", "tax", "registration"],
            "source": "GST India"
        },
        {
            "id": 3,
            "text": "Mudra Loan provides up to ₹10 lakhs for bakery businesses with minimal documentation. Interest rate is ~8-10%.",
            "business_type": "Bakery",
            "category": "Finance",
            "cost": 0,
            "timeline": 7,
            "difficulty": "easy",
            "keywords": ["mudra", "loan", "finance", "startup"],
            "source": "Ministry of MSME"
        },
    ]
    
    # ==================== RESTAURANT KNOWLEDGE ====================
    restaurant_knowledge = [
        {
            "id": 10,
            "text": "FSSAI License for restaurants includes inspection, documentation review, and compliance verification. Timeline: 30-45 days.",
            "business_type": "Restaurant",
            "category": "License",
            "cost": 5000,
            "timeline": 45,
            "difficulty": "hard",
            "keywords": ["FSSAI", "restaurant", "food", "inspection"],
            "source": "FSSAI Official"
        },
        {
            "id": 11,
            "text": "Liquor License for restaurants requires municipal approval and police clearance. Timeline can be 60-90 days.",
            "business_type": "Restaurant",
            "category": "License",
            "cost": 50000,
            "timeline": 90,
            "difficulty": "hard",
            "keywords": ["liquor", "license", "alcohol", "permit"],
            "source": "Excise Department"
        },
        {
            "id": 12,
            "text": "GST and NEFT registration is mandatory for restaurants with annual turnover > ₹40,00,000.",
            "business_type": "Restaurant",
            "category": "License",
            "cost": 0,
            "timeline": 3,
            "difficulty": "easy",
            "keywords": ["GST", "NEFT", "taxation"],
            "source": "GST India"
        },
        {
            "id": 13,
            "text": "PMEGP Scheme offers subsidy of 25-35% for restaurant startups with loan assistance up to ₹25 lakhs.",
            "business_type": "Restaurant",
            "category": "Finance",
            "cost": 0,
            "timeline": 14,
            "difficulty": "medium",
            "keywords": ["subsidy", "PMEGP", "finance", "government"],
            "source": "Ministry of MSME"
        },
    ]
    
    # ==================== SALON KNOWLEDGE ====================
    salon_knowledge = [
        {
            "id": 20,
            "text": "Salon requires Health & Safety Certificate from health department. Must follow hygiene standards for chemical handling.",
            "business_type": "Salon",
            "category": "License",
            "cost": 1000,
            "timeline": 15,
            "difficulty": "easy",
            "keywords": ["health", "hygiene", "safety", "certificate"],
            "source": "Health Department"
        },
        {
            "id": 21,
            "text": "GST registration required for salons with turnover > ₹40,00,000. Online registration takes 3-5 days.",
            "business_type": "Salon",
            "category": "License",
            "cost": 0,
            "timeline": 5,
            "difficulty": "easy",
            "keywords": ["GST", "registration", "tax"],
            "source": "GST India"
        },
        {
            "id": 22,
            "text": "Mudra Shishu Scheme provides up to ₹50,000 for salon businesses without collateral requirement.",
            "business_type": "Salon",
            "category": "Finance",
            "cost": 0,
            "timeline": 5,
            "difficulty": "easy",
            "keywords": ["mudra", "shishu", "loan", "startup"],
            "source": "Ministry of MSME"
        },
    ]
    
    # ==================== GYM KNOWLEDGE ====================
    gym_knowledge = [
        {
            "id": 30,
            "text": "Gyms require Health & Safety Certification from municipal authority. Equipment must meet safety standards.",
            "business_type": "Fitness_Gym",
            "category": "License",
            "cost": 2000,
            "timeline": 20,
            "difficulty": "medium",
            "keywords": ["health", "safety", "equipment", "certification"],
            "source": "Municipal Corporation"
        },
        {
            "id": 31,
            "text": "GST registration required for gyms with annual membership revenue > ₹40,00,000.",
            "business_type": "Fitness_Gym",
            "category": "License",
            "cost": 0,
            "timeline": 3,
            "difficulty": "easy",
            "keywords": ["GST", "membership", "registration"],
            "source": "GST India"
        },
        {
            "id": 32,
            "text": "Mudra Loan provides flexible repayment for gym startups. Average interest rate is 8.5-10.5% per annum.",
            "business_type": "Fitness_Gym",
            "category": "Finance",
            "cost": 0,
            "timeline": 7,
            "difficulty": "easy",
            "keywords": ["mudra", "loan", "finance"],
            "source": "Ministry of MSME"
        },
    ]
    
    # ==================== IT STARTUP KNOWLEDGE ====================
    it_startup_knowledge = [
        {
            "id": 40,
            "text": "Startup India Registration provides tax holiday for 3 years, 80IAC deduction, and exemption from angel tax.",
            "business_type": "IT_Startup",
            "category": "License",
            "cost": 0,
            "timeline": 14,
            "difficulty": "medium",
            "keywords": ["startup", "india", "tax", "registration"],
            "source": "Startup India Department"
        },
        {
            "id": 41,
            "text": "PAN and TAN registration is mandatory for IT startups. Can be completed online in 24-48 hours.",
            "business_type": "IT_Startup",
            "category": "License",
            "cost": 0,
            "timeline": 2,
            "difficulty": "easy",
            "keywords": ["PAN", "TAN", "registration"],
            "source": "Income Tax Department"
        },
        {
            "id": 42,
            "text": "NASSCOM Incubation provides mentorship, funding, and network for IT startups. Selection process is competitive.",
            "business_type": "IT_Startup",
            "category": "Incubation",
            "cost": 0,
            "timeline": 30,
            "difficulty": "hard",
            "keywords": ["NASSCOM", "incubation", "mentorship", "network"],
            "source": "NASSCOM"
        },
        {
            "id": 43,
            "text": "IT/ITeS Promotion Scheme provides infrastructure and tax benefits. Applicable in designated zones.",
            "business_type": "IT_Startup",
            "category": "Finance",
            "cost": 0,
            "timeline": 21,
            "difficulty": "medium",
            "keywords": ["ITeS", "promotion", "infrastructure", "tax"],
            "source": "Department of IT"
        },
    ]
    
    # ==================== MEDICAL CLINIC KNOWLEDGE ====================
    medical_knowledge = [
        {
            "id": 50,
            "text": "Medical Practice requires registration with state Medical Council. Doctor must be registered and in good standing.",
            "business_type": "Medical_Clinic",
            "category": "License",
            "cost": 10000,
            "timeline": 45,
            "difficulty": "hard",
            "keywords": ["medical", "council", "registration", "doctor"],
            "source": "State Medical Council"
        },
        {
            "id": 51,
            "text": "Environmental Clearance required for clinics managing biomedical waste. Incinerator approval needed.",
            "business_type": "Medical_Clinic",
            "category": "License",
            "cost": 5000,
            "timeline": 30,
            "difficulty": "hard",
            "keywords": ["environmental", "clearance", "waste", "biomedical"],
            "source": "Environmental Department"
        },
        {
            "id": 52,
            "text": "Ayushman Bharat registration provides access to government health insurance schemes and subsidies.",
            "business_type": "Medical_Clinic",
            "category": "Finance",
            "cost": 0,
            "timeline": 14,
            "difficulty": "medium",
            "keywords": ["Ayushman", "Bharat", "insurance", "healthcare"],
            "source": "Ministry of Health"
        },
    ]
    
    # ==================== E-COMMERCE KNOWLEDGE ====================
    ecommerce_knowledge = [
        {
            "id": 60,
            "text": "E-commerce businesses require GST registration if turnover > ₹40,00,000. Online registration process.",
            "business_type": "E_commerce_Store",
            "category": "License",
            "cost": 0,
            "timeline": 5,
            "difficulty": "easy",
            "keywords": ["GST", "ecommerce", "registration"],
            "source": "GST India"
        },
        {
            "id": 61,
            "text": "Digital Privacy and Consumer Protection Act compliance mandatory. Maintain proper terms & conditions.",
            "business_type": "E_commerce_Store",
            "category": "Compliance",
            "cost": 5000,
            "timeline": 10,
            "difficulty": "medium",
            "keywords": ["privacy", "consumer", "protection", "compliance"],
            "source": "Ministry of Consumer Affairs"
        },
        {
            "id": 62,
            "text": "Startup India provides ₹10 lakhs CGTMSE credit guarantee for e-commerce startups.",
            "business_type": "E_commerce_Store",
            "category": "Finance",
            "cost": 0,
            "timeline": 7,
            "difficulty": "easy",
            "keywords": ["startup", "credit", "guarantee", "CGTMSE"],
            "source": "Ministry of MSME"
        },
    ]
    
    # Combine all knowledge
    all_knowledge = (bakery_knowledge + restaurant_knowledge + salon_knowledge + 
                    gym_knowledge + it_startup_knowledge + medical_knowledge + ecommerce_knowledge)
    
    # Add to vector store
    for item in all_knowledge:
        vector_store.add_knowledge(
            id=item["id"],
            text=item["text"],
            business_type=item["business_type"],
            category=item["category"],
            cost_estimate=item["cost"],
            timeline_days=item["timeline"],
            difficulty_level=item["difficulty"],
            keywords=item["keywords"],
            source=item["source"]
        )
    
    print(f"✓ Vector store seeded with {len(all_knowledge)} knowledge documents")
    
    # Print statistics
    stats = vector_store.get_statistics()
    print(f"\n📈 Vector Store Statistics:")
    print(f"   Total Documents: {stats['total_documents']}")
    print(f"   Business Types: {len(stats['business_types'])}")
    print(f"   Categories: {len(stats['categories'])}")
    print(f"   Avg Timeline: {stats['avg_timeline']:.1f} days")
    print(f"   Avg Cost: ₹{stats['avg_cost']:.0f}")


def verify_seeding():
    """Verify that seeding was successful"""
    print("\n✅ Verification:")
    
    # Check graph
    from backend.graph.business_service import BusinessService
    service = BusinessService()
    
    for business_name in BUSINESS_NODES.keys():
        data = service.get_business_info(business_name)
        if data:
            print(f"   {business_name}: {len(data.get('licenses', []))} licenses, {len(data.get('schemes', []))} schemes")
        else:
            print(f"   {business_name}: ❌ Not found")


if __name__ == "__main__":
    print("=" * 60)
    print("🌱 LIFEOS PROFESSIONAL SEEDING PIPELINE")
    print("=" * 60)
    
    seed_graph_database()
    seed_vector_database()
    verify_seeding()
    
    print("\n" + "=" * 60)
    print("✨ Seeding complete! Ready for testing.")
    print("=" * 60)
