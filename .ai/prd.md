# Dokument wymagań produktu (PRD) - VibeVet AI

## 1. Przegląd produktu

VibeVet AI to aplikacja webowa skierowana do weterynarzy, która automatyzuje proces przeliczania dawek leków weterynaryjnych. Aplikacja wykorzystuje sztuczną inteligencję do analizy ulotek leków w formacie PDF i generowania dokładnych dawek na podstawie gatunku zwierzęcia oraz jego parametrów, takich jak waga. System umożliwia użytkownikom tworzenie własnej bazy leków, przeglądanie, edycję i usuwanie wprowadzonych informacji, co przyczynia się do redukcji błędów i zaoszczędzenia czasu podczas codziennej praktyki weterynaryjnej.

Aplikacja wykorzystuje zewnętrzną usługę do analizy dokumentów PDF, która zwraca dane w ustrukturyzowanym formacie JSON. Dzięki temu weterynarze mogą szybko uzyskać dostęp do potrzebnych informacji o lekach, a następnie dostosować je do swoich potrzeb przed zapisaniem w bazie danych.

## 2. Problem użytkownika

Weterynarze stoją przed następującymi wyzwaniami:

- Manualne czytanie ulotek i przeliczanie dawek leków weterynaryjnych jest czasochłonne.
- Proces ten jest podatny na błędy ludzkie, co może prowadzić do nieprawidłowego dawkowania.
- Brak ujednoliconego systemu do przechowywania i zarządzania informacjami o dawkowaniu leków dla różnych gatunków zwierząt.
- Trudności w szybkim dostępie do historycznych danych o lekach i ich dawkowaniu.

VibeVet AI rozwiązuje te problemy poprzez automatyzację procesu analizy ulotek leków i przeliczania dawek, umożliwiając weterynarznonym szybsze i dokładniejsze decyzje dotyczące leczenia zwierząt.

## 3. Wymagania funkcjonalne

### 3.1 Przetwarzanie ulotek leków

System będzie korzystał z zewnętrznej usługi do analizy dokumentów PDF z ulotkami leków. Usługa ta będzie zwracać dane w formacie JSON, zawierające informacje o leku, jego dawkowaniu, gatunkach dla których jest przeznaczony oraz skutkach ubocznych.

### 3.2 Przeliczanie dawek leków

System będzie przeliczał dawki leków na podstawie następujących parametrów:
- Gatunek zwierzęcia (np. pies, kot)
- Waga zwierzęcia
- Jednostka miary (jeśli potrzebna)

### 3.3 Zarządzanie bazą leków

Użytkownicy będą mogli:
- Przeglądać listę leków w formie tabelarycznej
- Dodawać nowe leki manualnie
- Dodawanie leków z plików pdf
- Zatwierdzanie wygenerowych danych leków przez AI z PDF
- Edytować informacje o lekach (nazwa, dawkowanie, gatunek, skutki uboczne)
- Usuwać leki z bazy danych

### 3.4 Zarządzanie kontem użytkownika

System będzie umożliwiał:
- Tworzenie nowych kont użytkowników
- Logowanie do systemu
- Zmianę hasła (wymaga potwierdzenia)
- Usuwanie konta (wymaga weryfikacji hasła)

### 3.5 Interfejs użytkownika

Interfejs użytkownika będzie:
- Prezentował listę leków w formie tabelarycznej
- Umożliwiał łatwe wprowadzanie danych o zwierzęciu (gatunek, waga)
- Pozwalał na modyfikację danych przed zapisaniem ich do bazy
- Zapewniał przyjazną prezentację danych o lekach

## 4. Granice produktu

W ramach MVP nie będą realizowane następujące funkcjonalności:

- Załączanie wielu plików PDF jednocześnie
- Integracje z innymi platformami weterynaryjnymi
- Aplikacje mobilne (tylko wersja webowa)
- Obsługa innych formatów niż PDF
- Współdzielenie własnej bazy leków pomiędzy kontami użytkowników
- Zaawansowane mechanizmy zabezpieczeń poza standardową autentykacją i autoryzacją

## 5. Historyjki użytkowników

### US-001: Rejestracja nowego użytkownika

#### Tytuł
Rejestracja nowego użytkownika

#### Opis
Jako nowy użytkownik, chcę utworzyć konto w systemie, aby móc korzystać z funkcji aplikacji i budować własną bazę leków.

#### Kryteria akceptacji
1. Użytkownik może wprowadzić adres e-mail, hasło i potwierdzenie hasła.
2. System wymaga hasła o odpowiedniej sile (minimum 8 znaków, w tym litery, cyfry i znaki specjalne).
3. System sprawdza, czy adres e-mail nie jest już zarejestrowany.
4. System wysyła e-mail z linkiem aktywacyjnym.
5. Konto jest aktywowane po kliknięciu w link.
6. Użytkownik otrzymuje potwierdzenie utworzenia konta.

### US-002: Logowanie do systemu

