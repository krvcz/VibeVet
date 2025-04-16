# API Endpoint Implementation Plan: Create Treatment Guide Query

## 1. Przegląd punktu końcowego
Endpoint umożliwia przesłanie czynników diagnostycznych w celu uzyskania potencjalnych wskazówek terapeutycznych generowanych przez system AI. Zapytanie powinno zwrócić identyfikator, wynik zapytania, podsumowanie przekazanych czynników oraz początkowe oceny (0 dla pozytywnych i negatywnych).

## 2. Szczegóły żądania
- **Metoda HTTP:** POST  
- **Struktura URL:** `/api/treatment-guides`  
- **Parametry:**  
  - **Wymagane:**  
    - `factors`: Obiekt zawierający różne właściwości:
    np:
      - `temperature`
      - `heart_rate`
      - `blood_pressure`
      - `weight`
      - `age`
      - `calcium`
      - `glucose`
      - `potassium`
      - `hemoglobin`
      - `platelets`
      - `respiratory_rate`
      - `oxygen_saturation`
      - `additional_notes`
      Użytkownik może przekazać dowolny czynnnik.

- **Request Body Example:**
  ```json
  {
    "factors": {
      "temperature": "39.5",
      "heart_rate": "110",
      "blood_pressure": "120/80",
      "weight": "25.5kg",
      "age": "5 year",
      "calcium": "100mg",
      "glucose": "120mg/dL",
      "potassium": "4.2mEq/L",
      "hemoglobin": "15g/dL",
      "platelets": "250000/μL",
      "respiratory_rate": "22",
      "oxygen_saturation": "98",
      "additional_notes": "Patient shows signs of dehydration"
    }
  }
  ```

## 3. Wykorzystywane typy
- **DTO/Command Model:**  
  - `CreateTreatmentGuideCommand` (zdefiniowany w `frontend/src/types.ts`)

- **Serializery:**  
  - `CreateTreatmentGuideSerializer` – do walidacji danych wejściowych.  
  - `TreatmentGuideSerializer` – do serializacji danych odpowiedzi.

## 4. Szczegóły odpowiedzi
- **Response JSON Example:**
  ```json
  {
    "id": 7,
    "result": "Potential conditions: ConditionA, ConditionB...",
    "factors": { "temperature": 39.5, "heart_rate": 110 },
    "positive_rating": 0,
    "negative_rating": 0
  }
  ```
- **Kody statusu:**
  - **201 Created:** Zasób został pomyślnie utworzony.
  - **400 Bad Request:** Dane wejściowe są niepoprawne.
  - **401 Unauthorized:** Brak odpowiednich danych uwierzytelniających.
  - **500 Internal Server Error:** Wystąpił nieoczekiwany błąd po stronie serwera.

## 5. Przepływ danych
1. **Przyjęcie żądania:**  
   - Klient wysyła żądanie POST do `/api/treatment-guides` z obiektem `factors` w ciele żądania.
2. **Walidacja:**  
   - Dane wejściowe są weryfikowane przez `CreateTreatmentGuideSerializer`.
   - Walidacja obejmuje sprawdzenie obecności wymaganych pól oraz ich typów.
3. **Logika biznesowa:**  
   - Po udanej walidacji, dane są przekazywane do serwisu (np. `treatment_guide_service`), który odpowiada za komunikację z systemem AI, przetwarzanie zapytania oraz zapis wyników w bazie danych.
4. **Serializacja wyniku:**  
   - Wynik zwracany przez serwis jest serializowany przy użyciu `TreatmentGuideSerializer`.
5. **Odpowiedź:**  
   - Zwracany jest JSON zawierający szczegóły zapytania i odpowiedź systemu AI z kodem 201 Created.

## 6. Względy bezpieczeństwa
- **Autoryzacja:**  
  - Upewnić się, że dostęp do endpointu jest ograniczony do autoryzowanych użytkowników (401 Unauthorized w przypadku braku autoryzacji).
- **Walidacja:**  
  - Szczegółowa walidacja danych wejściowych minimalizuje ryzyko ataków (np. przesłanie złośliwych danych).
- **Logowanie/Błędy:**  
  - Wszelkie błędy (np. z usługi AI) powinny być logowane przy użyciu systemu logowania Django.

## 7. Rozważania dotyczące wydajności
- **Responsywność:**  
  - System AI powinien generować odpowiedź w czasie poniżej 10 sekund.
- **Optymalizacja:**  
  - Minimalizacja narzutu obliczeniowego w ścieżce krytycznej, w tym asynchronicznego przetwarzania zapytań.
- **Skalowalność:**  
  - Rozważenie mechanizmu cache dla powtarzających się zapytań oraz wykorzystywanie kolejek do obsługi zapytań długotrwałych.

## 8. Etapy wdrożenia
1. **Analiza i przygotowanie:**  
   - Przejrzenie specyfikacji endpointu i ustalenie wymagań walidacji.
   - Identyfikacja niezbędnych modeli, DTOs oraz serializerów.

2. **Implementacja walidacji wejściowej:**  
   - Utworzenie lub modyfikacja `CreateTreatmentGuideSerializer` do walidacji struktury obiektu `factors`.
   - Testowanie walidacji przez wprowadzanie poprawnych i niepoprawnych danych.

3. **Wyodrębnienie logiki biznesowej:**  
   - Utworzenie serwisu `treatment_guide_service` odpowiedzialnego za:  
     - Komunikację z systemem AI
     - Przetwarzanie danych diagnostycznych
     - Zapis wyników w bazie danych

4. **Integracja z bazą danych:**  
   - Potwierdzenie, że model `TreatmentGuide` odpowiada definicji schematu w bazie danych.
   - Implementacja zapisu danych (np. ustawienie domyślnych wartości dla oceny).

5. **Implementacja mechanizmu odpowiedzi:**  
   - Serializacja wyniku przy użyciu `TreatmentGuideSerializer`.
   - Testowanie poprawności odpowiedzi JSON, w tym przekazywanych danych diagnostycznych.

6. **Implementacja logowania i monitoringu:**  
   - Konfiguracja systemu logowania Django aby rejestrować błędy i wyjątki.
   - Ustawienie monitoringu kluczowych operacji, szczególnie zapytań do systemu AI.

7. **Testowanie:**  
   - Przeprowadzenie testów jednostkowych na serializerach i logice serwisowej.
   - Testy integracyjne endpointu (poprawne przepływy, błędne dane wejściowe, autoryzacja).
   - Testy wydajnościowe, aby upewnić się, że czas odpowiedzi AI nie przekracza 10 sekund.

8. **Code Review oraz wdrożenie:**  
   - Przeprowadzenie code review przez zespół.
   - Wdrożenie na środowisko testowe, a następnie produkcyjne.