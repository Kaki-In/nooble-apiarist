import enum as _enum
import typing as _T

RAW_ROLE = _T.Literal['student', 'admin', 'teacher', 'teacher_admin'] 

class Role(_enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    ADMIN_TEACHER = "teacher_admin"
    STUDENT = "student"

    @staticmethod
    def from_raw_role(role: RAW_ROLE) -> "Role":
        if role == "admin":
            return Role.ADMIN
        
        if role == "teacher":
            return Role.TEACHER
        
        if role == "teacher_admin":
            return Role.ADMIN_TEACHER
        
        if role == "student":
            return Role.STUDENT
        
        raise ValueError('invalid role given')
    
    def __str__(self) -> RAW_ROLE:
        return self.value
    
    def is_admin(self) -> bool:
        return self in (Role.ADMIN, Role.ADMIN_TEACHER)




