**Model Fields & Relationships Markdown**

✔ A **BaseModel** in the `base` app
✔ A `utils/` folder note inside the `base` app
✔ Updated **Blog** model fields
✔ Use of **CKEditor** for blog content
✔ Inheritance from BaseModel (created_at, updated_at, created_by, updated_by)


---

#  **Model Field Documentation — Django CMS API**

### *(Structure, fields, descriptions, and relationships)*

This document defines the models and their fields used across the CMS backend.
It also describes shared base models and application-level utilities.

---

#  **Base App**

## **BaseModel**

### Purpose:

Provides common audit fields used by all models in the system.
Every model in the project will inherit from this BaseModel.

### Fields:

| Field      | Type               | Description                                               |
| ---------- | ------------------ | --------------------------------------------------------- |
| created_at | datetime           | Timestamp when the record was created (auto set)          |
| updated_at | datetime           | Timestamp when the record was last updated (auto updated) |
| created_by | FK(User, nullable) | User who created the record (optional)                    |
| updated_by | FK(User, nullable) | User who last modified the record (optional)              |

### Notes:

* All Blog and Contact models inherit these fields.
* `created_by` and `updated_by` will typically be used for admin/staff actions.

---

## **Utils Folder (`base/utils/`)**

### Purpose:

Contains helper functions shared across apps.

### Examples of utilities:

* slug generation
* model field validation helpers
* common formatting utilities
* audit helpers (for setting created_by, updated_by)

No business logic should be placed here — only low-level reusable helpers.

---

#  **Blog App Models**

## **1. Category**

### Purpose:

Defines organizational categories for blog posts.

### Fields:

| Field       | Type            | Description                            |
| ----------- | --------------- | -------------------------------------- |
| name        | string          | Category name                          |
| slug        | string          | URL-friendly and unique identifier     |
| description | text (optional) | Explanation or purpose of the category |

### Inherits:

* **BaseModel** → adds audit + timestamps

### Relationships:

* One-to-Many: **One Category → Many Blog posts**

---

## **2. Blog**

### Purpose:

Represents a blog post displayed on the CMS website.

### Fields:

| Field             | Type                 | Description                             |
| ----------------- | -------------------- | --------------------------------------- |
| title             | string               | Title of the blog post                  |
| slug              | string               | Unique URL-friendly blog identifier     |
| short_description | text                 | Brief summary shown on list pages       |
| content           | rich text (CKEditor) | Full article body stored using CKEditor |
| thumbnail         | image                | Cloudflare-stored featured image        |
| category          | FK(Category)         | Blog's category                         |
| is_published      | boolean              | Determines if blog is visible to public |

### Inherits:

* **BaseModel** → created_at, updated_at, created_by, updated_by

### Relationships:

* Blog → belongs to one Category
* Category → contains many Blogs

### Notes:

* CKEditor will store the rich text content.
* Slug should remain unique for SEO-friendly URLs.

---

# ✉️ **Contact App Models**

## **1. ContactMessage**

### Purpose:

Stores messages submitted from the website contact form.

### Fields:

| Field     | Type   | Description                 |
| --------- | ------ | --------------------------- |
| full_name | string | Name of sender              |
| email     | string | Email of sender             |
| subject   | string | Subject line of the message |
| message   | text   | Main content of the inquiry |

### Inherits:

* **BaseModel**

### Relationships:

* None — purely a data model used by admin + service layer.

---

#  **General Modeling Rules**

* All models requiring timestamps or user tracking must inherit from `BaseModel`.
* Models containing images must use Cloudflare R2 storage backend.
* Rich content fields (not plain text) must use CKEditor.
* Slugs must be unique and generally auto-generated when needed.
* Admin users performing CRUD operations should populate created_by / updated_by automatically.

