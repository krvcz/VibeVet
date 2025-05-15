# Plan testów backendu

## 1. Wprowadzenie i cele testowania
Celem testów jest zapewnienie niezawodności, stabilności i bezpieczeństwa systemu backendowego. Testowanie ma na celu:
- Weryfikację poprawności działania poszczególnych modułów systemu.
- Zapewnienie właściwej integracji między komponentami, w tym komunikacji z bazą danych PostgreSQL.
- Oceny wydajnościowego i bezpieczeństwa aplikacji.
- Wczesne wykrycie i eliminację błędów przed wdrożeniem na produkcję.
- Weryfikację poprawności integracji z usługami zewnętrznymi, szczególnie z openrouter.ai.

## 2. Zakres testów
Testy obejmują wszystkie kluczowe komponenty backendu, w szczególności:
- **Moduł użytkowników (users):** Zarządzanie rejestracją, logowaniem, profilami użytkowników.
- **Moduł terapii (treatments):** Operacje na danych dotyczących terapii, w tym dodawanie, modyfikacja i usuwanie.
- **Moduł interakcji (interactions):** Sprawdzanie logiki i powiązań między różnymi komponentami systemu.
- **Moduł leków (drugs):** Weryfikacja danych o lekach, przeliczanie dawek oraz integracja z systemem obliczeniowym.
- **Komponenty wspólne (common) oraz fixture'y:** Narzędzia i dane pomocnicze wykorzystywane przez inne moduły.
- **Konfiguracja systemu (config) oraz logi:** Sprawdzanie poprawności ładowania konfiguracji i rejestrowania zdarzeń.
- **Integracja z AI:** Testowanie komunikacji i przetwarzania danych między backendem a openrouter.ai.
- **Migracje bazy danych:** Weryfikacja poprawności schematów i integralności danych podczas migracji.

## 3. Typy testów do przeprowadzenia
- **Testy jednostkowe:** Weryfikacja pojedynczych funkcji oraz metod odpowiadających za logikę biznesową.
- **Testy integracyjne:** Sprawdzenie współdziałania między modułami oraz poprawności komunikacji z bazą danych.
- **Testy funkcjonalne (end-to-end):** Symulacja rzeczywistych scenariuszy użytkowania (np. rejestracja, logowanie, zarządzanie terapiami).
- **Testy wydajnościowe:** Ocena zachowania systemu przy zwiększonym obciążeniu oraz analiza czasów odpowiedzi.
- **Testy bezpieczeństwa:** Sprawdzenie odporności systemu na potencjalne ataki, weryfikacja mechanizmów autoryzacji i uwierzytelnienia.
- **Testy migracji bazy danych:** Weryfikacja procesu migracji i integralności danych po migracji.
- **Testy integracji z AI:** Sprawdzenie poprawności komunikacji z openrouter.ai oraz przetwarzania odpowiedzi.

## 4. Scenariusze testowe dla kluczowych funkcjonalności
- **Użytkownicy:**
  - Rejestracja nowego użytkownika oraz walidacja danych.
  - Logowanie, generowanie i weryfikacja tokenów uwierzytelniających.
  - Aktualizacja i usuwanie danych profilu użytkownika.
- **Terapie:**
  - Dodawanie, edycja i usuwanie wpisów dotyczących terapii.
  - Sprawdzanie poprawności relacji między terapią a profilem użytkownika.
- **Interakcje:**
  - Weryfikacja poprawności logiki łączenia pomiędzy modułem terapii a modułem leków.
  - Testy przepływu danych między modułami.
- **Leki:**
  - Import i walidacja danych o lekach.
  - Przeliczanie dawek lekowych oraz weryfikacja poprawności obliczeń.
  - Testowanie przetwarzania dużych zbiorów danych medycznych.
- **Konfiguracja i logi:**
  - Testy poprawności wczytywania konfiguracji systemu.
  - Weryfikacja prawidłowości rejestrowania zdarzeń oraz dostępności logów.
- **Integracja z AI:**
  - Testy wysyłania zapytań do openrouter.ai i przetwarzania odpowiedzi.
  - Weryfikacja mechanizmów fallback w przypadku niedostępności usługi AI.
  - Sprawdzenie precyzji analizy ulotek leków PDF i ekstrakcji informacji o dawkowaniu.
- **Baza danych:**
  - Testowanie migracji schematu bazy danych przy aktualizacji systemu.
  - Weryfikacja utrzymania integralności danych podczas migracji.

## 5. Środowisko testowe
- **Lokalne:** Środowisko deweloperskie, użycie Django test runner oraz symulacja konfiguracji bazodanowej na PostgreSQL.
- **Staging:** Replika środowiska produkcyjnego, umożliwiająca testy integracyjne oraz wydajnościowe.
- **CI/CD:** Automatyczne uruchamianie testów przy użyciu GitHub Actions, z raportowaniem wyników w systemie kontroli wersji.
- **Mock serwisy:** Symulacja usług zewnętrznych, w tym openrouter.ai, do testów offline.

