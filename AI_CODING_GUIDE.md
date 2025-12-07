# MSO Library - AI Coding Assistant Guide

This guide helps AI coding assistants understand how to use the MSO (Mongo Schema Object) library effectively.

## Quick Start Pattern

```python
from mso import connect_to_mongo, get_model

# Step 1: Connect to MongoDB
db = connect_to_mongo("mongodb://localhost:27017", "your-database-name")

# Step 2: Get a model based on collection schema
YourModel = get_model(db, "collection_name")

# Step 3: Use the model
instance = YourModel(field1="value", field2=123)
instance.save()
```

## Core Concepts

### 1. Connection Pattern
Always use `connect_to_mongo()` - never import `pymongo.MongoClient` directly.

```python
from mso import connect_to_mongo, get_model

# Basic connection
db = connect_to_mongo("mongodb://localhost:27017", "db-name")

# With custom timeout
db = connect_to_mongo("mongodb://localhost:27017", "db-name", timeout=10000)
```

### 2. Model Generation
Models are **dynamically generated** from MongoDB's `$jsonSchema` validator.

```python
# Get model - this reads the collection's schema
People = get_model(db, "people")

# Now People is a class with properties matching your schema
person = People(name="John Doe", age=30)
```

### 3. Creating Documents

```python
# Method 1: Constructor with kwargs
person = People(name="Alice", age=25, email="alice@example.com")

# Method 2: Create empty then set fields
person = People()
person.name = "Bob"
person.age = 30

# Method 3: From dictionary
person = People.from_dict({
    "name": "Charlie",
    "age": 35,
    "email": "charlie@example.com"
})
```

### 4. Nested Objects

Nested objects are accessed using dot notation:

```python
person = People()

# Access nested object - it auto-creates
person.health.primary_physician.name = "Dr. Strange"
person.health.primary_physician.contact.phone = "123-456-7890"
```

### 5. Array Fields

Arrays have special `.add()` method:

```python
# Add to array with kwargs
person.addresses.add(
    type="home",
    street="123 Elm St",
    city="NYC",
    state="NY",
    zip="10001"
)

# Add multiple items
person.addresses.add(
    {"type": "work", "street": "456 Oak Ave", "city": "LA"},
    {"type": "vacation", "street": "789 Beach Rd", "city": "Miami"}
)

# Access array items
first_address = person.addresses[0]
first_address.street = "Updated Street"
```

### 6. Saving Documents

```python
# Save new document
person = People(name="Alice", age=25)
person.save()  # Inserts into MongoDB
print(person._id)  # ObjectId is auto-generated

# Update existing document
person.age = 26
person.save()  # Updates the document
```

### 7. Querying Documents

```python
# Find one document
person = People.find_one({"name": "Alice"})

# Find many with options
people = People.find_many(
    filter={"age": {"$gte": 18}},
    sort=[("age", -1)],
    limit=10
)

# Query with projection
people = People.query(
    filter={"age": {"$gte": 18}},
    projection={"name": 1, "age": 1},
    sort=[("name", 1)],
    limit=20
)

# Count documents
count = People.count({"age": {"$gte": 18}})

# Check existence
exists = People.exists({"email": "alice@example.com"})
```

### 8. Updating Documents

```python
# Update one
People.update_one(
    {"name": "Alice"},
    {"$set": {"age": 30}}
)

# Update many
People.update_many(
    {"age": {"$lt": 18}},
    {"$set": {"category": "minor"}}
)

# Find and modify
updated_doc = People.find_and_modify(
    {"name": "Alice"},
    {"$inc": {"age": 1}}
)
```

### 9. Deleting Documents

```python
# Delete instance
person = People.find_one({"name": "Alice"})
person.delete()

# Delete by ID
People.delete_by_id(object_id)

# Delete many
People.delete_many({"age": {"$lt": 0}})

# Soft delete (sets is_deleted=True)
People.soft_delete({"status": "inactive"})

# Restore soft deleted
People.restore_deleted({"status": "inactive"})
```

### 10. Serialization

```python
# To dictionary
person_dict = person.to_dict()

# From dictionary
person = People.from_dict(person_dict)

# To JSON
import json
json_str = json.dumps(person.to_dict(), default=str)
```

### 11. Data Analysis

```python
# Get summary statistics
summary = People.summarize(sample_size=1000, top=10)
print(summary)
# Returns: field types, counts, missing values, min/max, top values, etc.
```

### 12. Advanced Queries

```python
# Regex search
results = People.regex_query(
    field="name",
    pattern="^John",
    options="i"
)

# Text search (requires text index)
results = People.text_search("doctor physician")

# Aggregation pipeline
pipeline = [
    {"$match": {"age": {"$gte": 18}}},
    {"$group": {"_id": "$city", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
results = People.aggregate(pipeline)

# Pagination
page_1 = People.paginate(filter={}, page=1, page_size=20)
page_2 = People.paginate(filter={}, page=2, page_size=20)
```

### 13. Comparison

```python
person1 = People(name="Alice", age=30)
person2 = {"name": "Alice", "age": "30"}  # age is string

# Compare with strict type checking
diff = People.diff(person1, person2, strict=True)
# Returns: {'age': {'old': 30, 'new': '30', 'type_changed': True}}
```

### 14. Lifecycle Hooks

