# API Endpoint Implementation Plan: Rate Treatment Guide

## 1. Przegląd punktu końcowego
Endpoint służy do aktualizacji oceny wyniku przewodnika leczenia. Użytkownik przesyła wartość "up" lub "down", co skutkuje inkrementacją pola positiveRating lub negativeRating w rekordzie TreatmentGuide. Celem jest umożliwienie użytkownikom szybkiej oceny jakości wygenerowanego wyniku.

## 2. Szczegóły żądania
- **Metoda HTTP:** PATCH
- **Struktura URL:** `/api/treatment-guides/{id}/rate`
- **Parametry:**
  - **Path Parameter:**  
    - `id` (wymagany) – unikalny identyfikator rekordu przewodnika leczenia.
  - **Request Body:**
    ```json
    {
      "rating": "up" // lub "down"
    }
    ```
- **Walidacja wejścia:**  
  - Użycie serializer’a `RateTreatmentGuideSerializer` do potwierdzenia, że pole `rating` przyjmuje wartość "up" lub "down".

## 3. Wykorzystywane typy
- **DTO / Command Model:**  
  - `RateTreatmentGuideCommand` (analogiczny do modelu RateDrugInteractionCommand, ale dla treatment guides)
- **Serializery:**  
  - `RateTreatmentGuideSerializer` (zgodny z definicją w pliku serializers.py)

## 4. Szczegóły odpowiedzi
- **200 OK:**  
  ```json
  {
    "message": "Rating updated successfully."
  }
  ```
- **Kody błędów:**  
  - **400 Bad Request:** nieprawidłowe dane wejściowe lub błędna wartość `rating`
  - **404 Not Found:** rekord o podanym `id` nie istnieje
  - **500 Internal Server Error:** nieoczekiwany błąd serwera

## 5. Przepływ danych
1. Klient wysyła żądanie PATCH do `/api/treatment-guides/{id}/rate` z wartością `rating` w ciele.
2. Endpoint pobiera `id` z URL oraz waliduje dane wejściowe przy użyciu `RateTreatmentGuideSerializer`.
3. Wywoływana jest logika biznesowa w warstwie serwisowej (np. funkcja `rate_treatment_guide` w module `treatment_guide_service`), która:
   - Weryfikuje istnienie rekordu TreatmentGuide wg `id`.
   - Na podstawie wartości `rating` – "up" lub "down" – inkrementuje odpowiednio pole positiveRating lub negativeRating.
   - Zapisuje zmiany w bazie danych.
4. W przypadku sukcesu zwracana jest odpowiedź z kodem 200 OK i komunikatem potwierdzającym.

## 6. Względy bezpieczeństwa
- **Autoryzacja:**  
  - Upewnić się, że użytkownik ma odpowiednie uprawnienia do modyfikacji rekordu (np. sprawdzenie uwierzytelnienia oraz autoryzacji).
- **Walidacja wejścia:**  
  - Serwer przeprowadza walidację danych przy użyciu serializerów, aby uniknąć nieprawidłowych lub złośliwych danych.
- **Ograniczenie nadużyć:**  
  - Rozważyć implementację mechanizmu rate limiting w celu ochrony endpointu przed nadużyciami typu brute force.

## 7. Obsługa błędów
- **400 Bad Request:**  
  - Zwracany w przypadku błędnej struktury żądania lub nieprawidłowej wartości `rating`.
- **404 Not Found:**  
  - Zwracany, gdy rekord TreatmentGuide o podanym `id` nie istnieje.
- **500 Internal Server Error:**  
  - Zwracany przy wystąpieniu nieoczekiwanych błędów. Szczegóły błędów powinny być logowane w systemie monitorowania błędów.

## 8. Rozważania dotyczące wydajności
- Operacja aktualizacji dotyczy pojedynczego rekordu – zatem obciążenie bazy danych powinno być minimalne.
- Kolumna `id` jest indeksowana, co umożliwia szybkie wyszukiwanie rekordu.
- Utrzymanie optymalizacji logiki aktualizacji oraz mechanizmów cache (jeżeli są wdrożone) w celu zmniejszenia opóźnień.

## 9. Etapy wdrożenia
1. **Analiza i przygotowanie:**  
   - Przegląd specyfikacji endpointu, istniejących modeli, serializerów i logiki biznesowej.
2. **Implementacja walidacji:**  
   - Utworzenie i wdrożenie `RateTreatmentGuideSerializer` zgodnie ze specyfikacją.
3. **Rozszerzenie logiki serwisowej:**  
   - Implementacja funkcji `rate_treatment_guide(id: int, rating: str)` w module `treatment_guide_service`:
     - Pobranie rekordu TreatmentGuide.
     - Weryfikacja istnienia rekordu.
     - Aktualizacja pola positiveRating lub negativeRating.
     - Zapis zmian do bazy danych.
4. **Integracja z endpointem:**  
   - Utworzenie widoku API (np. oparty na Django REST Framework, używając APIView lub ViewSet) obsługującego metodę PATCH dla ścieżki `/api/treatment-guides/{id}/rate`.
5. **Obsługa błędów i logowanie:**  
   - Implementacja mechanizmu obsługi wyjątków oraz logowania błędów.
6. **Testowanie:**  
   - Opracowanie testów jednostkowych i integracyjnych dla walidacji oraz logiki serwisowej.
7. **Code Review i wdrożenie:**  
   - Przeprowadzenie przeglądu kodu przez zespół, wdrożenie na środowisko testowe i monitorowanie działania endpointu.
8. **Monitorowanie i utrzymanie:**  
   - Konfiguracja systemu logowania i monitorowania błędów, aby szybko reagować na problemy produkcyjne.