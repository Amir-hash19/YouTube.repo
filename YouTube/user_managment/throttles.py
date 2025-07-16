from rest_framework.throttling import AnonRateThrottle




class SignUpRateThrottle(AnonRateThrottle):
    scope = "signup"