class BaseAppException(Exception):
    def __init__(self, message: str, error_code: str = "GENERIC_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class UnauthorizedRoleError(BaseAppException):
    def __init__(self, message: str = "شما نقش مورد نیاز برای انجام این عملیات را ندارید."):
        super().__init__(message=message, error_code="UNAUTHORIZED_ROLE")


class ForbiddenActionError(BaseAppException):
    def __init__(self, message: str = "شما مجاز به انجام این عملیات نیستید."):
        super().__init__(message=message, error_code="FORBIDDEN_ACTION")


class RoleHierarchyViolationError(BaseAppException):
    def __init__(self, message: str = "به دلیل محدودیت‌های سلسله‌مراتب نقش‌ها نمی‌توان این عملیات را انجام داد."):
        super().__init__(message=message, error_code="ROLE_HIERARCHY_VIOLATION")


class InvalidParticipantError(BaseAppException):
    def __init__(self, message: str = "داده‌های شرکت‌کننده نامعتبر است."):
        super().__init__(message=message, error_code="INVALID_PARTICIPANT")


class ResourceNotFoundError(BaseAppException):
    def __init__(self, message: str = "منبع درخواستی یافت نشد."):
        super().__init__(message=message, error_code="NOT_FOUND")


class ConflictError(BaseAppException):
    def __init__(self, message: str = "تضاد با داده‌های موجود."):
        super().__init__(message=message, error_code="CONFLICT")
