# MSO Library Usage Examples

## Example 1: Basic CRUD
```python
from mso import connect_to_mongo, get_model

db = connect_to_mongo("mongodb://localhost:27017", "db-name")
People = get_model(db, "people")

# CREATE
person = People(name="Alice", age=30, email="alice@example.com")
person.save()

# READ
person = People.find_one({"name": "Alice"})
print(f"{person.name} is {person.age} years old")

# UPDATE
person.age = 31
person.save()

# DELETE
person.delete()
```

## Example 2: Nested Objects
```python
from mso import connect_to_mongo, get_model

db = connect_to_mongo("mongodb://localhost:27017", "db-name")
People = get_model(db, "people")

person = People(name="Bob")
person.health.primary_physician.name = "Dr. Strange"
person.health.primary_physician.contact.phone = "555-1234"
person.save()
```

## Example 3: Array Fields
```python
from mso import connect_to_mongo, get_model

db = connect_to_mongo("mongodb://localhost:27017", "db-name")
People = get_model(db, "people")

person = People(name="Charlie")
person.addresses.add(type="home", street="123 Main St", city="NYC", state="NY", zip="10001")
person.addresses.add(type="work", street="456 Office Blvd", city="LA", state="CA", zip="90001")
person.save()
```

## Example 4: Querying
```python
from mso import connect_to_mongo, get_model

db = connect_to_mongo("mongodb://localhost:27017", "db-name")
People = get_model(db, "people")

# Find one
person = People.find_one({"email": "alice@example.com"})

# Find many with filter
adults = People.find_many({"age": {"$gte": 18}}, sort=[("age", -1)], limit=10)

# Count
total = People.count({"age": {"$gte": 18}})

# Check existence
exists = People.exists({"email": "alice@example.com"})
```

## Example 5: Bulk Operations
```python
from mso import connect_to_mongo, get_model

db = connect_to_mongo("mongodb://localhost:27017", "db-name")
People = get_model(db, "people")

# Create multiple
people = [People(name=f"Person {i}", age=20+i) for i in range(10)]
People.bulk_save(people)

# Update many
People.update_many({"age": {"$lt": 18}}, {"$set": {"status": "minor"}})
```

## Example 6: Aggregation
```python
from mso import connect_to_mongo, get_model

db = connect_to_mongo("mongodb://localhost:27017", "db-name")
People = get_model(db, "people")

pipeline = [
    {"$match": {"age": {"$gte": 18}}},
    {"$group": {"_id": "$city", "count": {"$sum": 1}, "avg_age": {"$avg": "$age"}}},
    {"$sort": {"count": -1}}
]
results = People.aggregate(pipeline)
```

## Example 7: REST API
```python
from mso import connect_to_mongo
from mso.api import start_api

db = connect_to_mongo("mongodb://localhost:27017", "db-name")
start_api(db, collections=["*"], port=8000)
# Visit http://localhost:8000/docs for Swagger UI
```
