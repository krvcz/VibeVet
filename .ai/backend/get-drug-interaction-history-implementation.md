# API Endpoint Implementation Plan: Get Drug Interaction History

## 1. Przegląd punktu końcowego
Endpoint `/api/drug-interactions` umożliwia pobranie paginowanej listy zapytań o interakcje leków związanych z aktywnością uwierzytelnionego użytkownika. Celem jest umożliwienie użytkownikowi przeglądania historii wcześniejszych zapytań dotyczących interakcji leków.

## 2. Szczegóły żądania
- **Metoda HTTP:** GET
- **Struktura URL:** `/api/drug-interactions`
- **Parametry:**
  - **Opcjonalne:** 
    - `page` (int) – numer strony paginacji (np. domyślnie 1)
    - `limit` (int) – liczba rekordów na stronę (np. domyślnie 20)
- **Request Body:** Brak, operacja GET

## 3. Wykorzystywane typy
- **DTO:**
  - `DrugInteractionDTO` – reprezentacja pojedynczego rekordu historii interakcji.
  - `PaginationDTO` – dane dotyczące paginacji.
  - (Opcjonalnie) `DrugsListResponseDTO` jako wzorzec opakowania wyników.
- **Serializery:**
  - `DrugInteractionSerializer` z `serializers.py` do serializacji danych interakcji.

## 4. Szczegóły odpowiedzi
- **Struktura JSON odpowiedzi:**
  ```json
  {
    "results": [
      {
        "id": 1,
        "query": "Example query",
        "result": "Interaction details",
        "positive_rating": 5,
        "negative_rating": 2,
        "created_at": "2025-04-16T12:00:00Z"
      },
      ...
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100
    }
  }