## 6. Narzędzia do testowania
- **Frameworki testowe:** Django test runner, unittest, pytest.
- **Narzędzia integracyjne:** Postman lub Insomnia do testowania API.
- **Testy wydajnościowe:** Locust lub JMeter.
- **Narzędzia analizy pokrycia kodu:** Coverage.py.
- **Systemy CI/CD:** GitHub Actions do automatyzacji testów.
- **System zarządzania błędami:** JIRA lub GitHub Issues.
- **Narzędzia do zarządzania danymi testowymi:** Factory Boy, Django fixtures.
- **Narzędzia monitorowania:** Prometheus, Grafana.

## 7. Harmonogram testów
- **Testy jednostkowe:** Uruchamiane automatycznie przy każdym commicie.
- **Testy integracyjne:** Przeprowadzane przy każdym wdrożeniu na środowisko staging.
- **Testy wydajnościowe i bezpieczeństwa:** Realizowane cyklicznie, np. na koniec każdego sprintu.
- **Testy migracji bazy danych:** Wykonywane przed każdą aktualizacją schematu.
- **Testy integracji z AI:** Przeprowadzane przy każdej zmianie w interfejsie API do openrouter.ai.
- **Testy akceptacyjne:** Przed finalnym wdrożeniem na produkcję.

## 8. Kryteria akceptacji testów
### Ogólne kryteria:
- Pokrycie kodu testami nie mniejsze niż 80%.
- Brak krytycznych błędów w testach integracyjnych, wydajnościowych i bezpieczeństwa.
- Zatwierdzenie wszystkich scenariuszy testowych przez zespół QA i deweloperów.

### Specyficzne kryteria modułowe:
- **Moduł użytkowników:** 100% poprawności procesów uwierzytelniania i autoryzacji, pełna walidacja danych wejściowych.
- **Moduł terapii:** Poprawność kalkulacji i relacji, integralność danych między pacjentami i protokołami leczenia.
- **Moduł leków:** Precyzja kalkulacji dawek z dokładnością 99.9%, odporność na błędy przy dużych zbiorach danych.
- **Integracja z AI:** Skuteczność analizy na poziomie minimum 95%, czas odpowiedzi poniżej 3 sekund.
- **Migracje bazy danych:** 100% zachowanie integralności danych, poprawne przejście wszystkich migracji w obu kierunkach.

## 9. Zarządzanie danymi testowymi
- **Dane statyczne:** Przygotowane fixtury zawierające reprezentatywne dane dla wszystkich modułów.
- **Dane generowane:** Wykorzystanie Factory Boy do dynamicznego generowania danych testowych.
- **Dane produkcyjne:** Zanonimizowane kopie danych produkcyjnych do testów wydajnościowych.
- **Strategia czyszczenia:** Automatyczne przywracanie stanu bazy danych po każdej sesji testowej.
- **Wersjonowanie danych testowych:** Synchronizacja zestawów testowych z wersjami rozwojowymi aplikacji.

## 10. Role i odpowiedzialności w procesie testowania
- **Inżynier QA:** Opracowanie, wdrożenie oraz utrzymanie scenariuszy testowych, analiza wyników oraz raportowanie błędów.
- **Deweloperzy:** Naprawa zgłoszonych błędów oraz wdrożenie poprawek zgodnie z wytycznymi QA.
- **Manager Projektu:** Koordynacja procesu testowania, monitorowanie postępów oraz komunikacja z zespołem.
- **DevOps:** Konfiguracja i utrzymanie środowisk testowych oraz narzędzi CI/CD.
- **Data Scientist:** Weryfikacja integracji z openrouter.ai i jakości przetwarzania danych przez AI.

## 11. Procedury raportowania błędów
- **Zgłaszanie błędów:** Błędy będą zgłaszane za pomocą systemu JIRA lub GitHub Issues z pełnym opisem, krokami reprodukcji oraz dołączonymi logami lub zrzutami ekranu.
- **Priorytetyzacja:** Błędy będą klasyfikowane według ich wpływu na funkcjonalność systemu (krytyczne, wysokie, średnie, niskie).
- **Komunikacja:** Regularne spotkania zespołu QA i deweloperów w celu omówienia postępów oraz priorytetów w naprawie błędów.
- **Weryfikacja:** Po poprawkach inicjowane będą ponowne testy regresyjne w celu potwierdzenia eliminacji zgłoszonych problemów.

## 12. Monitorowanie i reagowanie po wdrożeniu
- **Monitorowanie ciągłe:** Wykorzystanie narzędzi Prometheus i Grafana do śledzenia wydajności i dostępności systemu.
- **Alerty:** Konfiguracja powiadomień w przypadku przekroczenia progów wydajnościowych lub błędów aplikacji.
- **Procedury reagowania na incydenty:** Zdefiniowany proces diagnostyki i rozwiązywania problemów w środowisku produkcyjnym.
- **Testy A/B:** Monitorowanie wpływu nowych funkcjonalności na zachowanie użytkowników.
- **Feedback loop:** Systematyczne zbieranie informacji od użytkowników i implementacja usprawnień.