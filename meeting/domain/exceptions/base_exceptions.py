class BaseAppException(Exception):
    def __init__(self, message: str, error_code: str = "GENERIC_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class UnauthorizedRoleError(BaseAppException):
    def __init__(self, message: str = "You do not have the required role to perform this action."):
        super().__init__(message=message, error_code="UNAUTHORIZED_ROLE")


class ForbiddenActionError(BaseAppException):
    def __init__(self, message: str = "You are not allowed to perform this action."):
        super().__init__(message=message, error_code="FORBIDDEN_ACTION")


class RoleHierarchyViolationError(BaseAppException):
    def __init__(self, message: str = "Cannot perform this action due to role hierarchy restrictions."):
        super().__init__(message=message, error_code="ROLE_HIERARCHY_VIOLATION")


class InvalidParticipantError(BaseAppException):
    def __init__(self, message: str = "Invalid participant data provided."):
        super().__init__(message=message, error_code="INVALID_PARTICIPANT")


class ResourceNotFoundError(BaseAppException):
    def __init__(self, message: str = "The requested resource was not found."):
        super().__init__(message=message, error_code="NOT_FOUND")


class ConflictError(BaseAppException):
    def __init__(self, message: str = "Conflict with existing data."):
        super().__init__(message=message, error_code="CONFLICT")


class UserBannedError(BaseAppException):
    def __init__(self, message: str = "You have been banned from this meeting."):
        super().__init__(message=message, error_code="FORBIDDEN_ACTION")
