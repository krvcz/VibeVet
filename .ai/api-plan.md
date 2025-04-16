# REST API Plan

## 1. Resources
- **Species** (animal species information)
- **MeasurementUnit** (units for drug dosage)
- **Drug** (standard drug details)
- **CustomDrug** (user-specific drug records)
- **DrugInteraction** (drug interaction queries and AI-generated results)
- **TreatmentGuide** (AI-generated treatment guides based on diagnostic factors)
- **UserSearchHistory** (records of user searches and calculations)
- **SystemLog** (system events and logs – read-only for admins)

## 2. Endpoints

### A. Drug Resource
#### 1. Get Drugs List
- **Method:** GET  
- **URL:** `/api/drugs`  
- **Description:** Retrieve a list of standard drugs.  
- **Query Parameters:** 
  - `page` (int, optional)  
  - `limit` (int, optional)  
  - `search` (string, optional for name or active ingredient)
- **Response JSON:**
    ```json
    {
      "results": [
          { "id": 1, "name": "DrugA", "active_ingredient": "IngredientX", "species": 1, "measurement_value": "10.00000", "measurement_target": 1 },
          ...
      ],
      "pagination": { "page": 1, "limit": 20, "total": 100 }
    }
    ```
- **Success Codes:** 200 OK

### B. Custom Drug Resource
Endpoints mirror CRUD operations:
#### 1. Create Custom Drug
- **Method:** POST  
- **URL:** `/api/custom-drugs`  
- **Description:** Create a new user-specific custom drug.  
- **Request JSON:**
    ```json
    {
      "name": "CustomDrugA",
      "active_ingredient": "IngredientY",
      "species": 1,
      "contraindications": "None",
      "measurement_value": "5.00000",
      "measurement_target": 1
    }
    ```
- **Response JSON:** Newly created custom drug object.  
- **Success Codes:** 201 Created  
- **Error Codes:** 400 Bad Request, 401 Unauthorized

#### 2. List, Retrieve, Update, and Delete Custom Drug  
- **Methods:** GET, PUT/PATCH, DELETE  
- **URL Pattern:** `/api/custom-drugs/{id}`  
- **Authorization:** Only the owner of the custom drug may update or delete.

### C. Drug Interaction Resource
#### 1. Create Drug Interaction Query
- **Method:** POST  
- **URL:** `/api/drug-interactions`  
- **Description:** Submit a list of drug IDs and optional context to receive AI-generated interaction details.
- **Request JSON:**
    ```json
    {
      "drug_ids": [1, 3, 5],
      "context": "additional context here (max 50 chars)"
    }
    ```
- **Response JSON:**
    ```json
    {
      "id": 10,
      "query": "DrugA, DrugC, DrugE",
      "result": "AI generated interaction details...",
      "positive_rating": 0,
      "negative_rating": 0,
      "created_at": "2025-04-15T14:30:00Z"
    }
    ```
- **Success Codes:** 201 Created  
- **Error Codes:** 400 Bad Request, 401 Unauthorized

#### 2. Rate Drug Interaction
- **Method:** PATCH  
- **URL:** `/api/drug-interactions/{id}/rate`  
- **Description:** Update the rating (thumbs up/down) for a drug interaction record.  
- **Request JSON:**
    ```json
    {
      "rating": "up"  // or "down"
    }
    ```
- **Response JSON:**
    ```json
    {
      "message": "Rating updated successfully."
    }
    ```
- **Success Codes:** 200 OK

#### 3. Get Drug Interaction History
- **Method:** GET  
- **URL:** `/api/drug-interactions`  
- **Description:** Retrieve a paginated list of drug interaction queries for the authenticated user.
- **Query Parameters:** `page`, `limit`
- **Success Codes:** 200 OK

### E. Dosage Calculator Resource
#### 1. Calculate Dosage
- **Method:** POST  
- **URL:** `/api/dosage-calc`  
- **Description:** Calculate drug dosage based on selected drug, animal weight (up to 3 digits), species, and target measurement unit.
- **Request JSON:**
    ```json
    {
      "drug_id": 1,
      "weight": 45,
      "species": 2,
      "target_unit": 1
    }
    ```
