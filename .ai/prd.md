# Dokument wymagań produktu (PRD) - VetAssist

## 1. Przegląd produktu

VetAssist to aplikacja wspierająca weterynarzy w ich codziennej praktyce klinicznej. Głównym celem produktu jest usprawnienie procesu podejmowania decyzji medycznych poprzez dostarczenie szybkiego dostępu do trzech kluczowych modułów:

1. Wyszukiwanie interakcji lekowych - umożliwiający sprawdzenie potencjalnych interakcji między różnymi lekami
2. Kalkulator dawkowania - pomagający w precyzyjnym obliczaniu dawki leku dla różnych gatunków zwierząt
3. Baza standaryzowanych protokołów leczenia - zapewniająca dostęp do sprawdzonych procedur postępowania w różnych sytuacjach klinicznych

VetAssist (MVP) ma być prostym, intuicyjnym narzędziem, które oszczędza czas lekarzy weterynarii i minimalizuje ryzyko błędów medycznych związanych z nieprawidłowym dawkowaniem leków lub nieznajomością interakcji lekowych.

## 2. Problem użytkownika

Weterynarze w swojej pracy napotykają na szereg wyzwań związanych z dostępem do aktualnych i wiarygodnych informacji medycznych:

1. Brak szybkiego dostępu do informacji o interakcjach między lekami, co może prowadzić do niebezpiecznych kombinacji podczas terapii
2. Trudność w precyzyjnym dawkowaniu leków dla różnych gatunków zwierząt o zróżnicowanej wadze
3. Brak łatwego dostępu do standaryzowanych protokołów leczenia, które mogłyby zapewnić spójne podejście do często występujących przypadków klinicznych
4. Presja czasowa podczas wizyt, utrudniająca wyszukiwanie niezbędnych informacji z różnych źródeł

VetAssist odpowiada bezpośrednio na te problemy, dostarczając weterynarze wszystkich niezbędnych informacji w jednym, łatwo dostępnym miejscu, co pozwala na szybkie i pewne podejmowanie decyzji klinicznych.

## 3. Wymagania funkcjonalne

### 3.1. Moduł wyszukiwania interakcji lekowych
- Możliwość wprowadzania listy leków
- Otrzymywanie informacji o potencjalnych interakcjach (ograniczone do 200 znaków)
- Możliwość dodania dodatkowego kontekstu (do 50 znaków) do zapytania
- Interfejs z przyciskami oceny jakości odpowiedzi (kciuk w górę/kciuk w dół)

### 3.2. Moduł kalkulatora dawkowania
- Wybór leku z predefiniowanej listy
- Wprowadzanie wagi zwierzęcia (liczba całkowita do 3 znaków)
- Wybór gatunku zwierzęcia z listy rozwijanej
- Wybór docelowej jednostki miary z listy rozwijanej
- Wyświetlanie wyniku obliczonej dawki
- Ocena użyteczności wyniku (kciuk w górę/kciuk w dół)

### 3.3. Moduł protokołów postępowania
- Dostęp do standaryzowanych protokołów i checklist postępowania
- Wyniki ograniczone do 200 znaków
- Możliwość oceny przydatności protokołu (kciuk w górę/kciuk w dół)

### 3.4. Zarządzanie kontem użytkownika
- Rejestracja nowego użytkownika
- Logowanie do systemu
- Zmiana hasła
- Usuwanie konta

### 3.5. System audytu i feedbacku
- Zbieranie ocen użytkowników (kciuk w górę/kciuk w dół)
- Zapisywanie źródła oceny (który moduł)
- Gromadzenie danych do analizy satysfakcji użytkowników

### 3.6. Struktury danych
- Ujednolicony schemat JSON dla leków z polami: "name", "activeIngredient", "species", "measurementValue", "measurementTarget", "contraindications" (każda wartość ograniczona do 20 znaków)

## 4. Granice produktu

W ramach MVP **nie będą** uwzględnione:

- Rozbudowane zarządzanie wizytami lub kalendarz leczenia
- Zaawansowane funkcjonalności analizy danych pacjenta
- Rozbudowany frontend z dużym naciskiem na design
- System powiadomień
- Integracja z zewnętrznymi systemami szpitali weterynaryjnych
- Możliwość dodawania własnych leków do bazy
- Rozbudowane raportowanie
- Funkcje społecznościowe lub forum dyskusyjne
- Aplikacja mobilna (MVP to aplikacja webowa)

## 5. Historyjki użytkowników

### Zarządzanie kontem użytkownika

