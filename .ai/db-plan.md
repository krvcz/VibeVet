# VetAssist - Schemat Bazy Danych

## 1. Tabele, Kolumny, Typy Danych i Ograniczenia

### User
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| email       | VARCHAR(50) | NOT NULL, UNIQUE          |
| password    | VARCHAR(100)| NOT NULL                  |
| isActive    | BOOLEAN     | NOT NULL, DEFAULT TRUE    |
| createdAt   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updatedAt   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| createdBy   | INT         | NULL                      |

### Species
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| name        | VARCHAR(20) | NOT NULL, UNIQUE          |
| createdAt   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updatedAt   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| createdBy   | INT         | NOT NULL, REFERENCES User(id) |

### MeasurementUnit
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| shortName   | VARCHAR(5)  | NOT NULL, UNIQUE          |
| name        | VARCHAR(20) | NOT NULL, UNIQUE          |
| createdAt   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updatedAt   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| createdBy   | INT         | NOT NULL, REFERENCES User(id) |

### Drug
| Column             | Type        | Constraints                |
|-------------------|-------------|----------------------------|
| id                | SERIAL      | PRIMARY KEY                |
| name              | VARCHAR(20) | NOT NULL                  |
| activeIngredient  | VARCHAR(20) | NOT NULL                  |
| species_id        | INT         | NOT NULL, REFERENCES Species(id) |
| contraindications | VARCHAR(100)| NULL                      |
| measurementValue  | NUMERIC(10,5)| NOT NULL                  |
| measurementTarget_id | INT      | NOT NULL, REFERENCES MeasurementUnit(id) |
| createdAt         | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updatedAt         | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| createdBy         | INT         | NOT NULL, REFERENCES User(id) |

### CustomDrug
| Column             | Type        | Constraints                |
|-------------------|-------------|----------------------------|
| id                | SERIAL      | PRIMARY KEY                |
| name              | VARCHAR(20) | NOT NULL                  |
| activeIngredient  | VARCHAR(20) | NOT NULL                  |
| species_id        | INT         | NOT NULL, REFERENCES Species(id) |
| contraindications | VARCHAR(100)| NULL                      |
| measurementValue  | NUMERIC(10,5)| NOT NULL                  |
| measurementTarget_id | INT      | NOT NULL, REFERENCES MeasurementUnit(id) |
| user_id           | INT         | NOT NULL, REFERENCES User(id) |
| createdAt         | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updatedAt         | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| createdBy         | INT         | NOT NULL, REFERENCES User(id) |

### DrugInteractions
| Column           | Type         | Constraints                |
|-----------------|--------------|----------------------------|
| id              | SERIAL       | PRIMARY KEY                |
| query           | TEXT         | NOT NULL                  |
| result          | TEXT         | NOT NULL                  |
| context         | VARCHAR(50)  | NULL                      |
| positiveRating  | INT          | NOT NULL, DEFAULT 0       |
| negativeRating  | INT          | NOT NULL, DEFAULT 0       |
| createdAt       | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| updatedAt       | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| createdBy       | INT          | NOT NULL, REFERENCES User(id) |

### DrugInteractions_Drugs
| Column               | Type | Constraints                |
|---------------------|------|----------------------------|
| drugInteractions_id | INT  | NOT NULL, REFERENCES DrugInteractions(id) |
| drug_id             | INT  | NOT NULL, REFERENCES Drug(id) |

### TreatmentGuide
| Column           | Type         | Constraints                |
|-----------------|--------------|----------------------------|
| id              | SERIAL       | PRIMARY KEY                |
| query           | TEXT         | NOT NULL                  |
| result          | TEXT         | NOT NULL                  |
| factors         | JSONB        | NOT NULL                  |
| positiveRating  | INT          | NOT NULL, DEFAULT 0       |
| negativeRating  | INT          | NOT NULL, DEFAULT 0       |
| createdAt       | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| updatedAt       | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| createdBy       | INT          | NOT NULL, REFERENCES User(id) |

### SystemLogs
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| timestamp   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| logLevel    | VARCHAR(10) | NOT NULL                  |
| message     | TEXT        | NOT NULL                  |
| source      | VARCHAR(20) | NOT NULL                  |
| user_id     | INT         | NULL, REFERENCES User(id) |

### UserSearchHistory
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| user_id     | INT         | NOT NULL, REFERENCES User(id) |
| module      | VARCHAR(20) | NOT NULL                  |
| query       | TEXT        | NOT NULL                  |
| createdAt   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updatedAt   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |

## 2. Relacje między tabelami

1. **User do CustomDrug**: Jeden-do-Wielu
   - Jeden użytkownik może utworzyć wiele niestandardowych leków
   - Każdy niestandardowy lek należy dokładnie do jednego użytkownika

2. **Species do Drug**: Jeden-do-Wielu
   - Jeden gatunek może mieć wiele przypisanych leków
   - Każdy lek jest przypisany dokładnie do jednego gatunku

3. **Species do CustomDrug**: Jeden-do-Wielu
   - Jeden gatunek może mieć wiele przypisanych niestandardowych leków
   - Każdy niestandardowy lek jest przypisany dokładnie do jednego gatunku

4. **MeasurementUnit do Drug**: Jeden-do-Wielu
   - Jedna jednostka miary może być używana dla wielu leków
   - Każdy lek używa dokładnie jednej jednostki miary jako cel

5. **MeasurementUnit do CustomDrug**: Jeden-do-Wielu
   - Jedna jednostka miary może być używana dla wielu niestandardowych leków
   - Każdy niestandardowy lek używa dokładnie jednej jednostki miary jako cel

