# MSO Library - Quick Reference for AI Assistants

## Installation
```bash
pip install mso
```

## Essential Imports
```python
from mso import connect_to_mongo, get_model
```

## Connection (Always Required First)
```python
db = connect_to_mongo("mongodb://localhost:27017", "database-name")
```

## Get Model (Required Before Using Collection)
```python
ModelName = get_model(db, "collection_name")
```

## Create Document
```python
doc = ModelName(field1="value", field2=123)
doc.save()
```

## Read Documents
```python
# Find one
doc = ModelName.find_one({"field": "value"})

# Find many
docs = ModelName.find_many({"field": "value"}, limit=10)
```

## Update Document
```python
doc.field = "new_value"
doc.save()
```

## Delete Document
```python
doc.delete()
```

## Nested Objects (Auto-created)
```python
doc.nested.field = "value"
doc.nested.deeper.field = "value"
```

## Arrays (Use .add() method)
```python
doc.array_field.add(key1="value1", key2="value2")
```

## Common Queries
```python
# Count
count = ModelName.count({"field": "value"})

# Exists
exists = ModelName.exists({"field": "value"})

# Regex
results = ModelName.regex_query("field", "pattern")
```

## Error Handling
```python
try:
    db = connect_to_mongo("mongodb://localhost:27017", "db-name", timeout=5000)
except Exception as e:
    print(f"Connection failed: {e}")
```

## Key Rules
1. Always use `connect_to_mongo()` - never `MongoClient()`
2. Always call `get_model(db, "collection")` before using a collection
3. Nested objects are accessed with dots and auto-create
4. Array items use `.add()` not `.append()`
5. Changes require `.save()` to persist
6. MongoDB collection must have `$jsonSchema` validator defined
