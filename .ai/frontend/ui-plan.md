# Architektura UI dla VetAssist

## 1. Przegląd struktury UI
VetAssist to aplikacja webowa zapewniająca trzy główne moduły wspierające funkcje kliniczne weterynarzy – kalkulator dawkowania, wyszukiwanie interakcji lekowych oraz vademecum leczenia – uzupełnione o panel ustawień użytkownika oraz widok zarządzania niestandardowymi lekami (CRUD). UI opiera się na podejściu mobile-first, wykorzystując Astro, React, Tailwind i Shadcn/ui dla spójnego, responsywnego i dostosowanego do potrzeb użytkowników interfejsu.

## 2. Lista widoków
### 1. Widok logowania (Mock)
- **Ścieżka widoku:** `/login`
- **Główny cel:** Umożliwić symulację logowania użytkownika do systemu.
- **Kluczowe informacje do wyświetlenia:** Formularz logowania z polami email i hasło, komunikaty walidacyjne.
- **Kluczowe komponenty widoku:** Formularz, przycisk submit, inline komunikaty błędów.
- **UX, dostępność i względy bezpieczeństwa:** Prosty interfejs z uwzględnieniem standardów dostępności (ARIA labels, obsługa klawiatury), symulacja bez realnego uwierzytelniania.

### 2. Widok kalkulatora dawkowania
- **Ścieżka widoku:** `/dosage-calculator`
- **Główny cel:** Umożliwić szybkie obliczanie dawki leku na podstawie wybranych parametrów.
- **Kluczowe informacje do wyświetlenia:** Lista predefiniowanych leków, pola wejściowe do wprowadzenia wagi, wybór gatunku oraz jednostki miary, wynik obliczenia.
- **Kluczowe komponenty widoku:** Formularze z rozwijanymi listami, buttony do zatwierdzania, dynamiczny wyświetlacz wyniku oraz element oceny (kciuk w górę/dół) z animacją.
- **UX, dostępność i względy bezpieczeństwa:** Mobile-first design, responsywne formularze, walidacja danych inline z komunikatami, natychmiastowa informacja zwrotna przy obliczeniach.

### 3. Widok interakcji lekowych
- **Ścieżka widoku:** `/drug-interactions`
- **Główny cel:** Umożliwić wyszukiwanie potencjalnych interakcji między lekami przy wsparciu AI.
- **Kluczowe informacje do wyświetlenia:** Pole do wyboru leków (lista wielokrotnego wyboru), opcjonalne pole do dodawania kontekstu, prezentacja wyników interakcji (opis, data, rating).
- **Kluczowe komponenty widoku:** Formularz z listą wielokrotnego wyboru, pola tekstowe, przyciski oceny z animacjami, loader/spinner podczas oczekiwania na odpowiedź.
- **UX, dostępność i względy bezpieczeństwa:** Jasna nawigacja kroków wyszukiwania, informacja o trwających operacjach, elementy dostosowane dla urządzeń mobilnych, komunikaty błędów inline.

### 4. Widok vademecum leczenia
- **Ścieżka widoku:** `/treatment-guide`
- **Główny cel:** Umożliwić wprowadzenie czynników diagnostycznych i otrzymanie listy potencjalnych schorzeń przy wsparciu AI.
- **Kluczowe informacje do wyświetlenia:** Formularz do wprowadzania wielu czynników diagnostycznych, lista wyników z opisami, mechanizm oceny wyników.
- **Kluczowe komponenty widoku:** Dynamiczne formularze do dodawania czynników, przyciski potwierdzające, elementy do oceny wyników, area dyspozycyjna na prezentację wyników z loaderem.
- **UX, dostępność i względy bezpieczeństwa:** Łatwość wprowadzania wielu danych, walidacja i natychmiastowa informacja zwrotna, standardy dostępności zapewniające czytelność i nawigację.

