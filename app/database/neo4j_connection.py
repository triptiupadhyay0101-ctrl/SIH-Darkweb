import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv(
    "NEO4J_DATABASE",
    "sih-darkweb"
)


if not NEO4J_URI or not NEO4J_USER or not NEO4J_PASSWORD:
    raise ValueError(
        "Neo4j configuration is missing from .env"
    )


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def test_neo4j():

    with driver.session(
        database=NEO4J_DATABASE
    ) as session:

        result = session.run(
            'RETURN "FastAPI connected to Neo4j" AS message'
        )

        return result.single()["message"]