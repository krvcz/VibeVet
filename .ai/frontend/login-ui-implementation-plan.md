# Plan implementacji widoku Logowania

## 1. Przegląd
Widok logowania umożliwia zarejestrowanym użytkownikom (weterynarzom) dostęp do aplikacji VetAssist. Użytkownik wprowadza swój adres email i hasło, które są weryfikowane przez backend (Django auth). Po pomyślnym zalogowaniu użytkownik jest przekierowywany do głównego interfejsu aplikacji, a jego sesja jest zapamiętywana. Widok musi być prosty, intuicyjny i zgodny ze standardami dostępności.

## 2. Routing widoku
Widok będzie dostępny pod ścieżką `/login`. Implementacja w Astro jako plik `src/pages/login.astro`.

## 3. Struktura komponentów
src/pages/login.astro └── src/layouts/BaseLayout.astro (lub inny odpowiedni layout) └── src/components/auth/LoginForm.tsx (client:load) ├── Shadcn/ui Form │ ├── Shadcn/ui FormField (Email) │ │ ├── Shadcn/ui FormLabel │ │ ├── Shadcn/ui FormControl │ │ │ └── Shadcn/ui Input (type="email") │ │ └── Shadcn/ui FormMessage (dla błędów email) │ ├── Shadcn/ui FormField (Hasło) │ │ ├── Shadcn/ui FormLabel │ │ ├── Shadcn/ui FormControl │ │ │ └── Shadcn/ui Input (type="password") │ │ └── Shadcn/ui FormMessage (dla błędów hasła) │ └── Shadcn/ui Button (type="submit", z obsługą stanu ładowania) └── (Opcjonalnie) Miejsce na ogólne komunikaty błędów (np. błąd serwera, nieprawidłowe dane)


## 4. Szczegóły komponentów
### `src/pages/login.astro`
- **Opis komponentu:** Strona Astro definiująca ścieżkę `/login`. Odpowiada za renderowanie podstawowego layoutu strony oraz osadzenie interaktywnego komponentu formularza logowania (`LoginForm.tsx`).
- **Główne elementy:** Wykorzystanie komponentu layoutu (np. `BaseLayout.astro`), renderowanie komponentu `<LoginForm client:load />`. Może być odpowiedzialny za przekazanie początkowych danych (np. CSRF token, jeśli jest wymagany i pobierany po stronie serwera Astro).
- **Obsługiwane interakcje:** Brak bezpośrednich interakcji użytkownika.
- **Obsługiwana walidacja:** Brak.
- **Typy:** Standardowe typy Astro.
- **Propsy:** Może przyjmować propsy layoutu.

### `src/components/auth/LoginForm.tsx`
- **Opis komponentu:** Interaktywny formularz React do obsługi logowania użytkownika. Zarządza stanem pól email i hasła, walidacją po stronie klienta, komunikacją z API logowania, wyświetlaniem błędów oraz obsługą procesu wysyłania formularza. Zbudowany przy użyciu komponentów Shadcn/ui oraz biblioteki `react-hook-form` do zarządzania formularzem.
- **Główne elementy:** Komponent `Form` z `react-hook-form` i Shadcn/ui, dwa pola `FormField` (dla email i hasła) zawierające `FormLabel`, `FormControl` z `Input` oraz `FormMessage`. Przycisk `Button` typu `submit`. Opcjonalny element do wyświetlania błędów niezwiązanych z konkretnym polem (np. `Alert` z Shadcn/ui).
- **Obsługiwane interakcje:**
    - Wprowadzanie tekstu w polach Email i Hasło (`onChange`).
    - Wysłanie formularza (`onSubmit`) poprzez kliknięcie przycisku "Zaloguj się" lub naciśnięcie Enter w jednym z pól.
- **Obsługiwana walidacja:**
    - **Email:** Wymagane, musi być poprawnym formatem adresu email.
    - **Hasło:** Wymagane, nie może być puste. (Minimalna długość nie jest wymagana przez US-002 dla logowania, ale może być dodana dla spójności).
