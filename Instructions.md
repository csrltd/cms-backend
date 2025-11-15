#  Development Instructions — Django CMS API

This document defines strict rules all developers must follow while building the backend.  
These apply to **repository**, **service**, and **view** layers.

---

#  1. Response Classes (Mandatory Usage)

### **Repository Layer Must Return → `RepositoryResponse`**
Structure:

- `success`: boolean  
- `message`: string  
- `data`: dictionary, list, model instance, or optional

### **Service Layer Must Return → `APIResponse`**
Structure:

- `success`: boolean  
- `message`: string  
- `data`: dictionary, list, model instance, or optional  
- `status`: HTTP status code or response status indicator  

### Why this matters:
- Ensures consistent response formatting across the entire API  
- Separates low-level repository messages from high-level service responses  
- Prevents leaking internal exceptions to the API layer  

---

#  2. Try/Except Required in All Layers

Every repository and service method **must** wrap logic in a `try/except` block.

### Repository Rules:
- Catch all unexpected exceptions  
- Log the error  
- Return `RepositoryResponse(success=False, message="error message", data=None)`  

### Service Rules:
- Always wrap repository calls in try/except  
- Log errors that come from repository or service logic  
- Return appropriate `APIResponse` with clear messages and status codes  

### View Rules:
- Do NOT perform business logic  
- Views should only call service functions  
- Ensure service errors are returned as DRF responses  

---

#  3. Logging Requirements

Every app must include logging to capture:

- Repository errors  
- Service errors  
- External integration failures (Cloudflare, Postmark, Celery, Redis)  

Logs must include:

- The action attempted  
- The exception message  
- Any relevant identifiers (blog ID, contact ID, category, etc.)  

Logging should **never expose sensitive data**.

---

#  4. Architecture Enforcement (N-Tier Rules)

### Views:
- No direct model access  
- No business logic  
- Only responsible for:
  - calling service methods  
  - returning DRF responses  

### Services:
- Contain **all business logic**  
- Can call:
  - their own repositories  
  - other services  
  - external integrations  
- Must perform validation and error interpretation  
- Must return `APIResponse`

### Repositories:
- Only talk to the database  
- No business rules  
- Must return `RepositoryResponse`  

---

#  5. Testing Rules

### Tools Required:
- `unittest`  
- `factory_boy`  
- `faker`  

### Requirements:
- Each app must have:
  - `test_repository.py`
  - `test_service.py`
  - `factories.py`

- All tests must use Factory Boy for model creation  
- All tests must mock:
  - Postmark email calls  
  - Celery background tasks  
  - Redis caching where relevant  

### No PR should be raised unless **all tests pass** for the work completed.

---

#  6. Authentication & Permissions

### Rules:
- Blog listing: **public**  
- Blog create, update, delete: **protected** (requires authentication)  
- Contact submission: **public**  

Admin actions (approval, editing, reviewing messages) are handled via Django Admin only — not through API endpoints.

---

#  7. Utility & BaseModel Rules

### BaseModel:
All models must inherit common fields:
- `created_at`  
- `updated_at`  
- `created_by`  
- `updated_by`

### Utils Folder:
The `base/utils/` directory holds:
- slug/ID generators  
- validation helpers  
- shared formatting helpers  
- audit helpers  
No business logic allowed here.

---

#  8. External Integrations

### Cloudflare:
- Used for all media storage  
- Must handle integration errors in services and log them

### Postmark:
- Email sending must happen through Celery  
- Direct email sending from services is allowed only through Celery tasks  
- Failures must be logged

### Redis:
- Used for caching blog list results  
- Cache must invalidate on create/update/delete  

---

#  9. Requirements & Dependencies

Whenever a developer installs a new package:

1. Install the package  
2. Run `pip freeze > requirements.txt`  
3. Commit the updated requirements file  

---

#  10. Commit & PR Standards

### Commit Messages:
- Must be meaningful  
- Must reflect the actual layer changed  
- Examples:
  - `feat(blog-service): add create blog service logic`
  - `fix(contact-repo): correct message save handling`
  - `test(blog-repository): add tests for update method`

### PR Description:
- Must include:
  - What was implemented  
  - Why it was implemented  
  - Tests included  
  - Any architectural decisions  
- PR must not be raised unless **all tests pass** locally.

---

#  Final Rule

All developers must respect this architecture to maintain system consistency.  
Any deviation must be justified and approved by the technical lead.
