# API Endpoint Implementation Plan: Custom Drugs

Ten plan wdrożenia obejmuje dwa endpointy:
1. Pobieranie listy wszystkich custom-drugs.
2. Operacje na pojedynczym custom drug (GET, PUT/PATCH, DELETE).

---

## 1. Przegląd punktów końcowych
- **List Custom Drugs:**  
  Endpoint umożliwia pobranie listy wszystkich custom-drugs, zwracając dane dotyczące każdego rekordu.
- **Custom Drug Detail:**  
  Endpoint umożliwia pobranie szczegółów, aktualizację (częściową lub pełną) oraz usunięcie pojedynczego custom drug na podstawie jego identyfikatora. Operacje modyfikacji są zastrzeżone tylko dla właściciela zasobu.

---

## 2. Szczegóły żądania

### 2.1. List Custom Drugs
- **Metoda HTTP:** GET  
- **Struktura URL:** `/api/custom-drugs`  
- **Parametry:**  
  - Ewentualne parametry paginacji lub filtrowania mogą być dodane jako opcjonalne query stringi (np. `page`, `limit`, `search`).

### 2.2. Custom Drug Detail (GET, PUT/PATCH, DELETE)
- **Metody HTTP:**  
  - GET – Pobranie szczegółów custom drug.
  - PUT/PATCH – Aktualizacja pola custom drug (zgodnie z definicją UpdateCustomDrugCommand).
  - DELETE – Usunięcie custom drug.
- **Struktura URL:** `/api/custom-drugs/{id}`  
- **Parametry:**
  - **Path Parameter:**  
    - `id` (wymagany) – unikalny identyfikator custom drug.
- **Request Body (dla PUT/PATCH):**  
  Obiekt zawierający pola do aktualizacji, zgodny z definicją UpdateCustomDrugCommand:
  ```json
  {
    "name": "OptionalNewName",
    "active_ingredient": "OptionalNewIngredient",
    "species": 1,
    "contraindications": "Optional contraindications",
    "measurement_value": "OptionalNewValue",
    "measurement_target": 1
  }
  ```

---

## 3. Wykorzystywane typy
- **DTO:**
  - `CustomDrugDTO` – reprezentuje strukturę custom drug zwracaną w odpowiedzi.
- **Command Model:**
  - `UpdateCustomDrugCommand` – model danych używany przy aktualizacji (wszystkie pola opcjonalne).
- **Serializery:**
  - `CustomDrugSerializer` – do serializacji obiektu custom drug przy odczycie i aktualizacji.
  - Ewentualnie dedykowane serializery do walidacji danych wejściowych dla obu endpointów.

---

## 4. Szczegóły odpowiedzi

### 4.1. List Custom Drugs
- **200 OK:**  
  Zwraca listę obiektów custom drug, np.:
  ```json
  {
    "results": [
      {
        "id": 1,
        "name": "DrugA",
        "active_ingredient": "IngredientX",
        "species": 1,
        "contraindications": "Contraindications info",
        "measurement_value": "10.00000",
        "measurement_target": 1,
        "user_id": 123,
        "createdAt": "2025-04-15T12:00:00Z",
        "updatedAt": "2025-04-15T12:00:00Z",
        "createdBy": 123
      },
      ...
    ]
  }
  ```

### 4.2. Custom Drug Detail
- **GET:**  
  - **200 OK:** Zwraca pełny obiekt custom drug.
  - **404 Not Found:** Gdy custom drug o podanym id nie zostanie odnaleziony.
- **PUT/PATCH:**  
  - **200 OK:** Po pomyślnej aktualizacji zwraca zaktualizowany obiekt.
  - **400 Bad Request:** Dla nieprawidłowych danych wejściowych.
  - **401 Unauthorized:** Gdy użytkownik nie jest właścicielem zasobu.
  - **404 Not Found:** Gdy custom drug nie istnieje.
- **DELETE:**  
  - **204 No Content:** Po pomyślnym usunięciu.
  - **401 Unauthorized:** Gdy użytkownik nie jest właścicielem zasobu.
  - **404 Not Found:** Gdy custom drug nie zostanie odnaleziony.

---

## 5. Przepływ danych

