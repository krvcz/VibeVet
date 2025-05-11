# Przewodnik wdrożenia usługi OpenRouter

## 1. Opis usługi
Usługa OpenRouter ma za zadanie komunikację z API OpenRouter w celu uzupełnienia czatów opartych na LLM. Usługa odpowiada za:
- Przygotowanie i wysłanie żądania do API, zawierającego niezbędne parametry (komunikat systemowy, komunikat użytkownika, nazwa modelu, parametry modelu).
- Odbiór i walidację odpowiedzi, uwzględniając ustrukturyzowany schemat JSON (response_format).
- Integrację z backendem Django, inspirowaną istniejącymi serwisami (np. `drug_interaction_service.py` oraz `treatment_guide_service.py`).

## 2. Opis konstruktora
Konstruktor usługi OpenRouter powinien:
- Inicjalizować konfigurację połączenia z API, w tym ustawienia URL, nagłówki autoryzacyjne (np. API key) oraz prefiksy komunikatów.
- Przyjąć jako argumenty dane konfiguracyjne, takie jak domyślna nazwa modelu (np. "gpt-3.5-turbo") oraz inne parametry modelu (temperature, max_tokens, itp.).
- Ustawić zależności do logowania oraz mechanizm obsługi błędów.

## 3. Publiczne metody i pola
**Publiczne metody:**
1. `send_openrouter_request(system_message: str, user_message: str, response_format: dict, model_name: str, model_params: dict) -> dict`  
   - Odpowiada za przygotowanie żądania do API.
   - Łączy komunikat systemowy z komunikatem użytkownika.
   - Wysyła żądanie i zwraca odpowiedź w ustrukturyzowanym formacie JSON.
2. `parse_response(response: dict) -> dict`  
   - Waliduje zgodność odpowiedzi z podanym schematem (response_format).
   - Zwraca sparsowane dane lub zgłasza błąd walidacji.

**Publiczne pola:**
- `api_url`: URL punktu końcowego OpenRouter API.
- `headers`: Słownik z nagłówkami, np. zawierającymi API key.
- `default_model`: Domyślna nazwa modelu wykorzystywanego przez API.
- `default_params`: Domyślne parametry modelu (np. `temperature`, `max_tokens`).

## 4. Prywatne metody i pola
**Prywatne metody:**
1. `_prepare_payload(system_message: str, user_message: str, response_format: dict, model_name: str, model_params: dict) -> dict`  
   - Tworzy ładunek JSON zgodny z wymaganiami API.
   - Przykład ustrukturyzowanego schematu:
     ```json
     {
       "system_message": "Podaj komunikat systemowy, np. 'Proszę przetworzyć poniższe dane.'",
       "user_message": "Treść komunikatu użytkownika",
       "response_format": {
         "type": "json_schema",
         "json_schema": {
           "name": "OpenRouterResponseSchema",
           "strict": true,
           "schema": {
             "answer": "string",
             "confidence": "number"
           }
         }
       },
       "model": model_name,
       "model_params": model_params
     }
     ```
2. `_handle_api_errors(response: dict)`  
   - Analizuje odpowiedź pod kątem błędów (np. błędy sieci, błędy autoryzacji, błędy walidacji schematu).
   - W razie wystąpienia błędu wywołuje odpowiednią logikę obsługi.

**Prywatne pola:**
- `_logger`: Instancja loggera do rejestrowania operacji oraz błędów.
- `_timeout`: Domyślny czas oczekiwania na odpowiedź API.

## 5. Obsługa błędów
Potencjalne scenariusze błędów oraz podejścia ich obsługi:
1. **Błąd połączenia sieciowego lub timeout:**  
   - Rozwiązanie: Użyć mechanizmu ponawiania żądania, rejestrować błąd, informować użytkownika o problemach z połączeniem.
2. **Błąd autoryzacji (np. nieprawidłowy API key):**  
   - Rozwiązanie: Walidować konfigurację autoryzacyjną przy inicjalizacji, logować szczegóły błędu i zwracać klarowny komunikat.
3. **Błąd walidacji odpowiedzi (niezgodność response_format):**  
   - Rozwiązanie: Przeprowadzać walidację odpowiedzi przy użyciu biblioteki (np. zod lub custom schema validation), zgłaszać specyficzny wyjątek.
4. **Błąd odpowiedzi API (np. status 500):**  
   - Rozwiązanie: Logować pełen komunikat błędu, informować o wewnętrznym błędzie serwisu oraz ewentualnie uruchamiać mechanizm alarmowy.

## 6. Kwestie bezpieczeństwa
- **Przechowywanie API Key:**  
  Przechowywać klucz autoryzacyjny w bezpiecznych zmiennych środowiskowych oraz w bezpiecznym managerze konfiguracji Django.
- **Walidacja wejścia:**  
  Walidować wszystkie dane wejściowe przed wysłaniem żądania do API oraz przed zapisaniem odpowiedzi w bazie danych.
- **Logowanie i monitoring:**  
  Rejestrować zarówno operacje udane, jak i błędy, zapewniając audyt oraz możliwość szybkiej reakcji na incydenty.
- **Ograniczenia dostępu i rate limiting:**  
  Zabezpieczyć endpointy API przed nadużyciami oraz implementować mechanizmy firewalli i rate limiting.

## 7. Plan wdrożenia krok po kroku
1. **Utworzenie nowego modułu serwisu:**
   - Utworzyć plik, np. `openrouter_service.py` wewnątrz folderu `./backend/common/services/`.
   - Zaimplementować konstruktor oraz prywatne metody `_prepare_payload` i `_handle_api_errors`.

2. **Implementacja metody publicznej do wysyłania żądania:**
   - Zaimplementować metodę `send_openrouter_request`, która:
     - Łączy komunikat systemowy i użytkownika.
     - Używa `_prepare_payload` do przygotowania żądania.
     - Wysyła żądanie (np. przy użyciu biblioteki `requests`).
     - Odbiera odpowiedź i przekazuje ją do metody `parse_response` w celu walidacji.

3. **Konfiguracja response_format:**
   - Zdefiniować wzorzec response_format zgodnie z:
     ```json
     {
       "type": "json_schema",
       "json_schema": {
         "name": "OpenRouterResponseSchema",
         "strict": true,
         "schema": {
           "answer": "string",
           "confidence": "number"
         }
       }
     }
     ```
   - Zapewnić, że odpowiedzi API są walidowane pod kątem tego schematu.

4. **Konfiguracja parametrów modelu:**
   - Ustalić domyślne wartości dla `model_name` (np. "gpt-3.5-turbo") oraz `model_params` (np. `{ "temperature": 0.7, "max_tokens": 1500 }`).
   - Zaimplementować możliwość nadpisania tych parametrów przy wywołaniu metody.

5. **Integracja z istniejącymi serwisami Django:**
   - Zainspirować się implementacjami w [drug_interaction_service.py](http://_vscodecontentref_/0) oraz [treatment_guide_service.py](http://_vscodecontentref_/1).
   - Upewnić się, że logika połączenia oraz obsługa błędów opiera się o już wdrożone wzorce.


---
Ten przewodnik wdrożenia zapewnia kompleksowe podejście, obejmujące wszystkie kluczowe komponenty usługi OpenRouter oraz wdrożenie najlepszych praktyk dotyczących bezpieczeństwa, obsługi błędów i integracji z istniejącym stackiem technologicznym projektu.