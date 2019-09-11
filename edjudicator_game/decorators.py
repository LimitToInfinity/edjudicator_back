from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        value = args[0].request.data.get("value", "")
        if not value:
            return Response(
                data={
                    "message": "High Score is required to add one, yo!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
