from rest_framework.throttling import AnonRateThrottle




class SignUpRateThrottle(AnonRateThrottle):
    scope = "signup"



class LoginRateThrottle(AnonRateThrottle):
    scope = "login"



class CreateChannelThrottle(AnonRateThrottle):
    scope = "channel"