- **Typy:** `LoginFormData` (ViewModel), `LoginErrorViewModel` (ViewModel), `LoginCommand` (DTO dla żądania API).
- **Propsy:**
    - `csrfToken?: string` (Opcjonalnie, jeśli token CSRF jest przekazywany z Astro).

## 5. Typy
- **`LoginFormData` (ViewModel):** Interfejs reprezentujący dane formularza w komponencie React.
    ```typescript
    // filepath: c:\Users\user\Desktop\VibeVetAI\frontend\src\components\auth\types.ts
    export interface LoginFormData {
      email: string;
      password: string;
    }
    ```
- **`LoginCommand` (DTO):** Interfejs reprezentujący dane wysyłane do API logowania Django. Zakładając, że Django auth używa `username` jako identyfikatora.
    ```typescript
    // filepath: c:\Users\user\Desktop\VibeVetAI\frontend\src\types.ts
    // ...existing code...
    /* ====================================== */
    /* ============ AUTH MODELS ============= */
    /* ====================================== */

    export interface LoginCommand {
        username: string; // Email address will be used as username
        password: string;
    }

    // Potentially add UserDTO if login response returns user details
    // export interface UserDTO { ... }
    // export interface LoginResponseDTO { user: UserDTO; }
    // ...existing code...
    ```
- **`LoginErrorViewModel` (ViewModel):** Interfejs do przechowywania błędów walidacji lub błędów API do wyświetlenia w UI.
    ```typescript
    // filepath: c:\Users\user\Desktop\VibeVetAI\frontend\src\components\auth\types.ts
    export interface LoginErrorViewModel {
      email?: string;
      password?: string;
      nonFieldError?: string; // For general errors like invalid credentials or server errors
    }
    ```

## 6. Zarządzanie stanem
- Stan formularza (wartości pól, błędy walidacji, stan wysyłania) będzie zarządzany lokalnie w komponencie `LoginForm.tsx` przy użyciu biblioteki `react-hook-form`.
- Dodatkowy stan `isLoading` (boolean) do śledzenia postępu wywołania API i `apiError` (`string | null`) do przechowywania ogólnych błędów API (np. błąd serwera, nieprawidłowe dane logowania) będzie zarządzany za pomocą hooka `useState`.
- Nie przewiduje się potrzeby tworzenia dedykowanego customowego hooka dla tak prostego formularza, chyba że logika stanie się bardziej złożona. `react-hook-form` dostarcza wystarczających narzędzi.

## 7. Integracja API
- **Endpoint:** `POST /api/auth/login/` (Do potwierdzenia z backendem - domyślna ścieżka Django REST Framework dla logowania).
- **Żądanie:**
    - Metoda: `POST`
    - Nagłówki:
        - `Content-Type: application/json`
        - `X-CSRFToken: <wartość tokena>` (Jeśli wymagane przez Django)
    - Ciało (Body): Obiekt JSON zgodny z typem `LoginCommand`.
        ```json
        {
          "username": "user@example.com",
          "password": "user_password"
        }
        ```
- **Odpowiedź:**
    - **Sukces (200 OK):** Puste ciało odpowiedzi. Backend ustawia ciasteczko sesji (np. `sessionid`) w nagłówku `Set-Cookie`.
    - **Błąd - Nieprawidłowe dane (400 Bad Request):** Ciało odpowiedzi zawiera JSON z błędami, np.:
        ```json
        {
          "non_field_errors": ["Unable to log in with provided credentials."]
        }
        ```
    - **Błąd - Błąd serwera (500 Internal Server Error):** Ciało odpowiedzi może zawierać szczegóły błędu (w trybie DEBUG) lub być puste/generyczne.
    - **Błąd - Brak/Nieprawidłowy CSRF (403 Forbidden):** Odpowiedź bez ciała lub z komunikatem o błędzie CSRF.
