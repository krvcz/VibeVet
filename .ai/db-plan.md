# VetAssist - Schemat Bazy Danych

## 1. Tabele, Kolumny, Typy Danych i Ograniczenia

### User (CustomUser)
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| email       | VARCHAR(254) | NOT NULL, UNIQUE          |
| password    | VARCHAR(128)| NOT NULL                  |
| is_active   | BOOLEAN     | NOT NULL, DEFAULT TRUE    |
| is_staff    | BOOLEAN     | NOT NULL, DEFAULT FALSE   |
| is_superuser| BOOLEAN     | NOT NULL, DEFAULT FALSE   |
| date_joined | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| last_login  | TIMESTAMP   | NULL                      |
| first_name  | VARCHAR(150)| NOT NULL                  |
| last_name   | VARCHAR(150)| NOT NULL                  |

### Species
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| name        | VARCHAR(20) | NOT NULL, UNIQUE          |
| description | TEXT        | NULL                      |
| created_at  | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updated_at  | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| created_by  | INT         | NOT NULL, REFERENCES User(id) |

### Unit (MeasurementUnit)
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| short_name  | VARCHAR(5)  | NOT NULL, UNIQUE          |
| name        | VARCHAR(20) | NOT NULL, UNIQUE          |
| description | TEXT        | NULL                      |
| created_at  | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updated_at  | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| created_by  | INT         | NOT NULL, REFERENCES User(id) |

### Drug
| Column             | Type        | Constraints                |
|-------------------|-------------|----------------------------|
| id                | SERIAL      | PRIMARY KEY                |
| name              | VARCHAR(20) | NOT NULL                  |
| active_ingredient | VARCHAR(20) | NOT NULL                  |
| species_id        | INT         | NOT NULL, REFERENCES Species(id) |
| contraindications | VARCHAR(100)| NULL                      |
| measurement_value | NUMERIC(10,5)| NOT NULL                  |
| measurement_unit_id | INT      | NOT NULL, REFERENCES Unit(id) |
| per_weight_value  | NUMERIC(10,5)| NOT NULL                  |
| per_weight_unit_id | INT       | NOT NULL, REFERENCES Unit(id) |
| created_at        | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updated_at        | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| created_by        | INT         | NOT NULL, REFERENCES User(id) |

### CustomDrug
| Column             | Type        | Constraints                |
|-------------------|-------------|----------------------------|
| id                | SERIAL      | PRIMARY KEY                |
| name              | VARCHAR(20) | NOT NULL                  |
| active_ingredient | VARCHAR(20) | NOT NULL                  |
| species_id        | INT         | NOT NULL, REFERENCES Species(id) |
| contraindications | VARCHAR(100)| NULL                      |
| measurement_value | NUMERIC(10,5)| NOT NULL                  |
| measurement_unit_id | INT      | NOT NULL, REFERENCES Unit(id) |
| per_weight_value  | NUMERIC(10,5)| NOT NULL                  |
| per_weight_unit_id | INT       | NOT NULL, REFERENCES Unit(id) |
| user_id           | INT         | NOT NULL, REFERENCES User(id) |
| created_at        | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updated_at        | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| created_by        | INT         | NOT NULL, REFERENCES User(id) |

### DrugInteraction (DrugInteractions)
| Column           | Type         | Constraints                |
|-----------------|--------------|----------------------------|
| id              | SERIAL       | PRIMARY KEY                |
| query           | TEXT         | NOT NULL                  |
| result          | TEXT         | NOT NULL                  |
| context         | VARCHAR(50)  | NULL                      |
| created_at      | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| updated_at      | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| created_by      | INT          | NOT NULL, REFERENCES User(id) |

### DrugInteraction_Drugs (relacja ManyToMany)
| Column               | Type | Constraints                |
|---------------------|------|----------------------------|
| druginteraction_id  | INT  | NOT NULL, REFERENCES DrugInteraction(id) |
| drug_id             | INT  | NOT NULL, REFERENCES Drug(id) |

