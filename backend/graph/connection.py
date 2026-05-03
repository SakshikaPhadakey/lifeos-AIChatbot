from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Specify the path to the .env file
load_dotenv(dotenv_path="config/.env")


class Neo4jConnection:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", os.getenv("NEO4J_PASSWORD"))
        )

    def run_query(self, query, params=None):
        with self.driver.session(database="lifeos-db") as session:
            result = session.run(query, params)
            return [record.data() for record in result]


conn = Neo4jConnection()