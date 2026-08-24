# Instructions: Read in English, generate the final bug report strictly in Russian.

Transform the provided raw defect data, API logs, and database inspection results into a structured, professional Bug Report.

Raw Defect Data:
[PASTE_ERROR_LOGS_CURL_OR_MCP_SQL_OUTPUT]

Format the Bug Report in Russian strictly using this structure:
- **Title (Заголовок):** [Component] + [What happens] + [Under what conditions]
- **Severity / Priority:** (Blocker / Critical / Major / Minor / Trivial) with justification
- **Environment:** Docker Compose, FastAPI, PostgreSQL 16
- **Preconditions (Предусловия):** Initial database records
- **Steps to Reproduce (Шаги для воспроизведения):** Numbered steps (cURL / HTTP request & MCP verification)
- **Actual Result (Фактический результат):** Real response / error code / DB state
- **Expected Result (Ожидаемый результат):** Expected behavior according to specifications
- **Root Cause Analysis (Предполагаемая причина):** Suspected code/schema issue in `app/` or DDL

CRITICAL FORMATTING LAW FOR LINKS:
- NEVER append line numbers or colons to file paths in Markdown links (NO `:10`, NO `:2`, NO `:272`).
- Use plain, clean relative Markdown links (e.g. `[01_schema.sql](../docker/init-db/01_schema.sql)`).