### TreatmentGuide
| Column           | Type         | Constraints                |
|-----------------|--------------|----------------------------|
| id              | SERIAL       | PRIMARY KEY                |
| query           | TEXT         | NOT NULL                  |
| result          | TEXT         | NOT NULL                  |
| factors         | JSONB        | NOT NULL                  |
| created_at      | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| updated_at      | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| created_by      | INT          | NOT NULL, REFERENCES User(id) |

### Rating
| Column           | Type         | Constraints                |
|-----------------|--------------|----------------------------|
| id              | SERIAL       | PRIMARY KEY                |
| content_type_id | INT          | NOT NULL, REFERENCES ContentType(id) |
| object_id       | INT          | NOT NULL                  |
| rating          | VARCHAR(4)   | NOT NULL                  |
| created_at      | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| updated_at      | TIMESTAMP    | NOT NULL, DEFAULT NOW()   |
| created_by      | INT          | NOT NULL, REFERENCES User(id) |

### SystemLog (SystemLogs)
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| timestamp   | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| log_level   | VARCHAR(10) | NOT NULL                  |
| message     | TEXT        | NOT NULL                  |
| source      | VARCHAR(20) | NOT NULL                  |
| user_id     | INT         | NULL, REFERENCES User(id) |

### UserSearchHistory
| Column       | Type        | Constraints                |
|-------------|-------------|----------------------------|
| id          | SERIAL      | PRIMARY KEY                |
| module      | VARCHAR(20) | NOT NULL                  |
| query       | TEXT        | NOT NULL                  |
| created_at  | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| updated_at  | TIMESTAMP   | NOT NULL, DEFAULT NOW()   |
| created_by  | INT         | NOT NULL, REFERENCES User(id) |

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

4. **Unit do Drug (measurement_unit)**: Jeden-do-Wielu
   - Jedna jednostka miary może być używana dla wielu leków
   - Każdy lek używa dokładnie jednej jednostki miary dla wartości pomiaru

5. **Unit do Drug (per_weight_unit)**: Jeden-do-Wielu
   - Jedna jednostka miary może być używana dla wielu leków
   - Każdy lek używa dokładnie jednej jednostki miary dla wartości na wagę

6. **Unit do CustomDrug (measurement_unit)**: Jeden-do-Wielu
   - Jedna jednostka miary może być używana dla wielu niestandardowych leków
   - Każdy niestandardowy lek używa dokładnie jednej jednostki miary dla wartości pomiaru

7. **Unit do CustomDrug (per_weight_unit)**: Jeden-do-Wielu
   - Jedna jednostka miary może być używana dla wielu niestandardowych leków
   - Każdy niestandardowy lek używa dokładnie jednej jednostki miary dla wartości na wagę

8. **DrugInteraction do Drug**: Wiele-do-Wielu (przez DrugInteraction_Drugs)
   - Jeden rekord interakcji leków może obejmować wiele leków
   - Jeden lek może być zaangażowany w wiele rekordów interakcji leków

9. **User do UserSearchHistory**: Jeden-do-Wielu
   - Jeden użytkownik może mieć wiele rekordów historii wyszukiwania
   - Każdy rekord historii wyszukiwania należy dokładnie do jednego użytkownika

10. **User do SystemLog**: Jeden-do-Wielu (opcjonalnie)
    - Jeden użytkownik może być powiązany z wieloma logami systemowymi
    - Każdy log systemowy może być powiązany z jednym lub żadnym użytkownikiem (jeśli jest generowany przez system)

11. **ContentType do Rating**: Jeden-do-Wielu
    - Jeden typ zawartości może mieć wiele ocen
    - Każda ocena jest powiązana z dokładnie jednym typem zawartości

## 3. Indeksy

1. **Tabela User**:
   - Indeks na `email` (już obsługiwany przez ograniczenie UNIQUE)

2. **Tabela Drug**:
   - Indeks na `name` 
   - Indeks na `active_ingredient`

3. **Tabela CustomDrug**:
   - Indeks na `user_id`

