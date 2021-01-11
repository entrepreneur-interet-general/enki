from marshmallow.exceptions import ValidationError

errors = {
    ValidationError: {
        'message': "Validation Error",
        'status': 123,
    },
}