#### Tytuł
Logowanie do systemu

#### Opis
Jako zarejestrowany użytkownik, chcę logować się do systemu, aby uzyskać dostęp do moich zapisanych leków i korzystać z funkcji aplikacji.

#### Kryteria akceptacji
1. Użytkownik może wprowadzić adres e-mail i hasło.
2. System weryfikuje poprawność danych logowania.
3. System informuje o błędnych danych logowania.
4. Po poprawnym logowaniu użytkownik jest przekierowywany do strony głównej aplikacji.
5. Sesja użytkownika jest utrzymywana przez określony czas.

### US-003: Zmiana hasła

#### Tytuł
Zmiana hasła do konta

#### Opis
Jako zalogowany użytkownik, chcę zmienić hasło do mojego konta, aby zwiększyć bezpieczeństwo moich danych.

#### Kryteria akceptacji
1. Użytkownik może wprowadzić stare hasło, nowe hasło i potwierdzenie nowego hasła.
2. System weryfikuje poprawność starego hasła.
3. System sprawdza, czy nowe hasło spełnia wymagania bezpieczeństwa.
4. System wymaga potwierdzenia zmiany hasła.
5. Użytkownik otrzymuje potwierdzenie zmiany hasła.

### US-004: Usunięcie konta

#### Tytuł
Usunięcie konta użytkownika

#### Opis
Jako zalogowany użytkownik, chcę usunąć moje konto, aby usunąć moje dane z systemu.

#### Kryteria akceptacji
1. Użytkownik może zainicjować proces usunięcia konta.
2. System wymaga podania hasła w celu weryfikacji.
3. System wymaga potwierdzenia usunięcia konta.
4. Po usunięciu konta, wszystkie dane użytkownika są usuwane z systemu.
5. Użytkownik otrzymuje potwierdzenie usunięcia konta.

### US-005: Przesyłanie ulotki leku w PDF

#### Tytuł
Przesyłanie ulotki leku w formacie PDF

#### Opis
Jako zalogowany użytkownik, chcę przesłać ulotkę leku w formacie PDF, aby system mógł automatycznie wyodrębnić informacje o leku.

#### Kryteria akceptacji
1. Użytkownik może wybrać plik PDF z lokalnego komputera.
2. System sprawdza, czy plik jest w formacie PDF.
3. System informuje o maksymalnym rozmiarze pliku.
4. System wysyła plik do zewnętrznej usługi analizującej.
5. System wyświetla komunikat o trwającym przetwarzaniu.
6. Po zakończeniu przetwarzania, system prezentuje wyodrębnione dane.

### US-006: Przeglądanie wyników analizy ulotki

#### Tytuł
Przeglądanie wyników analizy ulotki

#### Opis
Jako zalogowany użytkownik, chcę zobaczyć wyniki analizy ulotki leku, aby sprawdzić poprawność wyodrębnionych informacji.

#### Kryteria akceptacji
1. System prezentuje nazwę leku, dawkowanie, gatunki oraz skutki uboczne.
2. Informacje są przedstawione w przejrzysty i czytelny sposób.
3. Użytkownik może przejrzeć wszystkie wyodrębnione dane przed zapisaniem.
4. System oznacza miejsca, gdzie dane mogą być niepewne lub niekompletne.

### US-007: Edycja danych o leku przed zapisaniem

#### Tytuł
Edycja danych o leku przed zapisaniem

#### Opis
Jako zalogowany użytkownik, chcę mieć możliwość edycji danych o leku przed zapisaniem ich do bazy, aby poprawić ewentualne błędy analizy.

#### Kryteria akceptacji
1. Użytkownik może edytować nazwę leku.
2. Użytkownik może edytować informacje o dawkowaniu.
3. Użytkownik może edytować listę gatunków.
4. Użytkownik może edytować informacje o skutkach ubocznych.
5. System zapisuje zmiany po zatwierdzeniu przez użytkownika.

### US-008: Zapisywanie leku do bazy danych

#### Tytuł
Zapisywanie leku do bazy danych

#### Opis
Jako zalogowany użytkownik, chcę zapisać lek do mojej bazy danych, aby móc go później wykorzystać.

#### Kryteria akceptacji
1. Użytkownik może zatwierdzić zapisanie leku do bazy danych.
2. System weryfikuje, czy wszystkie wymagane pola są wypełnione.
3. System zapisuje lek w bazie danych użytkownika.
4. Użytkownik otrzymuje potwierdzenie zapisania leku.

### US-009: Manualne dodawanie leku do bazy

#### Tytuł
Manualne dodawanie leku do bazy

#### Opis
Jako zalogowany użytkownik, chcę móc ręcznie dodać lek do mojej bazy, bez konieczności analizy ulotki PDF.

