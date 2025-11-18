# **Django CMS API**

### **Team:** Tuombe • Paccy • Christian

Each person has **unique work every day**, and all tasks are coordinated so the project finishes in 5 working days.

All tests must use **Factory Boy + Faker** for generating test data.
Each app will have its own `factories.py` file inside the `tests/` folder.

---

# **DAY 1 — Initialization & Base Structure**

### **Christian**

* Initialize Django project
* Create apps: `blog`, `contact`, `api`
* Configure `.env` loading & basic settings
* Install DRF + Celery + Redis + Postmark + Cloudflare
* Install **factory_boy** and **faker**
* Run `pip freeze > requirements.txt`
* Push initial setup to GitHub
* Create branch: `feature/setup-christian`

### **Paccy**

* Set up **blog app folder architecture**:
  * `repository/`, `service/`, `tests/`
* Create empty test files:
  * `test_repository.py`
  * `test_service.py`
  * `factories.py` (for Factory Boy)
* Create branch: `feature/blog-structure-paccy`

### **Tuombe**

* Set up **contact app folder architecture**:
  * `repository/`, `service/`, `tests/`
* Prepare empty test files:
  * `test_repository.py`
  * `test_service.py`
  * `factories.py`
* Create branch: `feature/contact-structure-tuombe`

---


# **DAY 2 — Models, Serializers & Repository Layer**

### **Paccy — Blog App**

* Implement `Category` model
* Implement `Blog` model
* Create blog serializers
* Add Factory Boy factories in `tests/factories.py`
* Implement blog repository functions:
  * create
  * get
  * list
  * update
  * delete
* Write repository tests
* Push updates

---

### **Christian — Contact App**

* Implement `ContactMessage` model
* Create serializer for contact
* Add Factory Boy factories
* Implement contact repository functions:
  * create
  * list
* Write repository tests
* Push updates

---

### **Tuombe — Cloud & Background Setup**

* Configure Cloudflare media storage
* Configure Redis caching (base settings)
* Configure Celery worker + beat
* Add `.env.example` variables
* Push updates

---

# **DAY 3 — Service Layer + API Endpoints**

### **Paccy — Blog Services & Views**

* Implement blog services:
  * `create_blog()`
  * `update_blog()`
  * `delete_blog()`
  * `list_blogs()`
* Write service tests
* Create blog API views with `@api_view`
* Add blog URLs under `api/urls/blog/`
* Push updates

---

### **Christian — Contact Services & Views**

* Implement contact services:
  * `save_contact_message()`
  * `send_email_notification()` (call Celery task if available)
* Write service tests
* Create contact API endpoint
* Add URLs under `api/urls/contact/`
* Push updates

---

### **Tuombe — Email Task + Extra Setup**

* Implement Postmark email Celery task
* Add logging
* Configure remaining Redis or Celery details
* Push updates

---

# **DAY 4 & DAY 5 — Full Testing, Debugging & Final Documentation**

### **All Developers**

* Run entire test suite
* Fix failing tests
* Fix broken endpoints
* Improve service logic
* Adjust models or serializers when needed
* Improve permissions and error responses
* Validate API manually with Postman
* Update README with usage examples
* Confirm `.env` variables setup
* Ensure branches are clean and ready for final PRs

---

# **FINAL NOTES**

* All work must be in feature branches
* Tests must pass before PR
* Requirements updated whenever packages change
* If a task cannot be completed, leave:

  **“to be implemented later”**