- **Implementacja:** Wywołanie API zostanie zrealizowane za pomocą funkcji `fetch` lub biblioteki typu `axios` wewnątrz handlera `onSubmit` dostarczonego przez `react-hook-form`. Należy obsłużyć różne kody statusu odpowiedzi i odpowiednio zaktualizować stan komponentu (błędy, stan ładowania) lub przekierować użytkownika.

## 8. Interakcje użytkownika
- **Wprowadzanie danych:** Użytkownik wpisuje email i hasło w odpowiednie pola. Stan formularza jest aktualizowany na bieżąco.
- **Walidacja na żywo (opcjonalnie):** Błędy walidacji mogą pojawiać się podczas wpisywania lub po utracie fokusa przez pole (konfigurowalne w `react-hook-form`).
- **Wysyłanie formularza:**
    - Użytkownik klika przycisk "Zaloguj się" lub naciska Enter.
    - Walidacja jest uruchamiana. Jeśli wystąpią błędy, są one wyświetlane pod odpowiednimi polami, a wysyłanie jest blokowane.
    - Jeśli walidacja przejdzie pomyślnie, przycisk jest dezaktywowany, pokazywany jest wskaźnik ładowania, a wywołanie API jest wysyłane.
- **Odpowiedź API:**
    - **Sukces:** Wskaźnik ładowania znika, użytkownik jest przekierowywany na stronę główną aplikacji (np. `/dashboard`).
    - **Błąd:** Wskaźnik ładowania znika, przycisk staje się ponownie aktywny, odpowiedni komunikat błędu (np. "Nieprawidłowy email lub hasło", "Błąd serwera") jest wyświetlany w formularzu.

## 9. Warunki i walidacja
- **Email:**
    - Warunek: Musi być podany.
    - Walidacja: Sprawdzenie, czy pole nie jest puste i czy ciąg znaków pasuje do wzorca adresu email (np. za pomocą wyrażenia regularnego lub walidatora `zod`).
    - Komponent: `LoginForm.tsx` (pole email).
    - Stan interfejsu: Wyświetlenie komunikatu błędu pod polem email, jeśli walidacja nie przejdzie. Blokada wysłania formularza.
- **Hasło:**
    - Warunek: Musi być podane.
    - Walidacja: Sprawdzenie, czy pole nie jest puste.
    - Komponent: `LoginForm.tsx` (pole hasła).
    - Stan interfejsu: Wyświetlenie komunikatu błędu pod polem hasła, jeśli walidacja nie przejdzie. Blokada wysłania formularza.
- **API (CSRF Token):**
    - Warunek: Jeśli backend wymaga tokenu CSRF, musi on być dołączony do żądania POST.
    - Walidacja: Po stronie backendu.
    - Komponent: Logika pobierania i wysyłania tokenu w `LoginForm.tsx` (lub przekazana z `login.astro`).
    - Stan interfejsu: W przypadku błędu 403, wyświetlenie ogólnego komunikatu błędu.

## 10. Obsługa błędów
- **Błędy walidacji klienta:** Obsługiwane przez `react-hook-form` i schemę walidacji (np. Zod). Komunikaty wyświetlane są pod odpowiednimi polami za pomocą komponentu `FormMessage` z Shadcn/ui.
- **Błędy API (np. 400 - nieprawidłowe dane):** Odpowiedź API jest parsowana. Jeśli zawiera `non_field_errors`, komunikat jest wyświetlany jako ogólny błąd formularza. Jeśli (mniej prawdopodobne w przypadku logowania) zawiera błędy specyficzne dla pól, można je przypisać do odpowiednich pól w `react-hook-form`.
- **Błędy sieciowe (fetch nie powiódł się):** Blok `catch` w obsłudze wywołania `fetch`. Wyświetlenie ogólnego komunikatu o błędzie połączenia.
- **Błędy serwera (5xx):** Wyświetlenie ogólnego komunikatu o błędzie serwera, np. "Wystąpił nieoczekiwany błąd. Spróbuj ponownie później.".
- **Błąd CSRF (403):** Wyświetlenie ogólnego komunikatu błędu. Może wymagać odświeżenia strony przez użytkownika.
- **Stan ładowania:** Przycisk "Zaloguj się" powinien być nieaktywny i pokazywać wskaźnik ładowania (np. spinner) podczas trwania wywołania API, aby zapobiec wielokrotnemu wysyłaniu formularza.

