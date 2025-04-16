# API Endpoint Implementation Plan: Get Drugs List

## 1. Przegląd punktu końcowego
Endpoint `/api/drugs` umożliwia pobranie listy standardowych leków z wsparciem paginacji i filtrowania przez opcjonalny parametr wyszukiwania (`search`). Celem jest szybkie udostępnienie klientom uporządkowanej listy leków.

## 2. Szczegóły żądania
- **Metoda HTTP:** GET  
- **Struktura URL:** `/api/drugs`  
- **Parametry zapytania:**
  - **Opcjonalne:**
    - `page` (int) – numer strony paginacji
    - `limit` (int) – liczba rekordów na stronę
    - `search` (string) – filtr dla nazwy leku lub składnika aktywnego

- **Brak Request Body**, ponieważ jest to operacja GET.

## 3. Wykorzystywane typy
- **DTO:**
  - `DrugDTO` – reprezentacja pojedynczego leku.
  - `PaginationDTO` – dane dotyczące paginacji.
  - `DrugsListResponseDTO` – opakowanie wyników i metadanych paginacyjnych.

- **Serializery:**
  - `DrugSerializer` z pliku `serializers.py` służy do serializacji danych leków.

## 4. Szczegóły odpowiedzi
- **Struktura JSON odpowiedzi:**
  ```json
  {
    "results": [
      {
        "id": 1,
        "name": "DrugA",
        "active_ingredient": "IngredientX",
        "species": 1,
        "measurement_value": "10.00000",
        "measurement_target": 1
      },
      ...
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100
    }
  }
  ```
- **Kody statusu:**
  - **200 OK:** Operacja zakończona sukcesem.
  - **400 Bad Request:** Nieprawidłowe dane wejściowe.
  - **500 Internal Server Error:** Błąd po stronie serwera.

## 5. Przepływ danych
1. Klient wysyła żądanie GET na endpoint `/api/drugs` z opcjonalnymi parametrami `page`, `limit` oraz `search`.
2. Endpoint w backendzie:
   - Waliduje parametry wejściowe.
   - Przekazuje żądanie do warstwy serwisowej (np. `drug_service.get_drugs_list(page, limit, search)`).
3. Warstwa serwisowa:
   - Pobiera dane leków z bazy danych przy użyciu Django ORM z mechanizmami filtrowania (na `name` lub `active_ingredient`) oraz paginacji.
4. Wyniki są serializowane przy użyciu `DrugSerializer`.
5. Ostateczna odpowiedź JSON zawiera wyniki oraz metadane paginacyjne.

## 6. Względy bezpieczeństwa
- **Walidacja wejściowa:** Sprawdzić typ i zakres parametrów `page` i `limit` oraz ograniczyć długość parametrów tekstowych (np. `search`).
- **Ochrona przed SQL Injection:** Wykorzystanie Django ORM eliminuje ryzyko SQL Injection.
- **Rate Limiting:** Rozważenie wdrożenia limitów żądań w celu zabezpieczenia przed atakami DDoS.

## 7. Obsługa błędów
- **Błąd walidacji:** Zwrócenie kodu 400 Bad Request wraz z komunikatem o nieprawidłowych danych.
- **Brak wyników:** Zwrócenie pustej listy wyników z kodem 200 OK, jeśli nie znaleziono pasujących rekordów.
- **Błąd serwera:** Zwrócenie 500 Internal Server Error przy nieoczekiwanych błędach, z rejestrowaniem błędów dla dalszej analizy.

## 8. Rozważania dotyczące wydajności
- **Paginacja:** Zapewnienie, że paginacja jest realizowana na poziomie zapytań do bazy danych.
- **Indeksacja:** Upewnienie się, że kolumny wykorzystywane przy filtrowaniu (np. `name`, `active_ingredient`) są odpowiednio indeksowane.
- **Cache:** Rozważenie zastosowania cache (np. Redis) przy dużym obciążeniu lub przy częstych zapytaniach.

## 9. Etapy wdrożenia
1. **Analiza i przygotowanie:**  
   - Przegląd specyfikacji oraz ustalenie domyślnych wartości paginacji (np. `page=1`, `limit=20`).

2. **Implementacja walidacji:**  
   - Walidacja parametrów zapytania przy użyciu mechanizmów Django oraz ewentualnie zod w przypadku endpointów Astro.

3. **Utworzenie warstwy logiki biznesowej:**  
   - Implementacja usługi (np. `drug_service`) odpowiedzialnej za pobieranie, filtrowanie i paginację leków.

4. **Integracja z modelem i serializerami:**  
   - Wykorzystanie Django ORM do pobierania danych z modelu `Drug`.
   - Serializacja wyników przy pomocy `DrugSerializer`.

5. **Testowanie:**  
   - Przeprowadzenie testów jednostkowych walidacji parametrów oraz testów integracyjnych symulujących żądania GET.
   - Testowanie poprawności odpowiedzi JSON oraz obsługi kodów błędów.

6. **Logowanie błędów:**  
   - Konfiguracja Django logging w celu rejestrowania wszelkich błędów i wyjątków.

7. **Code Review i wdrożenie:**  
   - Przeprowadzenie code review przez zespół.
   - Wdrożenie na środowisko testowe, a następnie produkcyjne.
