/* 
  DTO and Command Model definitions for VibeVetAI API based on the database models and API plan.
  Each interface corresponds to one or more Django models and reflects the structure required by the API.
*/

/* ============================= */
/* ======= BASE DTOs ========== */
/* ============================= */

export interface BaseAuditDTO {
    created_at: string; // ISO datetime
    updated_at: string; // ISO datetime
    created_by: number; // User ID
}

export interface SpeciesDTO extends BaseAuditDTO {
    id: number;
    name: string;
    scientific_name: string;
    description: string | null;
}

export interface MeasurementUnitDTO extends BaseAuditDTO {
    id: number;
    name: string;
    symbol: string;
    description: string | null;
}

/* ============================= */
/* ========= DRUG DTOs ========= */
/* ============================= */

export interface DrugDTO extends BaseAuditDTO {
    id: number;
    name: string;
    active_ingredient: string;
    species: SpeciesDTO;
    contraindications: string | null;
    measurement_value: number;
    measurement_target: MeasurementUnitDTO;
}

export interface PaginationDTO {
    page: number;
    limit: number;
    total: number;
}

export interface DrugsListResponseDTO {
    results: DrugDTO[];
    pagination: PaginationDTO;
}

/* ================================ */
/* ===== CUSTOM DRUG MODELS ======== */
/* ================================ */

export interface CustomDrugDTO extends DrugDTO {
    user: number; // User ID who created the custom drug
}

export interface CreateCustomDrugCommand {
    name: string;
    active_ingredient: string;
    species: number;
    contraindications?: string;
    measurement_value: number;
    measurement_target: number;
}

export type UpdateCustomDrugCommand = Partial<CreateCustomDrugCommand>;

/* =================================== */
/* ===== DRUG INTERACTION MODELS ===== */
/* =================================== */

export interface DrugInteractionDTO extends BaseAuditDTO {
    id: number;
    query: string;
    result: string;
    context: string | null;
    positive_rating: number;
    negative_rating: number;
    drugs: DrugDTO[];
}

export interface CreateDrugInteractionCommand {
    drug_ids: number[];
    context?: string;
}

export interface RatingCommand {
    rating: 'up' | 'down';
}

/* ================================== */
/* ===== DOSAGE CALCULATOR MODELS ==== */
/* ================================== */

export interface CalculateDosageCommand {
    drug_id: number;
    weight: number; // Positive integer up to 3 digits expected
    species: number;
    target_unit: number;
}

export interface DosageCalcResultDTO {
    drug_id: number;
    calculated_dose: number; // Changed from string to number
    unit: MeasurementUnitDTO; // Changed from string to full object
}

/* =================================== */
/* ===== TREATMENT GUIDE MODELS ====== */
/* =================================== */

export interface DiagnosisFactors {
    temperature: number;
    heart_rate: number;
    blood_pressure: string;
    weight: number;
    age: number;
    species: number;
    calcium: number | null;
    glucose: number | null;
    potassium: number | null;
    hemoglobin: number | null;
    platelets: number | null;
    respiratory_rate: number;
    oxygen_saturation: number;
    additional_notes?: string;
}

export interface TreatmentGuideDTO extends BaseAuditDTO {
    id: number;
    query: string;
    result: string;
    factors: DiagnosisFactors;
    positive_rating: number;
    negative_rating: number;
}

export interface CreateTreatmentGuideCommand {
    factors: DiagnosisFactors;
}

/* ====================================== */
/* ===== USER SEARCH HISTORY MODELS ===== */
/* ====================================== */

export interface UserSearchHistoryDTO extends BaseAuditDTO {
    id: number;
    module: string;
    query: string;
}

export interface SearchHistoryResponseDTO {
    results: UserSearchHistoryDTO[];
    pagination: PaginationDTO;
}

/* ====================================== */
/* =========== SYSTEM LOG =============== */
/* ====================================== */

export interface SystemLogDTO {
    id: number;
    timestamp: string; // ISO datetime
    log_level: string;
    message: string;
    source: string;
    user: number | null; // User ID, optional
}

/* ====================================== */
/* ============= RATING ================= */
/* ====================================== */

export interface RatingDTO extends BaseAuditDTO {
    id: number;
    content_type: string;
    object_id: number;
    rating: 'up' | 'down';
}