#### US-001
- Tytuł: Rejestracja nowego użytkownika
- Opis: Jako nowy użytkownik, chcę móc zarejestrować się w systemie, aby uzyskać dostęp do funkcjonalności aplikacji.
- Kryteria akceptacji:
  1. Formularz rejestracji zawiera pola: email, hasło, potwierdzenie hasła
  2. System waliduje poprawność adresu email
  3. System wymaga hasła o długości minimum 8 znaków
  4. System informuje użytkownika o błędach w formularzu
  5. Po poprawnej rejestracji system wyświetla komunikat o sukcesie
  6. Użytkownik otrzymuje email z linkiem aktywacyjnym

#### US-002
- Tytuł: Logowanie do systemu
- Opis: Jako zarejestrowany użytkownik, chcę móc zalogować się do systemu, aby korzystać z dostępnych funkcjonalności.
- Kryteria akceptacji:
  1. Formularz logowania zawiera pola: email i hasło
  2. System waliduje poprawność wprowadzonych danych
  3. System informuje użytkownika o błędach logowania
  4. Po poprawnym logowaniu użytkownik jest przekierowany do strony głównej
  5. System zapamiętuje sesję użytkownika

#### US-003
- Tytuł: Zmiana hasła
- Opis: Jako zalogowany użytkownik, chcę móc zmienić hasło do swojego konta, aby zapewnić jego bezpieczeństwo.
- Kryteria akceptacji:
  1. Dostępna opcja zmiany hasła w ustawieniach konta
  2. Formularz zawiera pola: aktualne hasło, nowe hasło, potwierdzenie nowego hasła
  3. System waliduje poprawność aktualnego hasła
  4. Nowe hasło musi spełniać wymogi bezpieczeństwa (min. 8 znaków)
  5. System informuje o pomyślnej zmianie hasła

#### US-004
- Tytuł: Usuwanie konta
- Opis: Jako zalogowany użytkownik, chcę móc usunąć swoje konto, aby moje dane zostały usunięte z systemu.
- Kryteria akceptacji:
  1. Dostępna opcja usunięcia konta w ustawieniach
  2. System wymaga potwierdzenia operacji przez wprowadzenie hasła
  3. System wyświetla ostrzeżenie o nieodwracalności operacji
  4. Po usunięciu konta wszystkie dane użytkownika są usuwane
  5. Po usunięciu konta użytkownik jest wylogowywany i przekierowany na stronę główną

#### US-005
- Tytuł: Odzyskiwanie zapomnianego hasła
- Opis: Jako użytkownik, który zapomniał hasła, chcę móc je zresetować, aby odzyskać dostęp do mojego konta.
- Kryteria akceptacji:
  1. Dostępna opcja "Zapomniałem hasła" na stronie logowania
  2. Formularz wymaga podania adresu email
  3. System wysyła email z linkiem do resetowania hasła
  4. Link do resetowania hasła jest ważny przez 24 godziny
  5. Po kliknięciu w link użytkownik może ustawić nowe hasło

### Moduł interakcji lekowych

#### US-006
- Tytuł: Wyszukiwanie interakcji lekowych
- Opis: Jako weterynarz, chcę móc wprowadzić listę leków, aby sprawdzić potencjalne interakcje między nimi.
- Kryteria akceptacji:
  1. Interfejs umożliwia wybór kilku leków z listy
  2. System generuje informację o interakcjach (do 200 znaków)
  3. Wynik jest prezentowany w czytelny sposób
  4. System informuje, jeśli nie znaleziono interakcji

#### US-007
- Tytuł: Dodawanie kontekstu do wyszukiwania interakcji
- Opis: Jako weterynarz, chcę móc dodać kontekst do wyszukiwania interakcji, aby otrzymać bardziej precyzyjną odpowiedź.
- Kryteria akceptacji:
  1. Dostępne pole do wprowadzenia dodatkowego kontekstu (max 50 znaków)
  2. System uwzględnia dodatkowy kontekst w generowaniu odpowiedzi
  3. Pole kontekstu jest opcjonalne

#### US-008
- Tytuł: Ocena wyników interakcji lekowych
- Opis: Jako weterynarz, chcę móc ocenić otrzymane informacje o interakcjach, aby pomóc w ulepszaniu systemu.
- Kryteria akceptacji:
  1. Dostępne przyciski oceny (kciuk w górę/kciuk w dół)
  2. System zapisuje ocenę wraz z identyfikacją modułu
  3. System potwierdza zapisanie oceny

### Moduł kalkulatora dawkowania

