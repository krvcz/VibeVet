# API Endpoint Implementation Plan: Create Drug Interaction Query

## 1. Przegląd punktu końcowego
Endpoint umożliwia przesłanie listy identyfikatorów leków oraz opcjonalnego kontekstu celem uzyskania szczegółowych danych o interakcjach leków generowanych przez AI. Operacja ta powinna utworzyć rekord interakcji w bazie danych oraz zwrócić dane o utworzonym rekordzie.

## 2. Szczegóły żądania
- **Metoda HTTP:** POST  
- **Struktura URL:** `/api/drug-interactions`
- **Parametry:**
  - **Wymagane:**  
    - `drug_ids` (array liczb) – lista identyfikatorów leków.
  - **Opcjonalne:**  
    - `context` (string, max 50 znaków) – dodatkowy kontekst dla zapytania.
- **Request Body:**
  ```json
  {
    "drug_ids": [1, 3, 5],
    "context": "additional context here (max 50 chars)"
  }
  ```

## 3. Wykorzystywane typy
- **DTO:** 
  - `DrugInteractionDTO`
- **Command Model:**
  - `CreateDrugInteractionCommand`
- **Serializery:**
  - `CreateDrugInteractionSerializer` – walidacja danych wejściowych.
  - `DrugInteractionSerializer` – serializacja danych wyjściowych.

## 4. Szczegóły odpowiedzi
- **Kod sukcesu:** 201 Created  
- **Struktura odpowiedzi JSON:**
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
- **Kody błędów:**
  - 400 Bad Request – dla nieprawidłowych danych wejściowych.

## 5. Przepływ danych
1. Klient wysyła żądanie POST z danymi JSON.
2. API waliduje dane wejściowe przy użyciu `CreateDrugInteractionSerializer`.
3. Po pozytywnej walidacji, dane są przekazywane do warstwy serwisowej (np. `drug_interaction_service.create_interaction`).
4. Warstwa serwisowa:
   - Przetwarza dane, buduje zapytanie (np. scalając nazwy leków).
   - Wywołuje model AI (Openrouter.ai) w celu wygenerowania wyników interakcji. Na czas MVP ta funkcjoinalność powinna zostać zamockowanna
   - Zapisuje rekord interakcji z domyślnymi wartościami ocen (0 dla obu).
5. Wynik zostaje zserializowany przy użyciu `DrugInteractionSerializer` i zwrócony klientowi.

## 6. Względy bezpieczeństwa
- **Walidacja danych:** Użycie serializerów Django REST Framework zapewni sprawdzenie typu, zakresu oraz długości pól.
- **Ochrona przed atakami:** Django ORM oraz stosowanie mechanizmów walidacji chronią przed atakami SQL Injection.

## 7. Obsługa błędów
- **400 Bad Request:** Zwracany, gdy dane wejściowe są nieprawidłowe (np. błędny format listy "drug_ids" lub przekroczenie limitu znaków w "context").
- **401 Unauthorized:** Zwracany, gdy użytkownik nie jest uwierzytelniony lub nie posiada odpowiednich uprawnień.
- **500 Internal Server Error:** Dla nieoczekiwanych błędów serwera; błędy powinny być logowane przy użyciu systemu Django logging.

## 8. Rozważania dotyczące wydajności
- **Paginacja i optymalizacja:** Operacja jest wykonywana na pojedynczym rekordzie, nie wymaga paginacji – główne obciążenie pochodzi z wywołania usługi AI.  
- **Cache:** Możliwość wdrożenia cache'owania wyników zapytań AI, jeśli podobne zapytania występują często.
- **Asynchroniczność:** Można rozważyć asynchroniczne przetwarzanie długotrwałych operacji w warstwie serwisowej, aby nie blokować żądania API.

## 9. Etapy wdrożenia
1. **Analiza i przygotowanie:**
   - Przegląd specyfikacji endpointu oraz ustalenie struktury danych.
   - Przegląd istniejących typów DTO i serializerów w projekcie.

2. **Implementacja walidacji wejścia:**
   - Utworzenie lub modyfikacja `CreateDrugInteractionSerializer` dla walidacji "drug_ids" oraz "context".

3. **Zaimplementowanie warstwy logiki biznesowej:**
   - Utworzenie modułu/service (np. `drug_interaction_service`) do obsługi logiki generowania interakcji.
   - Implementacja funkcji, która komunikuje się z Openrouter.ai, buduje zapytanie oraz zapisuje rekord w bazie danych.

4. **Integracja z modelem i serializacją:**
   - Użycie Django ORM do zapisu nowego rekordu w tabeli `DrugInteractions` oraz powiązanej tabeli `DrugInteractions_Drugs`.
   - Serializacja wyniku przy użyciu `DrugInteractionSerializer`.

5. **Testowanie:**
   - Opracowanie testów jednostkowych dla walidacji danych wejściowych.
   - Testy integracyjne symulujące poprawne oraz niepoprawne żądania.
   - Sprawdzenie logiki wywołania usługi AI (możliwe mockowanie odpowiedzi).

6. **Implementacja obsługi błędów:**
   - Dodanie mechanizmów logowania wyjątków.
   - Przygotowanie komunikatów błędów oraz ustawienie właściwych kodów statusu (400, 401, 500).

7. **Code Review i wdrożenie:**
   - Przeprowadzenie code review przez zespół.
   - Wdrożenie na środowisko testowe, monitorowanie logów i analiza zachowania endpointu.

8. **Monitorowanie i utrzymanie:**
   - Konfiguracja narzędzi monitorujących (np. Django logging, Sentry).
   - Utrzymanie endpointu i optymalizacje w razie zwiększonego obciążenia.