#### Kryteria akceptacji
1. Użytkownik może wprowadzić nazwę leku, dawkowanie, gatunki oraz skutki uboczne.
2. System weryfikuje, czy wszystkie wymagane pola są wypełnione.
3. Użytkownik zatwierdza poprawność wygenerowanych danych leków.
4. Użytkownik może zapisać wprowadzone dane.
5. System zapisuje lek w bazie danych użytkownika.
6. Użytkownik otrzymuje potwierdzenie zapisania leku.

### US-010: Przeglądanie bazy leków

#### Tytuł
Przeglądanie bazy leków

#### Opis
Jako zalogowany użytkownik, chcę przeglądać moją bazę leków, aby znaleźć potrzebne informacje.

#### Kryteria akceptacji
1. System wyświetla listę leków w formie tabelarycznej.
2. Użytkownik może sortować leki według nazwy, gatunku, itp.
3. Użytkownik może filtrować leki według różnych kryteriów.
4. System wyświetla podstawowe informacje o lekach w tabeli.
5. Użytkownik może kliknąć na lek, aby zobaczyć szczegółowe informacje.

### US-011: Edycja zapisanego leku

#### Tytuł
Edycja zapisanego leku

#### Opis
Jako zalogowany użytkownik, chcę edytować informacje o zapisanym leku, aby zaktualizować dane.

#### Kryteria akceptacji
1. Użytkownik może wybrać lek do edycji.
2. System wyświetla formularz z aktualnymi danymi leku.
3. Użytkownik może edytować wszystkie pola.
4. System weryfikuje, czy wszystkie wymagane pola są wypełnione po edycji.
5. System zapisuje zaktualizowane dane.
6. Użytkownik otrzymuje potwierdzenie aktualizacji danych.

### US-012: Usuwanie leku z bazy

#### Tytuł
Usuwanie leku z bazy

#### Opis
Jako zalogowany użytkownik, chcę usunąć lek z mojej bazy danych, gdy nie jest już potrzebny.

#### Kryteria akceptacji
1. Użytkownik może wybrać lek do usunięcia.
2. System wymaga potwierdzenia usunięcia leku.
3. Po potwierdzeniu, lek jest usuwany z bazy danych.
4. Użytkownik otrzymuje potwierdzenie usunięcia leku.

### US-013: Przeliczanie dawki leku

#### Tytuł
Przeliczanie dawki leku

#### Opis
Jako zalogowany użytkownik, chcę przeliczyć dawkę leku dla konkretnego zwierzęcia, aby określić odpowiednią ilość leku.

#### Kryteria akceptacji
1. Użytkownik może wybrać lek z bazy.
2. Użytkownik może wybrać gatunek zwierzęcia.
3. Użytkownik może wprowadzić wagę zwierzęcia.
4. Użytkownik może wybrać jednostkę miary wagi (jeśli potrzebna).
5. System przelicza dawkę leku na podstawie wprowadzonych danych.
6. System wyświetla przeliczoną dawkę leku.

### US-014: Podsumowanie leków z podziałem

#### Tytuł
Generowanie podsumowania leków

#### Opis
Jako zalogowany użytkownik, chcę wygenerować podsumowanie leków z podziałem na dawkę i gatunek, aby mieć przejrzysty obraz mojej bazy leków.

#### Kryteria akceptacji
1. Użytkownik może zainicjować generowanie podsumowania.
2. System generuje raport z podziałem leków według dawki i gatunku.
3. System prezentuje dane w przejrzystej formie.
4. Użytkownik może sortować i filtrować wyniki podsumowania.

### US-015: Wylogowanie z systemu

#### Tytuł
Wylogowanie z systemu

#### Opis
Jako zalogowany użytkownik, chcę wylogować się z systemu, aby zakończyć sesję.

#### Kryteria akceptacji
1. Użytkownik może kliknąć przycisk wylogowania.
2. System kończy sesję użytkownika.
3. Użytkownik jest przekierowywany na stronę logowania.
4. Dane sesji są usuwane.

## 6. Metryki sukcesu

### 6.1 Metryki techniczne

- 75% danych o lekach wygenerowanych przez AI jest akceptowane przez użytkownika bez konieczności edycji.
- Średni czas przetwarzania ulotki PDF nie przekracza 10 sekund.
- System działa stabilnie przy jednoczesnym użytkowaniu przez co najmniej 50 użytkowników.

### 6.2 Metryki biznesowe

- 75% użytkowników generuje minimum 5 leków i ich dawek miesięcznie.
- 60% użytkowników wraca do aplikacji co najmniej raz w tygodniu.
- Liczba aktywnych użytkowników rośnie o minimum 10% miesięcznie.

### 6.3 Metryki użytkownika

- Czas potrzebny na dodanie nowego leku (od przesłania ulotki do zapisania w bazie) nie przekracza 2 minut.
- 70% użytkowników ocenia interfejs aplikacji jako intuicyjny i łatwy w obsłudze.
- Liczba zgłaszanych problemów z przeliczaniem dawek nie przekracza 5% wszystkich przeprowadzonych przeliczeń.