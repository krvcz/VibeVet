import { AxiosError } from 'axios';

export interface ApiError {
  code: string;
  message: string;
}

export interface ApiErrorResponse {
  error: ApiError;
}

export class AppError extends Error {
  public code: string;
  public statusCode?: number;

  constructor(message: string, code: string, statusCode?: number) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
    this.name = 'AppError';
  }
}

export function handleApiError(error: unknown): AppError {
  if (error instanceof AppError) {
    return error;
  }

  if (error instanceof AxiosError) {
    const response = error.response;
    
    if (response?.data?.error) {
      const apiError = response.data.error as ApiError;
      return new AppError(
        apiError.message,
        apiError.code,
        response.status
      );
    }

    // Handle network errors
    if (!response) {
      return new AppError(
        'Nie można połączyć się z serwerem. Sprawdź połączenie internetowe.',
        'NetworkError',
        0
      );
    }

    // Handle other HTTP errors
    return new AppError(
      error.message || 'Wystąpił nieoczekiwany błąd.',
      'HttpError',
      response.status
    );
  }

  // Handle unknown errors
  return new AppError(
    error instanceof Error ? error.message : 'Wystąpił nieoczekiwany błąd.',
    'UnknownError',
    500
  );
}

export function getErrorMessage(error: AppError): string {
  switch (error.code) {
    case 'ValidationError':
      return 'Nieprawidłowe dane. Sprawdź wprowadzone informacje.';
    case 'ObjectDoesNotExist':
    case 'NotFound':
      return 'Nie znaleziono żądanego zasobu.';
    case 'PermissionDenied':
      return 'Brak uprawnień do wykonania tej operacji.';
    case 'NotAuthenticated':
    case 'AuthenticationFailed':
      return 'Wymagane zalogowanie. Zaloguj się i spróbuj ponownie.';
    case 'MethodNotAllowed':
      return 'Ta operacja nie jest dozwolona.';
    case 'Throttled':
      return 'Zbyt wiele prób. Spróbuj ponownie później.';
    case 'ParseError':
      return 'Błąd przetwarzania danych. Sprawdź format wprowadzonych informacji.';
    case 'CustomDrugValidationError':
      return 'Błąd walidacji leku. Sprawdź wprowadzone dane.';
    case 'DrugInteractionValidationError':
      return 'Błąd walidacji interakcji leków. Sprawdź wybrane leki.';
    case 'TreatmentGuideValidationError':
      return 'Błąd walidacji poradnika leczenia. Sprawdź wprowadzone dane.';
    case 'TreatmentGuideProcessingError':
      return 'Błąd przetwarzania poradnika leczenia. Spróbuj ponownie później.';
    case 'RatingValidationError':
      return 'Błąd walidacji oceny. Sprawdź wprowadzone dane.';
    case 'DosageCalculationError':
      return 'Błąd obliczania dawki. Sprawdź wprowadzone dane.';
    case 'UnitConversionError':
      return 'Nie można przeliczyć jednostek. Wybierz inną jednostkę docelową.';
    case 'NetworkError':
      return 'Problem z połączeniem internetowym. Sprawdź połączenie i spróbuj ponownie.';
    case 'HttpError':
      return 'Błąd komunikacji z serwerem. Spróbuj ponownie później.';
    default:
      return error.message || 'Wystąpił nieoczekiwany błąd. Spróbuj ponownie później.';
  }
}