'''
Using jsonschema to validate our inbound json request to make sure
it has the required fields and values
'''
schema = {
    "type": "object",
    "properties": {
        "first_name":     {"type": "string"},
        "last_name":      {"type": "string"},
        "service":        {"type": "string"},
        "status":         {"type": "string"},
        "street_address": {"type": "string"},
        "city":           {"type": "string"},
        "state":          {"type": "string", "pattern": "^[A-Z]{2}$"},
        "zip":            {"type": "string", "pattern": "^[0-9]{5}$"},
        "phone":          {"type": "string", "pattern": "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"},
        "date":           {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"},
        "price":          {"type": "string"},
    },
    "required": ["first_name", "last_name", "service", "status", "street_address", "city", "state", "zip", "phone",
                 "date", "price"]
}


schema_put = {
    "type": "object",
    "properties": {
        "status": {"type": "string"}
    },
    "required": ["status"]
}

