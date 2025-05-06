import random
import string


class PromoCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('visited_before'):
            promo_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            request.session['promo_code'] = promo_code
            request.session['visited_before'] = True
            print(promo_code)
        response = self.get_response(request)
        return response