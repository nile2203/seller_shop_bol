from shipments.helpers.result_builder import ResultBuilder


def validate_user(function):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.auth:
            return function(request, *args, **kwargs)
        else:
            result_builder = ResultBuilder()
            result_builder.user_unauthorized_401().fail()

            return result_builder.get_response()

    return _wrapped_view_func