```python
from mso import get_model
from mso.base_model import MongoModel, pre_save, post_save, pre_delete, post_delete

# Extend the model class
class CustomPeople(MongoModel):
    @pre_save
    def before_save(self):
        print(f"About to save: {self.name}")
        # Modify data before saving
        if not hasattr(self, 'created_at'):
            self.created_at = datetime.now()
    
    @post_save
    def after_save(self):
        print(f"Saved: {self.name}")
    
    @pre_delete
    def before_delete(self):
        print(f"About to delete: {self.name}")
    
    @post_delete
    def after_delete(self):
        print(f"Deleted document")

# Get model and apply hooks
People = get_model(db, "people")
# Apply your custom methods to the generated class
```

## Common Patterns for AI Assistants

### Pattern 1: CRUD Operations
```python
from mso import connect_to_mongo, get_model

db = connect_to_mongo("mongodb://localhost:27017", "myapp")
User = get_model(db, "users")

# Create
user = User(username="alice", email="alice@example.com")
user.save()

# Read
user = User.find_one({"username": "alice"})

# Update
user.email = "newemail@example.com"
user.save()

# Delete
user.delete()
```

### Pattern 2: Working with Nested Data
```python
Person = get_model(db, "people")

person = Person(name="John")
person.address.street = "123 Main St"
person.address.city = "NYC"
person.contacts.add(type="email", value="john@example.com")
person.contacts.add(type="phone", value="555-1234")
person.save()
```

### Pattern 3: Bulk Operations
```python
People = get_model(db, "people")

# Create multiple documents
people = [
    People(name=f"Person {i}", age=20+i)
    for i in range(100)
]
People.bulk_save(people)

# Query and update
all_people = People.find_many({})
for person in all_people:
    person.status = "active"
    person.save()
```

### Pattern 4: Error Handling
```python
from pymongo.errors import ConnectionFailure, ConfigurationError
from mso import connect_to_mongo

try:
    db = connect_to_mongo("mongodb://localhost:27017", "mydb", timeout=5000)
    Model = get_model(db, "collection")
except ConnectionFailure as e:
    print(f"Cannot connect to MongoDB: {e}")
except ConfigurationError as e:
    print(f"Invalid MongoDB URI: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Important Notes for AI Assistants

1. **Never import `MongoClient` directly** - always use `connect_to_mongo()`
2. **Models are dynamic** - they're generated from MongoDB schemas, not defined in code
3. **Nested objects auto-create** - accessing `person.address.city` creates the nested structure
4. **Arrays use `.add()`** - not `.append()` for nested object arrays
5. **Always call `.save()`** - changes aren't persisted until you call `.save()`
6. **Type hints are limited** - models are dynamically generated, use runtime checks
7. **Schema must exist** - the MongoDB collection must have a `$jsonSchema` validator

## REST API Generation

```python
from mso import connect_to_mongo
from mso.api import start_api

db = connect_to_mongo("mongodb://localhost:27017", "mydb")

# Auto-generate REST API with Swagger docs
start_api(
    db=db,
    collections=["*"],  # All collections, or ["users", "products"]
    port=8000
)

# Access at: http://localhost:8000/docs
```

## Complete Example

```python
from mso import connect_to_mongo, get_model

# Connect
db = connect_to_mongo("mongodb://localhost:27017", "company")

# Get model
Employee = get_model(db, "employees")

# Create employee
emp = Employee(
    name="Jane Smith",
    employee_id="E12345",
    email="jane@company.com"
)

# Add nested data
emp.department.name = "Engineering"
emp.department.manager = "John Doe"

# Add array items
emp.skills.add(name="Python", level="Expert")
emp.skills.add(name="MongoDB", level="Advanced")

# Add contact info
emp.contacts.add(type="work", phone="555-1234")
emp.contacts.add(type="mobile", phone="555-5678")

# Save
emp.save()
print(f"Created employee with ID: {emp._id}")

# Query
engineers = Employee.find_many({"department.name": "Engineering"})
for e in engineers:
    print(f"{e.name}: {e.email}")

# Update
emp.department.name = "Senior Engineering"
emp.save()

# Get summary
stats = Employee.summarize(top=5)
print(stats)
```

## TypeScript-Style Interface (For Reference)

While MSO is Python, here's what the generated model looks like conceptually:

```typescript
// This is for AI understanding - not actual code
interface People {
    _id: ObjectId;
    name: string;
    age: number;
    email?: string;
    addresses: Array<{
        type: "home" | "work" | "other";
        street: string;
        city: string;
        state: string;
        zip: string;
    }>;
    health: {
        primary_physician: {
            name: string;
            contact: {
                phone: string;
                address: {
                    street: string;
                    city: string;
                    state: string;
                    zip: string;
                }
            }
        };
        medical_history: {
            conditions: Array<{
                name: string;
                diagnosed: string;
            }>;
            allergies: string[];
        }
    };
    created_at?: Date;
    updated_at?: Date;
}
```

## Troubleshooting

**Problem**: `AttributeError: 'NoneType' object has no attribute 'save'`
**Solution**: Check if `find_one()` returned None (no matching document)

```python
person = People.find_one({"name": "Alice"})
if person:
    person.save()
else:
    print("Person not found")
```

**Problem**: `KeyError` when accessing nested field
**Solution**: Use `getattr()` with default or check existence

```python
# Safe access
phone = getattr(person.health.primary_physician.contact, 'phone', None)
```

**Problem**: Array `.append()` doesn't work for nested objects
**Solution**: Use `.add()` instead

```python
# Wrong
person.addresses.append({"type": "home", "street": "123 Main"})

# Right
person.addresses.add(type="home", street="123 Main")
```