6. **DrugInteractions do Drug**: Wiele-do-Wielu (przez DrugInteractions_Drugs)
   - Jeden rekord interakcji leków może obejmować wiele leków
   - Jeden lek może być zaangażowany w wiele rekordów interakcji leków

7. **User do UserSearchHistory**: Jeden-do-Wielu
   - Jeden użytkownik może mieć wiele rekordów historii wyszukiwania
   - Każdy rekord historii wyszukiwania należy dokładnie do jednego użytkownika

8. **User do SystemLogs**: Jeden-do-Wielu (opcjonalnie)
   - Jeden użytkownik może być powiązany z wieloma logami systemowymi
   - Każdy log systemowy może być powiązany z jednym lub żadnym użytkownikiem (jeśli jest generowany przez system)

## 3. Indeksy

1. **Tabela User**:
   - Indeks na `email` (już obsługiwany przez ograniczenie UNIQUE)

2. **Tabela Drug**:
   - Indeks na `name` dla szybszego wyszukiwania leków
   - Indeks na `activeIngredient` dla wyszukiwań według składnika
   - Indeks na `species_id` dla filtrowanych wyszukiwań według gatunku

3. **Tabela CustomDrug**:
   - Indeks na `name` dla szybszego wyszukiwania leków
   - Indeks na `activeIngredient` dla wyszukiwań według składnika
   - Indeks złożony na `user_id` i `species_id` dla filtrowanych wyszukiwań

4. **Tabela DrugInteractions**:
   - Indeks na `createdAt` dla zapytań opartych na czasie
   - Indeks na `createdBy` dla historii interakcji użytkownika

5. **Tabela TreatmentGuide**:
   - Indeks GIN na `factors` dla wydajnych zapytań JSONB
   - Indeks na `createdAt` dla zapytań opartych na czasie
   - Indeks na `createdBy` dla historii przewodników leczenia użytkownika

6. **Tabela SystemLogs**:
   - Indeks na `timestamp` dla zapytań o logi oparte na czasie
   - Indeks na `source` dla pobierania logów specyficznych dla modułu
   - Indeks na `logLevel` dla filtrowania według poziomu ważności
   - Indeks na `user_id` dla pobierania logów specyficznych dla użytkownika

7. **Tabela UserSearchHistory**:
   - Indeks na `user_id` dla szybszego pobierania historii specyficznej dla użytkownika
   - Indeks na `module` dla pobierania historii specyficznej dla modułu
   - Indeks złożony na `user_id` i `module` dla filtrowanego pobierania historii
   - Indeks na `createdAt` dla pobierania historii uporządkowanej według czasu

## 4. Polityki bezpieczeństwa na poziomie wierszy PostgreSQL (RLS)

### Polityki RLS dla tabeli CustomDrug

```sql
ALTER TABLE "CustomDrug" ENABLE ROW LEVEL SECURITY;

-- Policy that allows users to see only their own custom drugs
CREATE POLICY custom_drug_user_isolation ON "CustomDrug"
    USING (user_id = current_user_id());
    
-- Policy that allows administrators to see all custom drugs
CREATE POLICY custom_drug_admin_access ON "CustomDrug"
    USING (current_user_has_role('admin'));
```

### Polityki RLS dla tabeli UserSearchHistory

```sql
ALTER TABLE "UserSearchHistory" ENABLE ROW LEVEL SECURITY;

-- Policy that allows users to see only their own search history
CREATE POLICY search_history_user_isolation ON "UserSearchHistory"
    USING (user_id = current_user_id());
    
-- Policy that allows administrators to see all search history
CREATE POLICY search_history_admin_access ON "UserSearchHistory"
    USING (current_user_has_role('admin'));
```

## 5. Dodatkowe uwagi i decyzje projektowe

1. **Pola audytowe**:
   - Wszystkie tabele oprócz SystemLogs zawierają standardowe pola audytowe (createdAt, updatedAt, createdBy)
   - SystemLogs ma pole timestamp zamiast createdAt, ponieważ jest to tabela logów

2. **Strategia cache'owania danych**:
   - Tabele DrugInteractions i TreatmentGuide służą jako pamięć podręczna dla odpowiedzi generowanych przez AI
   - Redukuje to liczbę wywołań API do usług AI i poprawia wydajność
   - Pola oceny pozwalają na ciągłe doskonalenie odpowiedzi AI

3. **Długości pól tekstowych**:
   - Długości pól są ograniczone zgodnie z wymaganiami
   - VARCHAR(20) dla większości pól nazw
   - VARCHAR(50) dla pól email i context
   - VARCHAR(100) dla dłuższych tekstów jak przeciwwskazania
   - TEXT dla nieograniczonych pól tekstowych jak wyniki zapytań

4. **Przechowywanie JSON**:
   - TreatmentGuide.factors używa JSONB do przechowywania ustrukturyzowanych danych o czynnikach diagnostycznych
   - JSONB jest preferowany nad JSON dla lepszej wydajności zapytań z indeksami GIN

5. **Historia wyszukiwania**:
   - Tabela UserSearchHistory przechowuje historię wyszukiwania użytkownika we wszystkich modułach
   - Wspiera to wymaganie US-016 dotyczące dostępu do poprzednich wyszukiwań

6. **Względy bezpieczeństwa**:
   - Bezpieczeństwo na poziomie wierszy (RLS) zapewnia izolację danych między użytkownikami
   - Pole password powinno przechowywać tylko hasła hashowane (odpowiedzialność logiki aplikacji)
   - Tabela SystemLogs umożliwia śledzenie zdarzeń związanych z bezpieczeństwem