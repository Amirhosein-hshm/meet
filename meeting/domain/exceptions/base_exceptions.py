class BaseAppException(Exception):
    def __init__(self, message: str, error_code: str = "GENERIC_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class UnauthorizedRoleError(BaseAppException):
    def __init__(self, message: str = "برای انجام این عملیات دسترسی لازم را ندارید."):
        super().__init__(message=message, error_code="UNAUTHORIZED_ROLE")


class ForbiddenActionError(BaseAppException):
    def __init__(self, message: str = "امکان انجام این عملیات برای شما وجود ندارد."):
        super().__init__(message=message, error_code="FORBIDDEN_ACTION")


class RoleHierarchyViolationError(BaseAppException):
    def __init__(self, message: str = "به دلیل محدودیت سطح دسترسی، این عملیات قابل انجام نیست."):
        super().__init__(message=message, error_code="ROLE_HIERARCHY_VIOLATION")


class InvalidParticipantError(BaseAppException):
    def __init__(self, message: str = "اطلاعات شرکت‌کننده معتبر نیست."):
        super().__init__(message=message, error_code="INVALID_PARTICIPANT")


class ResourceNotFoundError(BaseAppException):
    def __init__(self, message: str = "مورد درخواستی پیدا نشد."):
        super().__init__(message=message, error_code="NOT_FOUND")


class ConflictError(BaseAppException):
    def __init__(self, message: str = "این عملیات با وضعیت فعلی داده‌ها سازگار نیست."):
        super().__init__(message=message, error_code="CONFLICT")
