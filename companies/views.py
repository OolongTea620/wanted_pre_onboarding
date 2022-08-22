import json
from django.views import View
from django.http import JsonResponse

from companies.models import Company
class CompanyView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            insert_items = {key:value for key, value in data.items()}

            Company.objects.create(**insert_items)
            return JsonResponse({"message" : "Success"}, status = 201) 
        except Exception as e:
            return JsonResponse({"message" : "Server_Error"},status = 500)
    
    def get(self, request):
        """
            데이처 조회용 (임시)
        """
        companies = Company.objects.all()
        return JsonResponse({"list" : [{ "name" : company.name, "country" : company.country, "city" : company.city}for company in companies]}, status = 200)