#### US-009
- Tytuł: Obliczanie dawki leku
- Opis: Jako weterynarz, chcę móc obliczyć dawkę leku dla zwierzęcia, aby zapewnić bezpieczne dawkowanie.
- Kryteria akceptacji:
  1. Interfejs umożliwia wybór leku z listy
  2. Możliwość wprowadzenia wagi zwierzęcia (do 3 cyfr)
  3. Możliwość wyboru gatunku zwierzęcia z listy
  4. Możliwość wyboru docelowej jednostki miary
  5. System oblicza i wyświetla dawkę leku
  6. System informuje o ewentualnych przeciwwskazaniach

#### US-010
- Tytuł: Walidacja danych w kalkulatorze dawkowania
- Opis: Jako weterynarz, chcę aby system walidował wprowadzane dane, aby uniknąć błędów w obliczeniach.
- Kryteria akceptacji:
  1. System sprawdza, czy waga jest liczbą całkowitą do 3 cyfr
  2. System nie pozwala na przesłanie formularza z nieprawidłowymi danymi
  3. System wyświetla komunikaty o błędach walidacji

#### US-011
- Tytuł: Ocena wyników kalkulatora dawkowania
- Opis: Jako weterynarz, chcę móc ocenić otrzymane obliczenia dawkowania, aby pomóc w ulepszaniu systemu.
- Kryteria akceptacji:
  1. Dostępne przyciski oceny (kciuk w górę/kciuk w dół)
  2. System zapisuje ocenę wraz z identyfikacją modułu
  3. System potwierdza zapisanie oceny

### Moduł protokołów postępowania

#### US-012
- Tytuł: Wyszukiwanie protokołów postępowania
- Opis: Jako weterynarz, chcę móc wyszukać standardowe protokoły postępowania dla danej sytuacji klinicznej, aby zapewnić prawidłowe leczenie.
- Kryteria akceptacji:
  1. Interfejs umożliwia wprowadzenie opisu sytuacji klinicznej
  2. System generuje protokół postępowania (do 200 znaków)
  3. Wynik jest prezentowany w czytelny sposób

#### US-013
- Tytuł: Ocena protokołów postępowania
- Opis: Jako weterynarz, chcę móc ocenić otrzymane protokoły postępowania, aby pomóc w ulepszaniu systemu.
- Kryteria akceptacji:
  1. Dostępne przyciski oceny (kciuk w górę/kciuk w dół)
  2. System zapisuje ocenę wraz z identyfikacją modułu
  3. System potwierdza zapisanie oceny

### Nawigacja i interfejs

#### US-014
- Tytuł: Nawigacja między modułami
- Opis: Jako weterynarz, chcę móc łatwo nawigować między trzema głównymi modułami, aby efektywnie korzystać z aplikacji.
- Kryteria akceptacji:
  1. Widoczne, wyraźnie oddzielone moduły w interfejsie
  2. Intuicyjne menu nawigacyjne
  3. Przejście między modułami nie wymaga przeładowania całej strony
  4. Aktualnie wybrany moduł jest wizualnie oznaczony

#### US-015
- Tytuł: Dostęp do historii wyszukiwań
- Opis: Jako weterynarz, chcę mieć dostęp do historii moich wcześniejszych wyszukiwań i obliczeń, aby nie musieć powtarzać tych samych operacji.
- Kryteria akceptacji:
  1. Lista ostatnich wyszukiwań/obliczeń dla zalogowanego użytkownika
  2. Możliwość ponownego użycia wcześniejszych zapytań
  3. Historia wyszukiwań zapisywana jest oddzielnie dla każdego modułu

## 6. Metryki sukcesu

### 6.1. Metryki techniczne
- Czas odpowiedzi na zapytania o interakcje lekowe: średnio poniżej 2 sekund
- Czas odpowiedzi na zapytania o protokoły leczenia: średnio poniżej 2 sekund
- Czas obliczania dawki leku: natychmiastowy (poniżej 0,5 sekundy)
- Dostępność systemu: minimum 99,5% czasu

### 6.2. Metryki użyteczności
- Pozytywny feedback od użytkowników: minimum 75% ocen pozytywnych (kciuk w górę)
- Liczba błędów zgłaszanych przez użytkowników: malejąca z tygodnia na tydzień
- Czas potrzebny nowemu użytkownikowi na wykonanie podstawowych operacji: poniżej 1 minuty

### 6.3. Metryki adopcji
- Liczba aktywnych użytkowników: wzrost o minimum 10% miesięcznie
- Liczba przeprowadzonych obliczeń dawek: minimum 5 na aktywnego użytkownika tygodniowo
- Liczba wyszukanych interakcji lekowych: minimum 3 na aktywnego użytkownika tygodniowo
- Liczba wyszukanych protokołów: minimum 2 na aktywnego użytkownika tygodniowo