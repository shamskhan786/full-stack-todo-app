--- 
name: backend-skill
description: Generate backend routes, handle requests and responses, and connect to databases. Use for building API endpoints and server logic.
---

# Backend Skill – Routes, Requests, Responses, and Database Connection

## Instructions

1. **Route Creation**
   - Define API endpoints (GET, POST, PUT, DELETE)
   - Organize routes by resource (e.g., /users, /products)
   - Use proper naming conventions for clarity

2. **Request Handling**
   - Parse incoming requests (body, query, params)
   - Validate input data
   - Handle authentication and authorization if needed

3. **Response Handling**
   - Send appropriate status codes (200, 201, 400, 404, 500)
   - Return JSON-formatted responses
   - Include error messages when necessary

4. **Database Connection**
   - Connect to SQL or NoSQL databases (e.g., PostgreSQL, MongoDB)
   - Perform CRUD operations efficiently
   - Ensure proper error handling and connection closing

## Best Practices
- Keep routes modular and organized
- Validate all inputs to avoid security issues
- Handle errors gracefully with informative messages
- Follow RESTful API conventions
- Ensure database queries are optimized

## Example Structure
```javascript
// Example Express.js route
import express from 'express';
import db from './db.js';

const router = express.Router();

// GET /users
router.get('/users', async (req, res) => {
  try {
    const users = await db.query('SELECT * FROM users');
    res