- **Response JSON:**
    ```json
    {
      "drug_id": 1,
      "calculated_dose": "15.00000",
      "unit": "mg"
    }
    ```
- **Performance Requirement:** Response time under 1 second.
- **Success Codes:** 200 OK  
- **Error Codes:** 400 Bad Request, 422 Unprocessable Entity

### F. Treatment Guide Resource
#### 1. Create Treatment Guide Query
- **Method:** POST  
- **URL:** `/api/treatment-guides`  
- **Description:** Submit diagnostic factors to retrieve potential treatment guides via AI.
- **Request JSON:**
    ```json
     {
        "factors": {
          "temperature": 39.5,
          "heart_rate": 110,
          "blood_pressure": "120/80",
          "weight": 25.5,
          "age": 5,
          "species": 1,
          "calcium": "100mg",
          "glucose": "120mg/dL",
          "potassium": "4.2mEq/L",
          "hemoglobin": "15g/dL",
          "platelets": "250000/μL",
          "respiratory_rate": 22,
          "oxygen_saturation": 98,
          "additional_notes": "Patient shows signs of dehydration"
        }
     }
     ```
- **Response JSON:**
    ```json
    {
      "id": 7,
      "result": "Potential conditions: ConditionA, ConditionB...",
      "factors": { "temperature": 39.5, "heart_rate": 110 },
      "positive_rating": 0,
      "negative_rating": 0
    }
    ```
- **Performance Requirement:** AI response time within 10 seconds.
- **Success Codes:** 201 Created  
- **Error Codes:** 400 Bad Request, 401 Unauthorized

#### 2. Rate Treatment Guide
- **Method:** PATCH  
- **URL:** `/api/treatment-guides/{id}/rate`  
- **Description:** Update rating for a treatment guide result.
- **Request JSON:**
    ```json
    {
      "rating": "up" // or "down"
    }
    ```
- **Response JSON:**
    ```json
    {
      "message": "Rating updated successfully."
    }
    ```
- **Success Codes:** 200 OK

### G. User Search History Resource
#### 1. Get Search History
- **Method:** GET  
- **URL:** `/api/search-history`  
- **Description:** Retrieve paginated search history records for the authenticated user (for both drug interactions and dosage/treatment queries).
- **Query Parameters:** `page`, `limit`, `module` (optional filter)
- **Success Codes:** 200 OK

## 3. Authentication and Authorization
- **Authentication Mechanism:**  
  - JSON Web Tokens (JWT) are used for stateless token-based authentication.  
  - Endpoints under `/api/auth/` are public while others require a valid token sent via the `Authorization: Bearer <token>` header.
- **Authorization Rules:**  
  - Users can only access/modify their own records (e.g., CustomDrug, UserSearchHistory).  
  - Admin endpoints (e.g., viewing SystemLogs) are protected by role-based access.

## 4. Validation and Business Logic
- **Field Validations:**  
  - Email format validation and unique constraint.  
  - Password minimum length (8 characters).  
  - Animal weight must be a positive integer (up to 3 digits).  
  - Input lengths for names, context fields, and constraints per DB schema.
- **Business Logic Implementation:**  
  - Dosage Calculator validates the selected drug and units and performs unit conversions.  
  - Drug Interaction and Treatment Guide endpoints interface with Openrouter.ai ensuring maximum response time constraints (10 seconds).  
  - Ratings endpoints update counts while ensuring the request comes from an authorized user.
- **Additional Considerations:**  
  - Pagination, filtering, and sorting support for list endpoints.  
  - Rate limiting and logging (via SystemLog) are integrated as middleware.
  
----

All endpoints and validations are designed in line with the provided DB schema, PRD, and technology stack (Django, PostgreSQL, Openrouter.ai for AI calls, TypeScript/React for the frontend via Astro). This plan ensures a structured REST API that adheres to business logic, performance and security requirements.