### 5.1. List Custom Drugs
1. Użytkownik wysyła żądanie GET do `/api/custom-drugs` wraz z opcjonalnymi parametrami.
2. Backend pobiera wszystkie rekordy custom drugs z bazy danych przy użyciu Django ORM.
3. Rekordy są serializowane za pomocą `CustomDrugSerializer` i zwracane jako lista.

### 5.2. Custom Drug Detail
1. Użytkownik wysyła żądanie (GET, PUT/PATCH lub DELETE) do `/api/custom-drugs/{id}`.
2. Warstwa uwierzytelniania weryfikuje token użytkownika.
3. Backend pobiera rekord custom drug z bazy danych.
4. Dla operacji PUT/PATCH oraz DELETE – weryfikowany jest identyfikator właściciela zasobu (porównanie `user_id` z identyfikatorem zalogowanego użytkownika).
5. W zależności od metody:
   - **GET:** Serializacja i zwrócenie obiektu.
   - **PUT/PATCH:** Walidacja danych wejściowych, aktualizacja rekordu oraz zwrócenie zaktualizowanego obiektu.
   - **DELETE:** Usunięcie rekordu i zwrócenie statusu 204.

---

## 6. Względy bezpieczeństwa
- **Walidacja danych wejściowych:**  
  - Sprawdzanie poprawności typów, zakresów wartości i długości pól.
  - Użycie serializerów Django REST Framework do walidacji.
- **Ochrona przed atakami:**  
  - Wykorzystanie Django ORM do ochrony przed SQL Injection.
  - Użycie guard clauses dla szybkiej detekcji niewłaściwych danych.

---

## 7. Obsługa błędów
- **400 Bad Request:**  
  - Błędne lub niekompletne dane wejściowe.
- **404 Not Found:**  
  - Zasób o podanym id nie istnieje.
- **500 Internal Server Error:**  
  - Niespodziewane wyjątki; błędy są logowane do systemu monitorowania.

---

## 8. Rozważania dotyczące wydajności
- Operacje na pojedynczych rekordach i listowanie rekordów nie powinny powodować obciążenia.
- Wykorzystanie Django ORM optymalizuje zapytania.
- Rozważenie cache’owania wyników operacji GET przy dużym ruchu.

---

## 9. Etapy wdrożenia

1. **Planowanie i przegląd:**  
   - Przegląd specyfikacji obu endpointów oraz zasad autoryzacji.
   - Omówienie z zespołem istniejących modeli, DTO i serializerów.

2. **Implementacja endpointu List Custom Drugs:**
   - Utworzenie widoku lub endpointu w Django REST Framework dla `/api/custom-drugs`.
   - Implementacja wyszukiwania, paginacji oraz serializacji listy rekordów.

3. **Implementacja endpointu Custom Drug Detail:**
   - Utworzenie widoku (np. ViewSet lub APIView) dla endpointu `/api/custom-drugs/{id}`.
   - Implementacja metod GET, PUT/PATCH oraz DELETE.
   - Integracja autoryzacji – weryfikacja, że tylko właściciel może modyfikować lub usuwać rekord.

4. **Warstwa serwisowa i logika biznesowa:**
   - Wyodrębnienie metod w module/service (np. `custom_drug_service`) do obsługi operacji:
     - `list_custom_drugs()`
     - `get_custom_drug(id)`
     - `update_custom_drug(id, data, user)`
     - `delete_custom_drug(id, user)`
   - Upewnienie się, że walidacja oraz autoryzacja odbywają się w tej warstwie.

5. **Walidacja i obsługa błędów:**
   - Użycie serializerów do walidacji danych wejściowych.
   - Dodanie mechanizmów logowania i guard clauses w celu obsługi błędów.

6. **Testowanie:**
   - Opracowanie testów jednostkowych i integracyjnych dla obu endpointów.
   - Testowanie scenariuszy: prawidłowe działanie, błędy walidacji, brak uprawnień oraz nieistniejące zasoby.

7. **Code Review i wdrożenie:**
   - Przeprowadzenie code review przez zespół.
   - Wdrożenie na środowisko testowe, monitorowanie logów i analiza zachowania systemu.
   - Wdrożenie zmian w produkcji po pozytywnych wynikach testów.

8. **Monitoring i utrzymanie:**
   - Konfiguracja systemów logowania i monitorowania.
   - Monitorowanie wydajności i systematyczna analiza logów dla szybkiej reakcji na błędy.
