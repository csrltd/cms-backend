#  **Django CMS API**

### **Team:** Tuombe • Paccy • Christian  
Each person has **unique work every day**, and all tasks are coordinated so the project finishes in 5 working days.

All tests must use **Factory Boy + Faker** for generating test data.  
Each app will have its own `factories.py` file inside the `tests/` folder.

---

#  **DAY 1 — Initialization & Base Structure**

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

#  **DAY 2 — Models & Serializers**

### **Tuombe**
* Implement `Category` and `Blog` models  
* Create blog serializers  
* Add blog factories in `tests/factories.py` using Factory Boy + Faker  
* Push updates and raise PR (tests must pass)  
* Update requirements if new package installed  

### **Paccy**
* Implement `ContactMessage` model  
* Create serializer for contact messages  
* Add contact factories using Factory Boy + Faker  
* Push updates and raise PR  
* Update requirements if needed  

### **Christian**
* Start configuring Cloudflare storage in settings  
* Add model media upload fields pointing to Cloudflare paths  
* Prepare `.env.example` for Cloudflare variables  
* Update requirements if needed  

---

#  **DAY 3 — Repository Layer + Tests**

### **Tuombe**
* Implement Blog repository functions:  
  * create, get, update, delete, list  
* Write repository tests using **Factory Boy data**  
* Ensure test coverage for success/failure  

### **Paccy**
* Implement repository functions for ContactMessage:  
  * create, list  
* Write repository tests using **Factory Boy data**  
* Ensure tests pass before PR  

### **Christian**
* Set up Redis caching for blog list  
* Configure Celery worker + beat + Redis  
* Prepare base Celery configuration module  
* Test worker startup  

---

#  **DAY 4 — Service Layer + Tests**

### **Tuombe**
* Implement Blog services:  
  * create_blog()  
  * update_blog()  
  * delete_blog()  
  * list_blogs() → includes Redis caching  
* Write full service tests (Factory Boy + mocks)  
* Use `APIResponse` for return values  

### **Paccy**
* Implement Contact services:  
  * save_contact_message()  
  * send_email_via_postmark() → queued via Celery  
* Write service tests (mock email + Celery tasks)  

### **Christian**
* Integrate Postmark  
* Implement Celery task for sending emails  
* Ensure task uses Postmark correctly  
* Add logging utilities  
* Write tests for Celery email task (mocked)  

---

#  **DAY 5 — Views, URLs, Permissions & Final QA**

### **Tuombe**
* Create blog API views using `@api_view`:  
  * list (public)  
  * create/update/delete (protected)  
* Wire blog URLs in `api/urls/blog/urls.py`  
* Final test on all blog endpoints  
* Raise PR  

### **Paccy**
* Create contact API view using `@api_view`:  
  * Public submission endpoint  
* Wire contact URLs in `api/urls/contact/urls.py`  
* Final tests for repository/service integration  
* Raise PR  

### **Christian**
* Improve settings structure (dev/prod separation)  
* Ensure all secrets use `.env`  
* Generate final `README.md` including:  
  * Celery usage  
  * Redis usage  
  * Cloudflare setup  
  * API examples  
* Run full test suite  
* Raise PR  

---

# **Final Notes**

* **PRs must NOT be raised when tests fail.**
* All developers work strictly in feature branches.
* All final merges require lead review.
* All sensitive values must be in `.env`.
* Requirements must be updated whenever packages change.
