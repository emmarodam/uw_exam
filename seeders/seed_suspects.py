from faker import Faker
from pyArango.connection import Connection
import random

# Initialize Faker
faker = Faker()

# Connect to ArangoDB
conn = Connection(arangoURL='http://localhost:8529', username='root', password='root')
db = conn['crimes']

# Ensure the suspects collection exists (create if not)
if not db.hasCollection('suspects'):
    suspects_collection = db.createCollection(name='suspects')
else:
    suspects_collection = db['suspects']

# Ensure the edge collections exist (create if not)
if not db.hasCollection('suspect_friends_with_suspect'):
    friends_edge_collection = db.createCollection(name='suspect_friends_with_suspect', className='Edges')
else:
    friends_edge_collection = db['suspect_friends_with_suspect']

if not db.hasCollection('suspect_related_to_suspect'):
    related_edge_collection = db.createCollection(name='suspect_related_to_suspect', className='Edges')
else:
    related_edge_collection = db['suspect_related_to_suspect']

# Truncate collections to remove all existing documents
suspects_collection.truncate()
friends_edge_collection.truncate()
related_edge_collection.truncate()

# Function to generate a fake suspect
def generate_suspect():
    return {
        'name': faker.name(),
        'address': faker.address(),
        'date_of_birth': faker.date_of_birth().isoformat(),
        'phone_number': faker.phone_number(),
        'ssn': faker.ssn(),
        'arrest_date': faker.date_this_decade().isoformat(),
        'bail_amount': round(random.uniform(1000, 100000), 2)
    }

# Insert fake suspects into the collection
num_suspects = 25  # Number of suspects to generate
suspect_docs = []

for _ in range(num_suspects):
    suspect = generate_suspect()
    doc = suspects_collection.createDocument(suspect)
    doc.save()
    suspect_docs.append(doc)

# Function to create an edge between two suspects
def create_edge(collection, from_doc, to_doc):
    edge = collection.createDocument()
    edge['_from'] = from_doc['_id']
    edge['_to'] = to_doc['_id']
    edge.save()

# Generate and insert edges
num_edges = 25  # Number of edges to generate for each type

for _ in range(num_edges):
    from_suspect = random.choice(suspect_docs)
    to_suspect = random.choice(suspect_docs)
    if from_suspect != to_suspect:
        create_edge(friends_edge_collection, from_suspect, to_suspect)
        
    from_suspect = random.choice(suspect_docs)
    to_suspect = random.choice(suspect_docs)
    if from_suspect != to_suspect:
        create_edge(related_edge_collection, from_suspect, to_suspect)

print(f"Successfully inserted {num_suspects} suspects into the 'suspects' collection.")
print(f"Successfully created {num_edges} 'friends_with' edges and {num_edges} 'related_to' edges.")