## 11. Kroki implementacji
1.  **Utworzenie strony Astro:** Stwórz plik `src/pages/login.astro`. Skonfiguruj podstawowy layout (np. `BaseLayout.astro`).
2.  **Utworzenie komponentu React:** Stwórz plik `src/components/auth/LoginForm.tsx`.
3.  **Zdefiniowanie typów:** Dodaj typy `LoginFormData`, `LoginErrorViewModel` w `src/components/auth/types.ts` oraz `LoginCommand` w `src/types.ts`.
4.  **Implementacja formularza:** W `LoginForm.tsx` użyj `react-hook-form` i komponentów Shadcn/ui (`Form`, `FormField`, `FormLabel`, `FormControl`, `Input`, `Button`, `FormMessage`) do zbudowania struktury formularza z polami email i hasła.
5.  **Implementacja walidacji:** Zdefiniuj schemę walidacji (np. używając `zod`) dla `LoginFormData` i zintegruj ją z `react-hook-form`. Skonfiguruj wyświetlanie błędów walidacji za pomocą `FormMessage`.
6.  **Implementacja logiki wysyłania:** W `LoginForm.tsx` zaimplementuj funkcję `onSubmit`, która będzie wywoływana przez `react-hook-form`.
7.  **Obsługa stanu ładowania:** Dodaj stan `isLoading` (`useState`) i aktualizuj go przed i po wywołaniu API. Użyj tego stanu do dezaktywacji przycisku i wyświetlania wskaźnika ładowania.
8.  **Integracja API:** Zaimplementuj wywołanie `POST /api/auth/login/` (lub potwierdzonej ścieżki) używając `fetch` lub `axios`. Przekaż dane z formularza (`LoginCommand`) i ewentualny token CSRF.
9.  **Obsługa odpowiedzi API:** W logice `onSubmit` obsłuż różne odpowiedzi API (sukces 200, błąd 400, błąd 500, błąd 403). W przypadku sukcesu przekieruj użytkownika (`window.location.href = '/dashboard'`). W przypadku błędu zaktualizuj stan błędów (`apiError` lub błędy `react-hook-form`) w celu wyświetlenia komunikatu użytkownikowi.
10. **Obsługa CSRF (jeśli wymagane):** Zaimplementuj logikę pobierania tokenu CSRF (np. z ciasteczka `csrftoken` ustawionego przez Django) i dołączania go do nagłówka `X-CSRFToken` żądania API. Może to wymagać drobnych modyfikacji w `login.astro` lub globalnej konfiguracji pobierania API.
11. **Dostępność:** Upewnij się, że wszystkie elementy formularza mają odpowiednie etykiety (`FormLabel` z Shadcn/ui powinien to zapewnić), a nawigacja za pomocą klawiatury działa poprawnie. Użyj atrybutów ARIA tam, gdzie to konieczne (Shadcn/ui zazwyczaj robi to domyślnie).
12. **Styling:** Dostosuj wygląd za pomocą Tailwind, jeśli domyślne style Shadcn/ui wymagają modyfikacji.
13. **Osadzenie w Astro:** W `login.astro` zaimportuj i użyj komponentu `<LoginForm client:load />`. Przekaż ewentualne propsy (np. `csrfToken`).
14. **Testowanie:** Przetestuj wszystkie ścieżki: pomyślne logowanie, błędne dane, błędy walidacji, błędy serwera, nawigację klawiaturą.