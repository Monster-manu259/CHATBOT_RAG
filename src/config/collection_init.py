from src.config.weaviate_db import weaviate_connection

def initialize_demo_collection():
    from weaviate.classes.config import Configure, Property, DataType
    client = weaviate_connection()
    try:
        client.collections.create(
            "DemoCollection",
            properties=[
                Property(name="chunk_text", data_type=DataType.TEXT),
                Property(name="filename", data_type=DataType.TEXT),
                Property(name="page_number", data_type=DataType.INT),
            ],
            vector_config=[
                Configure.Vectors.text2vec_weaviate(
                    name="chunk_text_vector",
                    source_properties=["chunk_text"],
                    model="Snowflake/snowflake-arctic-embed-l-v2.0",
                )
            ],
        )
        print("DemoCollection created with vectorizer.")
    except Exception as e:
        if "already exists" in str(e):
            print("DemoCollection already exists.")
        else:
            print(f"Error creating DemoCollection: {e}")
    finally:
        client.close()