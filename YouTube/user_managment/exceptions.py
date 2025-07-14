from django.utils.translation import gettext_lazy as _



class UserError(Exception):
    default_message = _("An unknown user error occurred!")
    default_code = "User_Error"


    def __init__(self, message=None, code=None, field=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.field = field
        super().__init__(self.message)


    def to_dict(self):
        return {
            "message":self.message,
            "code":self.code,
            "field":self.field
        }    

    def __str__(self):
        return f"{self.code}: {self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__} code = {self.code} message = {self.message}"    
    




class MissingEmailError(UserError):
    default_message = "Email is required."
    default_code = "missing_email"


    def __init__(self, message=None, field="email"):
        super().__init__(message=message, code=self.default_code, field=field)





class EmailAlreadyExistsError(UserError):
    default_message = "A user with this email already exists."
    default_code = "email_exists."

    def __init__(self, message=None, field=None):
        super().__init__(message=message, code=self.default_code, field=field)




class InvalidGenderError(UserError):
    default_message = "Gender must be 'male' or 'female'."
    default_code = "Invalid_gender"


    def __init__(self, message=None, field="gender"):
        super().__init__(message=message, code=self.default_code, field=field)



class MissingUsernameError(UserError):
    default_message = "username is Requied."
    default_code = "missing_email"

    def __init__(self, message=None, field=None):
        super().__init__(message=message, code=self.default_code, field=field)



class UsernameAlreadyExistsError(UserError):
    default_message = "username is already exists."
    default_code = "username_exists."

    def __init__(self, message=None, field=None):
        super().__init__(message=message, code=self.default_code, field=field)




class WeakPasswordError(UserError):
    default_message = "password is not strong enough!."
    default_code = "weakpassword_error."

    def __init__(self, message=None, field=None):
        super().__init__(message=message, code=self.default_code, field=field)    
