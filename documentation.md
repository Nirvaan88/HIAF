# HIAF: Employee Management System Documentation

This document provides a comprehensive technical and functional overview of the HIAF Employee Management System.

---

## 1. System Overview

HIAF is a web-based application built with **Flask (Python)** and **MongoDB**. It serves as an employee profile management system where employees can fill out their comprehensive details (including family data), and administrators can view, manage, and export this data.

### 1.1 Key Technologies
* **Backend:** Flask, PyMongo (MongoDB driver), Werkzeug (Security/Password hashing)
* **Frontend:** HTML5, Bootstrap 5 (CSS framework), Vanilla JavaScript for dynamic interactions
* **Database:** MongoDB (Collections: `employees`)

### 1.2 User Roles
* **Admin:** Full access. Can add new employees, view all profiles, delete employees (individually or in bulk), and export data to CSV/Excel. Can edit completed profiles.
* **User (Employee):** Limited access. Can log in to complete their profile. Once submitted, their profile becomes read-only, and they must contact an admin for further changes.

---

## 2. Page-by-Page Feature Breakdown

### 2.1 Login / Landing Page (`landing.html` & `auth.py`)
* **Purpose:** Entry point of the application.
* **Features:** 
  * Accepts Employee ID and Password.
  * Routes the user to either the User Dashboard or Admin Dashboard based on their role.

### 2.2 Admin Dashboard (`admin_dashboard.html` & `admin.py`)
* **Purpose:** Central hub for administrators to manage all employees.
* **Features:**
  * **Employee Listing:** Tabular view of all registered employees with visual indicators (e.g., pink rows) for incomplete profiles.
  * **Search/Filter:** Real-time search by name, employee ID, email, phone, etc.
  * **Bulk Operations:** Checkboxes for selecting multiple employees to perform bulk deletions.
  * **Individual Actions:** View or Delete specific employees.
  * **Exporting:** Export filtered or selected employee lists to CSV or Excel (`export.py`).
  * **Add Employee:** Admins can pre-register employees by setting up initial credentials.

### 2.3 User Dashboard (`dashboard.html`)
* **Purpose:** Landing page for standard employees post-login.
* **Features:**
  * Displays the current profile completion status (Complete vs. Incomplete).
  * Provides a direct link to the Profile Completion form.

### 2.4 Profile Completion Form (`complete_profile.html` & `main.py`)
* **Purpose:** The core data-entry interface where employees provide exhaustive personal and familial details.
* **Features:**
  * **Draft Saving:** Autosaves progress before final submission via AJAX (`/api/save_draft`).
  * **Dynamic UI Validation:** Real-time feedback for incorrect entries (e.g., invalid phone lengths, characters).
  * **Conditional Form Bifurcation:** Sections dynamically show/hide based on specific selections (detailed below).
  * **Final Submission Lock:** Once submitted, fields become `readonly` for standard users.

### 2.5 Employee Detail View (`employee_detail.html`)
* **Purpose:** Read-only view of a completed profile.
* **Features:**
  * Displays all provided data in an organized, card-based layout.
  * Admins see an "Edit" button to override standard read-only constraints.

---

## 3. Profile Form: Field Descriptions & Validations

The Profile Completion form is the most complex component, utilizing strict validation both on the frontend (JavaScript/HTML5) and backend (Python).

### 3.1 Basic Information (Always Required)
| Field Name | Type | Description | Validations |
| :--- | :--- | :--- | :--- |
| **Name** | Text | Full name of the employee. | Only letters and spaces (`^[A-Za-z\s]+$`). |
| **Phone** | Text | Primary contact number. | Exactly 10 digits (`^\d{10}$`). |
| **Employee ID** | Text | Unique identifier. | Only digits. Cannot duplicate an existing ID in DB. |
| **Designation** | Text | Job title. | Only letters and spaces. |
| **Department** | Text | Department name. | Only letters and spaces. |
| **Email** | Email | Personal email address. | Standard Email Regex. |
| **Date of Joining** | Date | When they started. | Must be chronologically *after* Date of Birth. |
| **Date of Birth** | Date | Employee's DOB. | **Critical:** Must result in an age of **18 years or older**. |
| **Age** | Text | Auto-calculated age. | `Readonly`. Dynamically calculated from DOB via JS. |
| **Gender** | Select | Male, Female. | Required. |

### 3.2 Marital Status & Form Bifurcation Logic
The **Marital Status** field dynamically dictates the structure of the rest of the form:

* **If "Unmarried":**
  * The **Spouse Section** is entirely hidden and omitted from backend processing.
  * The **Children Section** is entirely hidden.

* **If "Married":**
  * **Spouse Section:** Becomes visible and strictly required. 
    * Fields: *Name (as per Aadhaar)*, *DOB*, *Age (auto-calculated)*, *Gender*.
    * Validation: Spouse Name cannot duplicate another family member's name. Spouse DOB must result in an age **≥ 18 years**.
  * **Children Section:** Becomes visible. Employees can add **up to 2 children**.

* **If "Divorced / Widowed":**
  * **Spouse Section:** Hidden and omitted.
  * **Children Section:** Remains visible, allowing up to 2 children.

### 3.3 Children Section (Dynamic)
* **Visibility:** Only if Married, Divorced, or Widowed.
* **Constraints:** Maximum of 2 children allowed (Add button disables after 2).
* **Fields per Child:** Name, DOB, Age (Auto-calculated), Gender.
* **Validations:** 
  * Names must contain only letters/spaces and cannot duplicate existing family members.
  * DOB is restricted from 1935 up to the current date.

### 3.4 Global Cross-Field Validations (Backend)
1. **Duplicate Family Names:** The system ensures no two family members share the exact same name (case-insensitive) to prevent clerical duplication errors.
2. **Duplicate Phones:** Phone numbers provided for children or spouse cannot duplicate each other.
3. **DOB vs DOJ:** Date of Joining can never precede the Date of Birth.

---

## 4. Technical Workflows

### 4.1 Age Calculation System
Age calculation exists in two places to ensure robustness:
1. **Frontend (`complete_profile.html` JS):** Calculates real-time exact age (e.g., "15 days", "3 months", "32 years") as soon as a user selects a date from the date-picker. It handles leap years and month-rollovers dynamically.
2. **Backend (`utils.py -> calc_age`):** Recalculates and verifies age using `dateutil.relativedelta` upon form submission to prevent tampering.

### 4.2 Data Normalization (`utils.py -> normalize_family`)
When fetching data from MongoDB, the `normalize_family` function organizes the flat `family_members` array back into structured categories (`spouse`, `children`) so the Jinja templates can easily render the distinct sections.

### 4.3 Security & Caching (`app.py`)
To prevent data leaks on shared computers, the application injects strict HTTP Cache-Control headers (`no-store, no-cache, must-revalidate`). If a user logs out and hits the "Back" button, the browser is forced to reload the page, which triggers authentication failure instead of displaying cached profile data. CSRF protection is also strictly enforced across all forms.
