---
name: auth-skill
description: Handle user authentication with signup, signin, password hashing, JWT tokens, and better auth integration.
---

# Auth Skill – Signup, Signin, Password Hashing, JWT Tokens

## Instructions

1. **User Signup**
   - Accept user credentials (email, password, etc.)
   - Hash passwords securely using algorithms like bcrypt
   - Store user data safely in the database

2. **User Signin**
   - Verify email and password
   - Compare hashed passwords securely
   - Return JWT token for session management

3. **JWT Token Management**
   - Generate JWT tokens upon successful signin
   - Include expiry and secure claims
   - Verify JWT on protected routes

4. **Password Security**
   - Hash passwords before storage
   - Use salting to enhance security
   - Provide password reset functionality if needed

5. **Integration Best Practices**
   - Keep authentication logic modular
   - Use environment variables for secret keys
   - Ensure HTTPS for token transmission
   - Validate inputs to prevent injection attacks

## Best Practices
- Never store plain text passwords
- Keep JWT secret keys safe
- Expire tokens after a reasonable time
- Implement rate limiting to prevent brute-force attacks

## Example Structure (Node.js / Express)
```javascript
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

// Signup
const hashedPassword = await bcrypt.hash(password, 10);
await User.create({ email, password: hashedPassword });

// Signin
const user = await User.findOne({ email });
const valid = await bcrypt.compare(password, user.password);
if(valid) {
  const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.json({ token });
}