4. **Tabela DrugInteraction**:
   - Indeks na `created_by`

5. **Tabela TreatmentGuide**:
   - Indeks GIN na `factors` dla wydajnych zapytań JSONB
   - Indeks na `created_by`

6. **Tabela Rating**:
   - Indeks na `content_type_id, object_id`
   - Indeks na `created_by`
   - Ograniczenie unique_together dla `created_by, content_type_id, object_id`

7. **Tabela SystemLog**:
   - Indeks na `timestamp`
   - Indeks na `source`
   - Indeks na `log_level`
   - Indeks na `user_id`

8. **Tabela UserSearchHistory**:
   - Indeks na `-created_at`
   - Indeks na `created_by, -created_at`
   - Indeks na `created_by, module, -created_at`
   - Indeks na `module`

## 4. Polityki bezpieczeństwa na poziomie wierszy PostgreSQL (RLS)

### Polityki RLS dla tabeli CustomDrug

```sql
ALTER TABLE "custom_drug" ENABLE ROW LEVEL SECURITY;

-- Policy that allows users to see only their own custom drugs
CREATE POLICY custom_drug_user_isolation ON "custom_drug"
    USING (user_id = current_user_id());
    
-- Policy that allows administrators to see all custom drugs
CREATE POLICY custom_drug_admin_access ON "custom_drug"
    USING (current_user_has_role('admin'));
```

### Polityki RLS dla tabeli UserSearchHistory

```sql
ALTER TABLE "user_search_history" ENABLE ROW LEVEL SECURITY;

-- Policy that allows users to see only their own search history
CREATE POLICY search_history_user_isolation ON "user_search_history"
    USING (created_by_id = current_user_id());
    
-- Policy that allows administrators to see all search history
CREATE POLICY search_history_admin_access ON "user_search_history"
    USING (current_user_has_role('admin'));
```

## 5. Dodatkowe uwagi i decyzje projektowe

1. **Pola audytowe**:
   - Większość tabel dziedziczy z BaseAuditModel, który zapewnia standardowe pola audytowe (created_at, updated_at, created_by)
   - SystemLog ma pole timestamp zamiast created_at, ponieważ jest to tabela logów

2. **System ocen (Rating)**:
   - Zastosowano generyczny system ocen oparty na ContentType Framework Django
   - Pozwala to na ocenianie różnych typów treści (interakcji leków, przewodników leczenia) przy użyciu jednej tabeli
   - Oceny są reprezentowane jako "up" lub "down" zamiast liczników w każdej tabeli

3. **Struktura modeli leków**:
   - Drug i CustomDrug dzielą wspólne pola dzięki bazie BaseDrugModel
   - Obie tabele zawierają zarówno measurement_unit jak i per_weight_unit dla obsługi różnych jednostek miary

4. **Długości pól tekstowych**:
   - Długości pól są ograniczone zgodnie z wymaganiami Django i specyfikacjami aplikacji
   - VARCHAR(20) dla większości pól nazw
   - VARCHAR(5) dla krótkich nazw jednostek
   - VARCHAR(100) dla dłuższych tekstów jak przeciwwskazania
   - TEXT dla nieograniczonych pól tekstowych jak wyniki zapytań i opisy

5. **Przechowywanie JSON**:
   - TreatmentGuide.factors używa JSONB do przechowywania ustrukturyzowanych danych o czynnikach diagnostycznych
   - JSONB jest preferowany nad JSON dla lepszej wydajności zapytań z indeksami GIN

6. **Historia wyszukiwania**:
   - Tabela UserSearchHistory przechowuje historię wyszukiwania użytkownika we wszystkich modułach
   - Wspiera to dostęp do poprzednich wyszukiwań i analizy użytkownika

7. **System bezpieczeństwa**:
   - Wykorzystanie mechanizmu ochrony na poziomie wierszy (RLS) PostgreSQL
   - Model użytkownika oparty na AbstractUser Django z email zamiast username jako identyfikatora
   - Bezpieczne przechowywanie haseł dzięki mechanizmom Django