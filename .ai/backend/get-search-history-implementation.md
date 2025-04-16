# API Endpoint Implementation Plan: Get Search History

## 1. Przegląd punktu końcowego
Endpoint umożliwia pobranie paginowanej historii wyszukiwań użytkownika. Użytkownik musi być uwierzytelniony, a historia może być filtrowana opcjonalnie po module (np. "drug-interaction", "dosage-calc", "treatment-guide").

## 2. Szczegóły żądania
- **Metoda HTTP:** GET  
- **Struktura URL:** `/api/search-history`  
- **Parametry:**
  - **Wymagane:**  
    - `page` – numer strony (np. `1`)
    - `limit` – liczba rekordów zwracanych na stronę (np. `10`)
  - **Opcjonalne:**  
    - `module` – filtr wyników według modułu (np. `"drug-interaction"`)
- **Request Body:** Brak (parametry przesyłane jako query parameters)

## 3. Wykorzystywane typy
- **DTO:**
  - `SearchHistoryRecordDTO`
  - `PaginationDTO`
  - `SearchHistoryResponseDTO`
- **Serializery:**  
  - `UserSearchHistorySerializer`

## 4. Szczegóły odpowiedzi
- **Kod sukcesu:** 200 OK
- **Struktura odpowiedzi JSON:**  
  ```json
  {
    "results": [
      {
        "id": 1,
        "module": "drug-interaction",
        "query": "example query",
        "timestamp": "2025-04-15T14:30:00Z"
      },
      ...
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 50
    }
  }