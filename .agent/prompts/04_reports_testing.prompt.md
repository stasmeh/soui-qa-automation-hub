# Instructions: Read in English, generate all output strictly in Russian.

Generate test cases for reporting and analytics feature:

Report Name: [REPORT_NAME] (e.g., Student Performance Summary, Grade Sheet)
Data Source: PostgreSQL views / `sql-tests/02_business_logic_reports.sql`
Filters/Parameters: [LIST_PARAMETERS] (e.g., group_id, course_id, min_grade)
Output Format: JSON API response / Tabular data

Cover:
- Report generation with various query filter combinations
- Data calculation & aggregation accuracy (AVG grade, GPA calculation)
- Division by zero / handling students with 0 grades
- Empty result handling (valid empty response vs 500 error)
- Direct data reconciliation (API response vs direct SQL result via `postgres-soui` MCP)

Format each test scenario in Russian:
- Scenario ID
- Parameters (Параметры фильтрации)
- Steps (Шаги выполнения)
- Expected Calculation / Output (Ожидаемый расчет и структура)
- MCP SQL Verification Query (SQL-запрос сверки)