from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"  # Update if Neo4j is running elsewhere
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "yourpassword"  # Replace with your actual password

try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run("RETURN 'Neo4j Connection Successful' AS message")
        for record in result:
            print(record["message"])
    driver.close()
except Exception as e:
    print(f"Neo4j Connection Failed: {e}")