### 5. Panel ustawień użytkownika
- **Ścieżka widoku:** `/account/settings`
- **Główny cel:** Umożliwić zarządzanie kontem użytkownika (zmiana hasła, edycja danych, ustawienia personalizacji).
- **Kluczowe informacje do wyświetlenia:** Formularze do edycji danych konta, sekcja zmiany hasła, opcja usuwania konta, historia wyszukiwań.
- **Kluczowe komponenty widoku:** Formularze, przyciski potwierdzające operacje, sekcja wyświetlania historii, komunikaty sukcesu/błędów.
- **UX, dostępność i względy bezpieczeństwa:** Jasny podział sekcji, uwzględnienie mechanizmów bezpieczeństwa (weryfikacja przez hasło przy krytycznych operacjach), zgodność z wytycznymi dostępu (ARIA, responsywność).

### 6. Widok zarządzania niestandardowymi lekami (CRUD)
- **Ścieżka widoku:** `/custom-drugs`
- **Główny cel:** Umożliwić użytkownikowi tworzenie, edycję, przeglądanie i usuwanie leków niestandardowych.
- **Kluczowe informacje do wyświetlenia:** Lista istniejących niestandardowych leków, przyciski do dodania nowego leku, formularz edycji z walidacją i komunikatami błędów.
- **Kluczowe komponenty widoku:** Tabela/lista, formularze CRUD, przyciski (utwórz, edytuj, usuń), modal dialogi potwierdzające operacje.
- **UX, dostępność i względy bezpieczeństwa:** Intuicyjna edycja i zarządzanie danymi, jednoznaczne komunikaty o błędach, potwierdzenie operacji krytycznych, responsywne tabele oraz formularze.

## 3. Mapa podróży użytkownika
1. **Start:** Użytkownik trafia na stronę logowania (`/login`) i loguje się (symulacja).
2. **Główna nawigacja:** Po logowaniu użytkownik trafia do głównego dashboardu, gdzie górne menu umożliwia wybór modułu.
3. **Wybór modułu:** Użytkownik wybiera jeden z modułów: kalkulator dawkowania, interakcja lekowa, vademecum leczenia, panel ustawień lub niestandardowe leki.
4. **Interakcja:** W obrębie wybranego modułu użytkownik wprowadza dane (np. wybiera lek, wprowadza wagę) → system prezentuje wynik oraz umożliwia ocenę.
5. **Powiadomienia:** W trakcie operacji prezentowane są loadery/spinery. Po zakończeniu operacji wyświetlane są komunikaty sukcesu lub błędy inline.
6. **Przegląd historii i ustawienia:** Użytkownik może przejść do panelu ustawień, aby sprawdzić historię i zarządzać kontem.

## 4. Układ i struktura nawigacji
Główna nawigacja oparta będzie na stałym, górnym menu z widocznymi zakładkami odpowiadającymi głównym widokom (Kalkulator, Interakcje, Vademecum, Custom Leki, Ustawienia). Aktualnie aktywna zakładka będzie wyróżniona wizualnie. Nawigacja nie wymaga pełnego przeładowania strony (SPA) z płynnymi przejściami między widokami. Dla urządzeń mobilnych menu będzie zoptymalizowane pod kątem dotykowej interakcji i responsywności.

## 5. Kluczowe komponenty
- **Menu nawigacyjne:** Główne, responsywne menu z wyróżnieniem aktywnego modułu.
- **Formularze:** Wielostronicowe formularze z walidacją inline i komunikatami błędów, używające standardów dostępności.
- **Przyciski oceny:** Komponenty z animowanymi ikonami (np. kciuk w górę/kciuk w dół) do oceny wyników.
- **Loader/Spinner:** Komponenty informujące o trwających operacjach, używane globalnie.
- **Modal Dialogi:** Potwierdzenie operacji krytycznych, np. usuwanie konta lub leków.
- **Komponenty list i tabel:** Dynamiczne listy do prezentacji wyników wyszukiwań, z opcjami filtrowania i sortowania, zoptymalizowane pod kątem responsywności.