---
name: prime-review
description: Prime context for security and quality review tasks
argument-hint: [review focus area]
---

# Security Review Context Priming

Use the reviewer agent to prepare context for security and quality analysis: $ARGUMENTS

## Purpose
Load focused context for conducting security reviews, code quality assessments, and compliance checks.

## Workflow
1. **Survey codebase scope** - Identify security-critical areas
2. **Analyze attack surfaces** - API endpoints, user inputs, data handling
3. **Review authentication/authorization** - Access controls and permissions
4. **Examine data flow** - Sensitive data handling and validation
5. **Check dependencies** - Third-party libraries and security updates

The reviewer agent will:
- Identify high-risk code areas and entry points
- Map authentication and authorization mechanisms
- Examine input validation and sanitization
- Review data storage and transmission security
- Check for common vulnerability patterns
- Assess dependency security and updates
- Prepare focused security context

**Review Focus**: Use $ARGUMENTS to specify review area (e.g., "API security", "user input validation", "data encryption", "authentication flows")