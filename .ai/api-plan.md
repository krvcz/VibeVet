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
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
          { "id": 1,
           "name": "DrugA",
            "active_ingredient": "IngredientX",
             "species": {
                          "id": 1,
                           "name": "Dog",
                            "description": "Domestic dog - man's best friend"},
                             "contraindications": "Penicillin allergy", "measurement_value": "10.00000", 
           "measurement_unit": { 
                                "id": 1,
                                "name": "Milligram",
                                "short_name": "mg"
                              } ,
           "per_weight_value": "1.00000",
           "per_weight_unit": {
                              "id": 3,
                              "name": "Kilogram",
                              "short_name": "kg"
                              }
        },
          ...
      ],
    }
    ```
- **Success Codes:** 200 OK
- **Error Codes:** 404 Not Found, 401 Unauthorized

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
      "measurement_unit": 1,
      "per_weight_value": "1.00000",
      "per_weight_unit": 1
    }
    ```
- **Response JSON:**
  ```json
    {
    "id": 5,
    "name": "CustomDrugA",
    "active_ingredient": "IngredientY",
    "species": 1,
    "contraindications": "None",
    "measurement_value": "5.00000",
    "measurement_unit": 1,
    "per_weight_value": "1.00000",
    "per_weight_unit": 1
  }
  ```
- **Success Codes:** 201 Created  
- **Error Codes:** 400 Bad Request, 401 Unauthorized


#### 2. List Custom Drug
- **Method:** GET  
- **URL:** `/api/custom-drugs`  
- **Description:** Retrieve a list of standard drugs.
- **Query Parameters:** 
  - `page` (int, optional)  
  - `limit` (int, optional)  
  - `search` (string, optional for name or active ingredient)
- **Response JSON:**
    ```json
    {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
          { 
            "id": 5,
             "name": "CustomDrugA",
              "active_ingredient": "IngredientY",
              "species": {
                            "id": 1,
                             "name": "Dog",
                            "description": "Domestic dog - man's best friend"
                          },
              "contraindications": "None",
              "measurement_value": "10.00000",
              "measurement_unit": { 
                                    "id": 1,
                                    "name": "Milligram",
                                    "short_name": "mg"
                                  } ,
              "per_weight_value": "1.00000",
              "per_weight_unit": {
                              "id": 3,
                              "name": "Kilogram",
                              "short_name": "kg"
                              }                  
        },
          ...
      ]
    }
    ```
- **Success Codes:** 200 OK
- **Error Codes:** 404 Not Found, 401 Unauthorized

#### 3. Get Custom Drug
- **Method:** GET  
- **URL:** `/api/custom-drugs/{id}`  
- **Description:** Get custom drug by its pk.
- **Path Parameters:** 
  - `id` (int)  
- **Request:**
    ```http
    /api/custom-drugs/4
    ```
- **Response JSON:**
    ```json
      { 
        "id": 4,
        "name": "CustomDrugA",
        "active_ingredient": "IngredientY",
        "species": {
                      "id": 1,
                       "name": "Dog", 
                       "description": "Domestic dog - man's best friend"
                    },
        "contraindications": "None",
        "measurement_value": "10.00000",
        "measurement_unit": { 
                              "id": 1,
                              "name": "Milligram",
                              "short_name": "mg"
                            },
        "per_weight_value": "1.00000",
        "per_weight_unit": {
                              "id": 3,
                              "name": "Kilogram",
                              "short_name": "kg"
                              }
        }
    ```
- **Success Codes:** 200 OK
- **Error Codes:** 404 Not Found, 401 Unauthorized

#### 4. Update Custom Drug
- **Method:** PUT/PATCH 
- **URL:** `/api/custom-drugs/{id}`  
- **Description:** Update custom drug by its pk.
- **Path Parameters:** 
  - `id` (int)  
- **Request:**
    ```http
    /api/custom-drugs/4
    ```
- **Response JSON:**
    ```json
      { "id": 4, "name": "CustomDrugA",
        "active_ingredient": "IngredientY",
        "species": 1,
        "contraindications": "None",
        "measurement_value": "10.00000",
        "measurement_unit": 1,
        "per_weight_value": "1.00000",
        "per_weight_unit": 1
        }
    ```
- **Success Codes:** 200 OK
- **Error Codes:** 404 Not Found, 401 Unauthorized

#### 5. Update Custom Drug
- **Method:** DELETE
- **URL:** `/api/custom-drugs/{id}`  
- **Description:** Delete custom drug by its pk.
- **Path Parameters:** 
  - `id` (int)  
- **Request:**
    ```http
    /api/custom-drugs/4
  ```
- **Success Codes:** 204 OK
- **Error Codes:** 404 Not Found, 401 Unauthorized

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
      "id": 28,
      "query": "Metacam, Phenylbutazone, Rimadyl",
      "result": "Mock interaction analysis for: Metacam, Phenylbutazone, Rimadyl Context: 123"
    }
    ```
- **Success Codes:** 201 Created, 200 OK
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
- **Error Codes:** 400 Bad Request, 401 Unauthorized, 404 NotFound

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
      "factors": { "temperature": 39.5, "heart_rate": 110 }
    }
    ```
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
- **Error Codes:** 400 Bad Request, 401 Unauthorized

### G. User Search History Resource
#### 1. Get Search History
- **Method:** GET  
- **URL:** `/api/search-history`  
- **Description:** Retrieve paginated search history records for the authenticated user (for both drug interactions and dosage/treatment queries).
- **Query Parameters:** `page`, `limit`, `module`, `from_date`, `to_date`
- **Request:**
    ```http
    /api/search-history/
    ```
- **Response JSON:**
    ```json
      {
    "count": 1,
    "next": "http://localhost:8000/api/search-history/?limit=1&page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "module": "drug-interaction",
            "query": "Drug interaction query for drug IDs: [1, 2]",
            "timestamp": "2025-04-28T08:13:47.767484Z"
        }
    ]
}
    ```
- **Success Codes:** 200 OK
- **Error Codes:** 400 Bad Request, 401 Unauthorized


### G. Common Resource
#### 1. Get Species
- **Method:** GET  
- **URL:** `/api/species`  
- **Description:** Retrieve paginated species for the authenticated user.

- **Request:**
    ```http
    /api/species/
    ```
- **Response JSON:**
    ```json
      {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Cat",
            "description": "Domestic cat species"
        },
        {
            "id": 1,
            "name": "Dog",
            "description": "Domestic dog species"
        }
    ]
}
    ```
- **Success Codes:** 200 OK
- **Error Codes:** 400 Bad Request, 401 Unauthorized


#### 2. Get Units
- **Method:** GET  
- **URL:** `/api/units`  
- **Description:** Retrieve paginated units for the authenticated user.

- **Request:**
    ```http
    /api/units/
    ```
- **Response JSON:**
    ```json
   {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Kilogram",
            "short_name": "kg"
        },
        {
            "id": 1,
            "name": "Milligram",
            "short_name": "mg"
        }
    ]
}
    ```
- **Success Codes:** 200 OK
- **Error Codes:** 400 Bad Request, 401 Unauthorized
----

All endpoints and validations are designed in line with the provided DB schema, PRD, and technology stack (Django, PostgreSQL, Openrouter.ai for AI calls, TypeScript/React for the frontend via Astro). This plan ensures a structured REST API that adheres to business logic, performance and security requirements.
