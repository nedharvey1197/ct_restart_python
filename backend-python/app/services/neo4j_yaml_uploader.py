import yaml
from neo4j import GraphDatabase
import json

# Neo4j connection configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "secretpassword"

class Neo4jYAMLUploader:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("Connected to Neo4j successfully!")
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")
            raise e
        
        self.successful_nodes = []
        self.successful_relationships = []
        self.rejected_entries = []
    
    def _preprocess_yaml(self, yaml_data):
        preprocessed = []
        for schema_name, schema_details in yaml_data.get("components", {}).get("schemas", {}).items():
            node = {
                "name": schema_name,
                "label": "Schema",
                "properties": {},
                "relationships": []
            }

            if "default" in schema_details:
                node["properties"]["defaultSchema"] = schema_details["default"]

            if "type" in schema_details:
                node["relationships"].append({"from": schema_name, "to": schema_details["type"], "type": "CAN_BE"})

            if "enum" in schema_details:
                node["relationships"].append({"from": schema_name, "to": "Enum", "type": "CAN_BE"})
                for enum_value in schema_details["enum"]:
                    node["relationships"].append({"from": "Enum", "to": enum_value, "type": "HAS_VALUE"})

            if "$ref" in schema_details:
                ref_target = schema_details["$ref"].split("/")[-1]
                node["relationships"].append({"from": schema_name, "to": ref_target, "type": "DEFINES"})
                
            if "items" in schema_details:
                item_type = schema_details["items"].get("type", None)
                if item_type:
                    node["relationships"].append({"from": schema_name, "to": item_type, "type": "CONTAINS"})

            preprocessed.append(node)
        return preprocessed
    
    def close(self):
        try:
            self.driver.close()
            print("Connection to Neo4j closed successfully.")
        except Exception as e:
            print(f"Error closing Neo4j connection: {e}")

    def upload_nodes_and_relationships(self, yaml_file):
        with open(yaml_file, 'r') as f:
            raw_data = yaml.safe_load(f)
        
        preprocessed_data = self._preprocess_yaml(raw_data)

        with self.driver.session() as session:
            for node_data in preprocessed_data:
                try:
                    self._create_node(session, node_data["name"], node_data["label"], node_data["properties"])

                    # Ensure all referenced elements exist before linking
                    for rel in node_data["relationships"]:
                        if rel["to"] in ["string", "integer", "boolean", "object", "array"]:
                            self._create_node(session, rel["to"], "DataType", {})
                        elif rel["type"] in ["HAS_VALUE", "CAN_BE", "DEFINES", "CONTAINS"]:
                            self._create_node(session, rel["to"], "SchemaElement", {})
                        self._create_relationship(session, rel["from"], rel["to"], rel["type"])
                except Exception as e:
                    print(f"Error processing node: {node_data['name']}, Error: {e}")
                    self.rejected_entries.append(node_data["name"])
        
        self._save_results()

    def _create_node(self, session, name, label, properties):
        try:
            properties_to_store = {k: v for k, v in properties.items() if k not in ["schema", "enum"]}
            print(f"Creating node: {name}, Label: {label}, Properties: {properties_to_store}")
            
            query = (
                "MERGE (n:{label} {{name: $name}}) "
                "SET n += $properties"
            ).format(label=label)
            session.run(query, name=name, properties=properties_to_store)
            self.successful_nodes.append({"name": name, "label": label})
        except Exception as e:
            print(f"Error creating node: {name}, Error: {e}")
            self.rejected_entries.append(name)
    
    def _create_relationship(self, session, from_node, to_node, relationship):
        try:
            query = (
                "MATCH (a {name: $from_node}), (b {name: $to_node}) "
                "MERGE (a)-[r:{relationship}]->(b)"
            ).format(relationship=relationship)
            session.run(query, from_node=from_node, to_node=to_node)
            self.successful_relationships.append({"from": from_node, "to": to_node, "relationship": relationship})
        except Exception as e:
            print(f"Error creating relationship: {from_node} -[{relationship}]-> {to_node}, Error: {e}")
            self.rejected_entries.append({"from": from_node, "to": to_node, "relationship": relationship})

    def _save_results(self):
        result_data = {
            "successful_nodes": self.successful_nodes,
            "successful_relationships": self.successful_relationships,
            "rejected_entries": self.rejected_entries
        }
        with open("neo4j_upload_results.json", "w") as f:
            json.dump(result_data, f, indent=4)
        print("Upload results saved to neo4j_upload_results.json")

if __name__ == "__main__":
    uploader = Neo4jYAMLUploader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        yaml_file = "ctg-oas-v2.yaml"
        print("Starting YAML upload to Neo4j...")
        uploader.upload_nodes_and_relationships(yaml_file)
        print("YAML file uploaded to Neo4j successfully!")
    except Exception as e:
        import traceback
        print("Error uploading YAML to Neo4j:")
        print(traceback.format_exc())
    finally:
        uploader.close()
