# Raport Analizy dla Frontendu ↔ Backend

## 1. Podsumowanie Analizy

- **Obsługa Pełnych Obiektów:**  
  Pola `species` oraz `measurement_target` powinny być reprezentowane jako pełne obiekty, a nie jako proste identyfikatory. Konieczne jest stworzenie dedykowanych interfejsów (`SpeciesDTO`, `MeasurementUnitDTO`) i użycie ich w odpowiednich typach (np. `DrugDTO`, `CustomDrugDTO`).

- **Zmiana Typu `measurement_value`:**  
  Backend dostarcza wartość `measurement_value` jako liczbę. W związku z tym, typ tego pola w interfejsach powinien być zmieniony z `string` na `number`.

- **Spójność z Walidacją:**  
  Frontend powinien uwzględniać walidację zgodną z backendową, np. minimalne i maksymalne wartości oraz długości ciągów w odpowiednich polach.
  
- **Obsługa Pól Opcjonalnych:**  
  Gdzie istnieje możliwość, że pole przyjmie wartość `null` lub będzie opcjonalne (np. `contraindications`), typ powinien zostać zdefiniowany jako unia (np. `string | null`).

## 2. Rekomendacje Dopasowania

1. **Utworzenie Dedykowanych Interfejsów:**  
   - Zdefiniuj interfejsy `SpeciesDTO` oraz `MeasurementUnitDTO` w pliku `types.ts`.
   - Zaktualizuj pola `species` i `measurement_target` w interfejsach takich jak `DrugDTO` i `CustomDrugDTO`, aby korzystały z nowych interfejsów.

2. **Aktualizacja Typu `measurement_value`:**  
   - Zmień typ `measurement_value` w interfejsach dotyczących leków (np. `DrugDTO`, `CustomDrugDTO`) z `string` na `number`.

3. **Dopasowanie Walidacji:**  
   - Zapewnij, że walidacja w formularzach frontendowych będzie zgodna z ograniczeniami i specyfikacjami backendowymi.
   - Upewnij się, że wszelkie operacje matematyczne wykonują się na wartościach liczbowych, a nie ciągach znaków.

4. **Zachowanie Spójności Opinii:**  
   - Pozostałe pola, takie jak daty (np. `created_at`), oceny (np. `positive_rating`) oraz inne informacje, pozostają bez zmian – o ile ich formaty (np. ISO datetime) są zgodne z backendem.
   - Jeśli istnieją dodatkowe pola opcjonalne, użyj typów unii tam, gdzie zachodzi taka potrzeba.

## 3. Założenia

- API backendu zwraca pełne obiekty dla pól `species` i `measurement_target`, co wymusza konieczność stworzenia dedykowanych interfejsów.
- Backend przesyła `measurement_value` jako liczbę, nie jako ciąg znaków.
- Zachowujemy możliwie największe podobieństwo między modelami backendowymi a frontendowymi dla utrzymania spójności i minimalizacji błędów.

## 4. Pytania Wyjaśniające

Na chwilę obecną nie ma dodatkowych pytań, ponieważ ustalenia są jasne. W przypadku pojawienia się nowych wymagań lub niejasności dotyczących pozostałych pól, zalecana jest ponowna weryfikacja struktury typów w `types.ts`.