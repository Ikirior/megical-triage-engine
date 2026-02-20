class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""
    pass

class DuplicateUserError(Exception):
    """Raised when trying to create a user with an existing email or CPF."""
    pass

class PatientNotFoundError(Exception):
    """Raised when a patient is not found in the database."""
    pass

class ReceptionistNotFoundError(Exception):
    """Raised when a receptionist is not found in the database."""
    pass

class MedicalRecordAlreadyExistsError(Exception):
    """Raised when trying to create a duplicate record."""
    pass

class DuplicatePatientError(Exception):
    """Raised when trying to create a duplicate record."""
    pass

class ServiceSheetNotFoundError(Exception):
    """Raised when a specific triage service sheet cannot be found."""
    pass

class NurseNotFoundError(Exception):
    """Raised when the nurse ID provided for triage does not exist."""
    pass

class InvalidTriageStateError(Exception):
    """Raised when attempting an operation not allowed by the current service sheet status."""
    pass

class IncompleteTriageDataError(Exception):
    """Raised when attempting to progress triage without requisite phase data."""
    pass

class DoctorNotFoundError(Exception):
    """Raised when a doctor is not found in the database."""
    pass

class InvalidConsultationStateError(Exception):
    """Raised when attempting an operation not allowed by the current consultation status."""
    pass

class UnauthorizedDoctorError(Exception):
    """Raised when a doctor attempts to modify a consultation assigned to another doctor."""
    pass