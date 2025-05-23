from django.http import JsonResponse
import random
import string

class PromoCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/api/promo-code/':
            saved_promo_code = request.COOKIES.get('promo_code', None)
            print(f"Saved promo code in cookie: {saved_promo_code}")

            if not saved_promo_code:
                promo_code = self.generate_promo_code()
                response = JsonResponse({'promo_code': promo_code})
                response.set_cookie('promo_code', promo_code, max_age=30*24*60*60, samesite='Lax', secure=False)
            else:
                response = JsonResponse({'promo_code': saved_promo_code})

            return response

        return self.get_response(request)

    def generate_promo_code(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))