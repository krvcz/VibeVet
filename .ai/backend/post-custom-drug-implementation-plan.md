# API Endpoint Implementation Plan: Create Custom Drug

## 1. Przegląd punktu końcowego
Endpoint POST `/api/custom-drugs` umożliwia utworzenie nowego, specyficznego dla użytkownika leku niestandardowego. Celem jest przyjmowanie danych wejściowych z formularza lub innego klienta i zapisanie ich w bazie danych, zwracając nowo utworzony rekord leku w formacie JSON.

## 2. Szczegóły żądania
- **Metoda HTTP:** POST  
- **Struktura URL:** `/api/custom-drugs`
- **Parametry:**  
  - **Brak parametrów URL i query.**
- **Request Body:**  
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
  - **Wymagane pola:**  
    - `name` (string) – nazwa leku
    - `active_ingredient` (string) – substancja aktywna
    - `species` (number) – identyfikator gatunku (musi być > 0)
    - `measurement_value` (string) – sformatowana wartość numeryczna
    - `measurement_target` (number) – identyfikator jednostki miary
  - **Opcjonalne pole:**  
    - `contraindications` (string) – przeciwwskazania (może być puste lub null)

## 3. Wykorzystywane typy
- **DTO oraz Command Modele:**  
  - `CustomDrugDTO` – reprezentacja zwróconego obiektu leku.
  - `CreateCustomDrugCommand` – struktura danych przesyłanych do endpointa.
- **Serializery:**  
  - `CustomDrugSerializer` (odpowiada za serializację danych wyjściowych)
  - (Ewentualnie dedykowany serializer do walidacji wejścia lub użycie wbudowanej walidacji Django REST Framework)

## 4. Szczegóły odpowiedzi
- **Struktura JSON odpowiedzi:**  
  Po udanym utworzeniu, odpowiedź zawiera pełny obiekt CustomDrug:
  ```json
  {
    "id": 123,
    "name": "CustomDrugA",
    "active_ingredient": "IngredientY",
    "species": 1,
    "contraindications": "None",
    "measurement_value": "5.00000",
    "measurement_target": 1,
    "user_id": 45,
    "createdAt": "2025-04-15T12:00:00Z",
    "updatedAt": "2025-04-15T12:00:00Z",
    "createdBy": 45
  }
  ```
- **Kody statusu:**  
  - **201 Created:** Sukces przy utworzeniu zasobu  
  - **400 Bad Request:** Nieprawidłowe dane wejściowe  
  - **401 Unauthorized:** Brak lub niewłaściwa autoryzacja

## 5. Przepływ danych
1. **Przyjęcie żądania:**  
   Klient wysyła żądanie POST z danymi JSON.
2. **Walidacja wejścia:**  
   Warstwa API (np. widok oparty na Django REST Framework) waliduje dane zgodnie z CreateCustomDrugCommand.
4. **Przekazanie do warstwy serwisowej:**  
   Dane są przekazywane do nowego lub istniejącego serwisu (np. `custom_drug_service.create_custom_drug(data, user)`), który obsługuje logikę biznesową oraz interakcję z bazą.
5. **Operacja na bazie danych:**  
   Używając Django ORM, serwis tworzy rekord w tabeli `CustomDrug`, przypisując dodatkowe pola, takie jak `user_id` i `createdBy`.
6. **Serializacja i odpowiedź:**  
   Utworzony obiekt jest serializowany przy użyciu `CustomDrugSerializer` i zwracany klientowi z kodem 201.

## 6. Względy bezpieczeństwa
- **Walidacja wejścia:**  
  Upewnij się, że wszystkie pola są odpowiednio sprawdzane (np. długość `name`, zakres dla `species`, poprawność formatu `measurement_value`).
- **Ochrona przed atakami:**  
  Stosowanie wbudowanych zabezpieczeń Django (np. ORM, mechanizmy walidacji) redukuje ryzyko SQL Injection.
- **Rejestracja operacji:**  
  Logowanie błędów oraz nieudanych prób walidacji i autoryzacji.

## 7. Obsługa błędów
- **400 Bad Request:**  
  Zwracany, gdy dane wejściowe nie spełniają walidacji, np. brak wymaganych pól lub błędny format.
- **401 Unauthorized:**  
  Zwracany, gdy użytkownik nie jest uwierzytelniony lub nie ma uprawnień.
- **500 Internal Server Error:**  
  Przechwytywanie nieoczekiwanych wyjątków i rejestrowanie ich w systemie logowania (np. poprzez konfigurację logging Django).

## 8. Rozważania dotyczące wydajności
- **Bezpośrednie zapytanie:**  
  Operacja tworzenia pojedynczego rekordu nie powinna stanowić problemu wydajnościowego, jednak należy monitorować obciążenie przy dużej liczbie równoczesnych żądań.
- **Baza danych:**  
  Upewnienie się, że indeksy są obecne na polach używanych w zapytaniach (choć przy operacji INSERT jest to mniejsze ryzyko).
- **Optymalizacja serwisu:**  
  Wykorzystywanie transakcji Django i ewentualnie mechanizmów kolejkowania, jeśli pojawią się długotrwałe operacje po stronie serwera.

## 9. Etapy wdrożenia
1. **Przegląd specyfikacji i przygotowanie konfiguracji:**  
   - Zapoznanie zespołu z wymaganiami endpointu oraz istniejącymi schematami DTO i serializerami.
   - Ustalenie wzorca walidacji danych wejściowych.
2. **Implementacja widoku API:**  
   - Utworzenie nowego widoku lub klasy w Django REST Framework dla endpointu POST `/api/custom-drugs`.
   - Dodanie mechanizmu autoryzacji użytkownika.
3. **Rozwój warstwy serwisowej:**  
   - Implementacja funkcji `create_custom_drug` w module serwisowym (`custom_drug_service`).
   - Integracja z modelem `CustomDrug` przy użyciu Django ORM.
4. **Walidacja danych wejściowych:**  
   - Dodanie logiki walidującej dane zgodnie z `CreateCustomDrugCommand` (użycie serializerów lub dedykowanej walidacji).
5. **Testowanie jednostkowe i integracyjne:**  
   - Opracowanie testów jednostkowych w celu sprawdzenia walidacji danych, poprawności operacji na bazie danych i odpowiedzi API.
6. **Logowanie i monitoring:**  
   - Konfiguracja logowania błędów w Django.
   - Monitorowanie operacji endpointu podczas testów i wdrożenia.
7. **Code Review i wdrożenie:**  
   - Przeprowadzenie code review przez zespół.
   - Wdrożenie na środowisko testowe, a następnie produkcyjne.
