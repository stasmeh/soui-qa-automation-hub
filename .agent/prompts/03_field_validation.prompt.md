# Instructions: Read in English, generate all output strictly in Russian.

Generate test cases for input & field validation:

Entity / Schema Name: [SCHEMA_OR_ENDPOINT_NAME]
Fields: [LIST_ALL_FIELDS_WITH_VALIDATION_RULES]
Database Constraints (PostgreSQL): [LIST_CHECK_AND_NOT_NULL_CONSTRAINTS]

Create test cases for:
- Required field validation (FastAPI / Pydantic 422 errors)
- Data type validation (string vs integer, invalid UUIDs)
- Format validation (email, dates)
- Length constraints (empty strings `""`, whitespace, exceeding VARCHAR length)
- Boundary checks & PostgreSQL CHECK constraint violations (e.g., grade < 1 or > 5)

Format output as a Markdown table in Russian:
`| Поле | Тестовое значение | Ожидаемый код ответа | Слой перехвата (Pydantic / DB Check) | Ожидаемое поведение |`