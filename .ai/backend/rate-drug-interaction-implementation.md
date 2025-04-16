# API Endpoint Implementation Plan: Rate Drug Interaction

## 1. Przegląd punktu końcowego
Endpoint służy do aktualizacji oceny interakcji leku. Użytkownik przekazuje wartość "up" lub "down", co powoduje inkrementację odpowiednio pola positiveRating lub negativeRating w rekordzie interakcji.

## 2. Szczegóły żądania
- **Metoda HTTP:** PATCH  
- **Struktura URL:** `/api/drug-interactions/{id}/rate`  
- **Parametry:**
  - **Path Parameter:**  
    - `id` (wymagany) – unikalny identyfikator rekordu interakcji.
  - **Request Body:**
    ```json
    {
      "rating": "up"  // lub "down"
    }
    ```
- **Walidacja wejścia:**  
  - Użycie serializer’a `RateDrugInteractionSerializer` do weryfikacji, że pole "rating" przyjmuje wartość "up" lub "down".

## 3. Wykorzystywane typy
- **DTO/Command Model:**  
  - RateDrugInteractionCommand (zgodny z oczekiwanym schematem walidacji)
- **Serializery:**  
  - `RateDrugInteractionSerializer` (odpowiadający specyfikacji w pliku serializers.py)

## 4. Szczegóły odpowiedzi
- **200 OK:**  
  ```json
  {
    "message": "Rating updated successfully."
  }
  ```
- **Błędy:**
  - **400 Bad Request:** – gdy JSON lub wartość "rating" nie spełniają wymagań walidacji.
  - **404 Not Found:** – gdy rekord interakcji o podanym `id` nie istnieje.
  - **500 Internal Server Error:** – przy nieoczekiwanych błędach serwera.

## 5. Przepływ danych
1. Klient wysyła żądanie PATCH do `/api/drug-interactions/{id}/rate` z wartością "rating" w ciele.
2. Endpoint pobiera parametr `id` ze ścieżki i waliduje dane wejściowe przy użyciu `RateDrugInteractionSerializer`.
3. Warstwa serwisowa (np. funkcja `rate_interaction` w module `drug_interaction_service`) wykonuje:
   - Weryfikację istnienia rekordu interakcji na podstawie `id`.
   - Aktualizację wartości:
     - Jeśli "rating" to "up": inkrementacja pola `positiveRating`.
     - Jeśli "rating" to "down": inkrementacja pola `negativeRating`.
   - Zapis zmodyfikowanego rekordu w bazie danych.
4. W przypadku sukcesu zwracana jest odpowiedź z komunikatem potwierdzającym operację.

## 6. Względy bezpieczeństwa
- **Autoryzacja:**  
  - Sprawdzenie, czy użytkownik posiada uprawnienia do modyfikacji danego rekordu (np. weryfikacja właściciela lub odpowiednich ról).
- **Walidacja wejścia:**  
  - Użycie serializerów Django REST Framework gwarantujących, że dane wejściowe są poprawne.
- **Ograniczenie nadużyć:**  
  - Wdrożenie mechanizmu rate limiting, by zabezpieczyć endpoint przed atakami typu brute force.

## 7. Obsługa błędów
- **400 Bad Request:**  
  - Zwracane gdy dane wejściowe są nieprawidłowe.
- **404 Not Found:**  
  - Zwracane gdy rekord interakcji o podanym `id` nie istnieje.
- **500 Internal Server Error:**  
  - Zwracane przy nieoczekiwanych błędach, z jednoczesnym logowaniem szczegółowych informacji o błędzie w systemie Django.

## 8. Rozważania dotyczące wydajności
- **Baza danych:**  
  - Operacja aktualizacji dotyczy pojedynczego rekordu, więc obciążenie bazy danych jest minimalne.
- **Indeksacja:**  
  - Kolumna `id` jest indeksowana, co umożliwia szybkie wyszukiwanie rekordu.
- **Cache:**  
  - Aktualizacja danych (operacja zapisu) nie korzysta z mechanizmów cache, ale monitorowanie obciążenia jest zalecane.

## 9. Etapy wdrożenia
1. **Analiza i przygotowanie:**  
   - Przegląd specyfikacji endpointu, istniejących modeli, serializerów i modułu logiki biznesowej.
2. **Implementacja walidacji:**  
   - Wdrożenie walidatora przy użyciu `RateDrugInteractionSerializer`.
3. **Implementacja logiki serwisowej:**  
   - Utworzenie lub rozszerzenie modułu `drug_interaction_service` o funkcję `rate_interaction(id, rating)`:
     - Pobranie rekordu interakcji.
     - Weryfikacja istnienia rekordu.
     - Aktualizacja pola `positiveRating` lub `negativeRating` w zależności od wartości "rating".
     - Zapis zmienionego rekordu.
4. **Integracja z endpointem:**  
   - Utworzenie dedykowanego widoku API (np. APIView lub ViewSet) obsługującego metodę PATCH dla URL `/api/drug-interactions/{id}/rate`.
5. **Obsługa błędów i logowanie:**  
   - Zapewnienie odpowiedniej obsługi wyjątków, logowanie błędów i zwracanie właściwych kodów odpowiedzi.
6. **Testowanie:**  
   - Przeprowadzenie testów jednostkowych dla walidacji i logiki serwisowej.
   - Testy integracyjne symulujące poprawne oraz niepoprawne żądania.
7. **Code Review i wdrożenie:**  
   - Przegląd kodu przez zespół programistyczny.
   - Wdrożenie na środowisko testowe oraz monitorowanie działania endpointu.
8. **Monitorowanie:**  
   - Konfiguracja systemu logowania i monitorowania błędów w Django, aby szybko reagować na ewentualne problemy.
