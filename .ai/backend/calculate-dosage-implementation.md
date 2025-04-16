# API Endpoint Implementation Plan: Calculate Dosage

## 1. Przegląd punktu końcowego
Endpoint `/api/dosage-calc` służy do obliczania dawki leku na podstawie przekazanych parametrów, takich jak:
- `drug_id`: identyfikator leku
- `weight`: waga zwierzęcia (do 3 cyfr)
- `species`: identyfikator gatunku
- `target_unit`: identyfikator jednostki miary

Obliczona dawka (jako precyzyjnie sformatowany string) oraz jednostka (np. "mg") zostaną zwrócone klientowi w odpowiedzi JSON.

## 2. Szczegóły żądania
- **Metoda HTTP:** POST  
- **Struktura URL:** `/api/dosage-calc`
- **Parametry (Request Body):**
  - **Wymagane:**
    - `drug_id` (number)
    - `weight` (number, ograniczony do 3 cyfr)
    - `species` (number)
    - `target_unit` (number)
- **Przykładowy Request Body:**
  ```json
  {
    "drug_id": 1,
    "weight": 45,
    "species": 2,
    "target_unit": 1
  }
  ```

## 3. Wykorzystywane typy
- **DTO / Command Model:**
  - `CalculateDosageCommand` (definiowany w pliku `frontend/src/types.ts`)
  - `DosageCalcResultDTO` (definiowany w pliku `frontend/src/types.ts`)
- **Serializery:**
  - `DosageCalcInputSerializer` (odpowiedzialny za walidację danych wejściowych; znajduje się w `backend/core/serializers.py`)
  - `DosageCalcResultSerializer` (do serializacji wyniku, również w `backend/core/serializers.py`)

## 4. Szczegóły odpowiedzi
- **Struktura Response JSON:**
  ```json
  {
    "drug_id": 1,
    "calculated_dose": "15.00000",
    "unit": "mg"
  }
  ```
- **Kody statusu:**
  - **200 OK:** Pomyślne obliczenie dawki.
  - **400 Bad Request:** Nieprawidłowe dane wejściowe.
  - **422 Unprocessable Entity:** Błąd związany z logiką biznesową, np. nieistniejący `drug_id` lub niespełnienie warunków do obliczenia dawki.
  - **500 Internal Server Error:** Nieoczekiwany błąd po stronie serwera.

## 5. Przepływ danych
1. **Przyjęcie żądania:**  
   Klient wysyła żądanie POST do `/api/dosage-calc` z odpowiednim JSON w ciele żądania.
2. **Walidacja:**  
   - Dane wejściowe walidowane są przez `DosageCalcInputSerializer` (sprawdzenie wymagalności pól, zakresy liczbowe m.in. dla `weight`).
   - Opcjonalnie, dodatkowa walidacja istnienia leku w bazie danych.
3. **Logika biznesowa:**  
   - Wyodrębnienie logiki obliczania dawki do dedykowanego serwisu (np. `dosage_calculator_service`), który przyjmuje dane wejściowe, wykonuje obliczenia i zwraca wynik.
4. **Serializacja wyniku:**  
   Wynik obliczeń jest przetwarzany przez `DosageCalcResultSerializer` i zwracany jako JSON.
5. **Odpowiedź:**  
   Zwracany jest JSON zawierający `drug_id`, `calculated_dose` oraz `unit` z odpowiednim kodem statusu.

## 6. Względy bezpieczeństwa
- **Walidacja danych wejściowych:**  
  Konieczne jest rygorystyczne sprawdzenie poprawności danych przy użyciu serializerów, aby zapobiec przesłaniu złośliwych lub niepoprawnych danych.
- **Bezpieczne operacje na bazie danych:**  
  Wykorzystanie Django ORM ogranicza ryzyko SQL Injection.
- **Rate Limiting:**  
  Ewentualne wdrożenie limitera zapytań, aby chronić endpoint przed przeciążeniem.
- **Autoryzacja:**  
  Sprawdzenie, czy dostęp do endpointu mają autoryzowani użytkownicy, jeśli wymaga tego logika aplikacji.

## 7. Obsługa błędów
- **400 Bad Request:**  
  Zwracany, gdy dane wejściowe nie przejdą walidacji (np. brak wymaganych pól lub niepoprawny format danych).
- **422 Unprocessable Entity:**  
  Używany do sygnalizacji błędów logiki biznesowej, takich jak nieistniejący `drug_id`.
- **500 Internal Server Error:**  
  Dla nieoczekiwanych błędów po stronie serwera; wszystkie wyjątki należy logować przy użyciu systemu logowania Django.

## 8. Rozważania dotyczące wydajności
- **Wymaganie:** Czas odpowiedzi poniżej 1 sekundy.
- Optymalizacja zapytań do bazy danych, np. szybkie sprawdzenie istnienia leku.
- Minimalizacja logiki obliczeniowej w ścieżce krytycznej.
- Rozważenie implementacji mechanizmu cache, jeżeli obciążenie będzie bardzo duże.

## 9. Etapy wdrożenia
1. **Analiza i przygotowanie:**
   - Przegląd specyfikacji endpointu.
   - Ustalenie wymagań walidacji i domyślnych wartości.
2. **Implementacja walidacji:**
   - Użycie `DosageCalcInputSerializer` do sprawdzania poprawności danych wejściowych.
   - Implementacja dodatkowych reguł walidacji (np. zakres wagi, istnienie leku).
3. **Implementacja logiki biznesowej:**
   - Utworzenie serwisu `dosage_calculator_service` w logice backendu.
   - Implementacja algorytmu obliczania dawki.
4. **Integracja z Django ORM:**
   - Sprawdzenie istnienia leku i innych powiązanych rekordów w bazie.
5. **Serializacja i zwrócenie odpowiedzi:**
   - Korzystanie z `DosageCalcResultSerializer` do przygotowania odpowiedzi.
   - Zwrócenie odpowiedzi z kodem 200 OK w przypadku powodzenia.
6. **Testowanie:**
   - Testy jednostkowe walidacji danych wejściowych.
   - Testy integracyjne endpointu (poprawne i niepoprawne żądania).
   - Testy wydajnościowe, aby zapewnić czas odpowiedzi poniżej 1 sekundy.
7. **Logowanie i monitoring:**
   - Konfiguracja systemu logowania Django do rejestrowania błędów.
   - Monitorowanie endpointu przy użyciu narzędzi APM.
8. **Code Review i wdrożenie:**
   - Przeprowadzenie code review przez zespół.
   - Wdrożenie na środowisko testowe, a następnie produkcyjne.