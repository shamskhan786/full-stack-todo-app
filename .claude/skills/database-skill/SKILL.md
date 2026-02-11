---
name: database-skill
description: Create tables, manage migrations, and design schemas for relational databases. Use for efficient database setup and management.
---

# Database Skill

## Instructions

1. **Schema Design**
   - Define clear table structures
   - Establish relationships (one-to-one, one-to-many, many-to-many)
   - Use appropriate data types for each column
   - Normalize data where necessary to reduce redundancy

2. **Table Creation**
   - Write SQL `CREATE TABLE` statements or use ORM models
   - Include primary keys, foreign keys, and unique constraints
   - Add indexes for faster query performance

3. **Migrations**
   - Create migration scripts for schema changes
   - Ensure backward compatibility for production data
   - Use version control for migration files

4. **Data Integrity**
   - Apply constraints (NOT NULL, UNIQUE, CHECK)
   - Use triggers or stored procedures if necessary
   - Plan for soft deletes and audit trails

## Best Practices
- Use meaningful table and column names
- Keep schemas consistent across environments
- Avoid redundant data; normalize properly
- Document relationships and constraints
- Test migrations in staging before production
