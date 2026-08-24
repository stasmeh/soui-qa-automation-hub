# Instructions: Read in English, generate all output strictly in Russian.

Create functional test cases for CRUD operations on [ENTITY_NAME] (e.g., Students, Courses, Grades):

Entity Fields: [LIST_FIELDS_AND_TYPES]
Business Rules: [DESCRIBE_RULES]
MCP Tool: Use `postgres-soui` to verify schema, Foreign Keys, and constraints.

Generate test cases for:
- **Create:** Valid/invalid data, required fields, defaults, duplicate unique keys.
- **Read:** Single record, multiple records, filtering, sorting, non-existent ID (404).
- **Update:** Partial updates, full updates, invalid FK references.
- **Delete:** Single delete, cascade effects, orphaned records validation via MCP SQL queries.

Format each test case in Russian with:
- Test ID
- Action (Действие: Create / Read / Update / Delete)
- Preconditions (Предусловия)
- Steps (Шаги с HTTP-запросом и SQL)
- Expected Result (Ожидаемый результат)
- Actual/DB Verification (Проверка через MCP)