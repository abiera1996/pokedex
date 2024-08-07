from rest_framework import serializers 


class PokemonDetailsResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default=None,)
    data = serializers.JSONField(
        default=  {
            "id": 555,
            "abilities": [
            {
                "id": 3,
                "name": "blaze"
            },
            {
                "id": 4,
                "name": "solar-power"
            }
            ],
            "types": [
            {
                "id": 3,
                "name": "fire"
            }
            ],
            "name": "charmeleon",
            "default_photo": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/5.gif",
            "photo": None,
            "height": 11,
            "weight": 190
        }
    ) 


class PokemonDetailsNotFoundResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default='No Pokemon matches the given query.',)
    data = serializers.JSONField(
        default=  {}
    )  

    
class PokemonListResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default="")
    data = serializers.JSONField(
        default=   {
            "current_page": 1,
            "limit": 1,
            "total_page": 152,
            "count": 152,
            "results": [
            {
                "id": 551,
                "name": "bulbasaur",
                "default_photo": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/1.gif",
                "photo": None,
                "height": 7,
                "weight": 69,
                "types": [
                1,
                2
                ],
                "abilities": [
                1,
                2
                ]
            }
            ],
            "page_details": {
            "limit": 1,
            "record_count": 152,
            "page_count": 152,
            "record_from": 1,
            "record_to": 1,
            "pages": [
                1,
                2,
                3
            ],
            "page": 1,
            "has_next": True,
            "has_prev": False,
            "prev": None,
            "next": 1
            } 
        }
    ) 

class ErrorFieldSerializer(serializers.Serializer):
    message = serializers.CharField(default="")
    data = serializers.JSONField(
        default=  {
        "error_fields": [
            "email",
            "avatar"
        ],
        "complete_error": {
            "email": [
                "user with this email already exists."
            ],
            "avatar": [
                "The submitted data was not a file. Check the encoding type on the form."
            ]
        }
    }
    ) 


class PokemonCreateReponseSerializer(serializers.Serializer):
    message = serializers.CharField(default="Pokemon successfully added.")
    data = serializers.JSONField(
        default=  {}
    ) 


class PokemonUpdateReponseSerializer(serializers.Serializer):
    message = serializers.CharField(default="Pokemon successfully updated.")
    data = serializers.JSONField(
        default=  {}
    ) 


class PokemonDeleteReponseSerializer(serializers.Serializer):
    message = serializers.CharField(default="Pokemon successfully deleted.")
    data = serializers.JSONField(
        default=  {}
    ) 


class AuthenticationErrorSerializer(serializers.Serializer):
    message = serializers.CharField(default="Authentication credentials were not provided.")
    data = serializers.JSONField(
        default=  {}
    ) 

class ErrorFieldAccountVerificationSerializer(serializers.Serializer):
    message = serializers.CharField(default="")
    data = serializers.JSONField(
        default=  {
        "error_fields": [
                "code"
            ],
            "complete_error": {
                "code": [
                    "Invalid code verification."
                ]
            }
        }
        
    ) 


class AccountVerificationSuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default="Account successfully onboarded. Please check your email for account verification.",)
    data = serializers.JSONField(
        default=  {
                "success": True,
                "id": 8,
                "avatar": None,
                "first_name": "Dhaibert",
                "last_name": "Abiera",
                "email": "dhaibertabiera+va@gmail.com",
                "date_joined": "2024-07-04 16:11:11",
                "role": 2,
                "virtual_assistant": {
                    "id": 6, 
                    "phone_country_code": "63",
                    "phone_number": "9168344885",
                    "is_premium": True,
                    "social_media_link": "",
                    "user": 8,
                    "interest": [
                        1
                    ]
                },
                "token": {
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMDE5NjUzNywiaWF0IjoxNzIwMTEwMTM3LCJqdGkiOiJmNDNmOWQyZDYwNmM0YmE2OTQwMmVmODBiMmJhNTU2MyIsInVzZXJfaWQiOjh9.8a3T8xjKBVrdczAgDP-SxAayVfZYqAALgchPcbOrAyk",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMzY5MzM3LCJpYXQiOjE3MjAxMTAxMzcsImp0aSI6ImQ5NjMzOWYxYmJkOTRhNjZhYmNlNDU3YjJjZjVhMmIwIiwidXNlcl9pZCI6OH0.Zu5EkNiPH1ddC-117gs43p8iHrdTyyVIE2wYzwWRkyQ"
                }
            } 
    )
    code = serializers.CharField(default="OTP-S1")

 
class InterestListSuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default=None)
    data = serializers.JSONField(
        default=  {
                "current_page": 1,
                "limit": 2,
                "total_page": 2,
                "count": 3,
                "results": [
                {
                    "id": 1,
                    "name": "Soccer Game",
                    "date_created": "2024-07-04 16:05:30",
                    "created_by": None
                },
                {
                    "id": 2,
                    "name": "Software Development",
                    "date_created": "2024-07-04 16:05:30",
                    "created_by": None
                }
                ],
                "page_details": {
                "limit": 2,
                "record_count": 3,
                "page_count": 2,
                "record_from": 1,
                "record_to": 2,
                "pages": [
                    1,
                    2
                ],
                "page": 1,
                "has_next": True,
                "has_prev": False,
                "prev": None,
                "next": 2
                }
            } 
    )
    code = serializers.CharField(default="OTP-S1")

 