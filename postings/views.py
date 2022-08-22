import json
from django.views import View
from django.http import JsonResponse

from django.db.models import Q

from postings.models import Posting
from companies.models import Company

class ArticleView(View):
    def get(self, request):
        # 채용 공고 리스트로 가져오는 기능  OR 바로 검색 지원하는 기능
        try:
            keyword = request.GET.get("search", None)

            if keyword == None:
                postings = Posting.objects.all()
            else:
                postings = Posting.objects.filter(
                        Q(position__contains=keyword)|Q(skill__contains=keyword)
                    )
            
            postings = postings.select_related('company')

            posting_list = list()
            for posting in postings:

                posting_list.append(
                    {
                        "채용공고_id" : posting.id,
                        "회사명" : posting.company.name,
                        "국가" : posting.company.country,
                        "지역" : posting.company.city,
                        "채용포지션" : posting.position,
                        "채용보상금": posting.bounty,
                        "사용기술" : posting.skill
                    }
                )
            return JsonResponse({"postings" : posting_list}, status = 200)
        
        except Posting.DoesNotExist as notfound :
            return JsonResponse({"message" : "Not_Found"}, status = 404)
        
        except KeyError as ke:
            return JsonResponse({"message" : "Key_Error"}, status = 400)
        
        except Exception as e:
            return JsonResponse({"message" : "ServerError"}, status = 500)

    def post(self, request):
        try:
            data = json.loads(request.body)
            company_id = data["company_id"]
            position = data["position"]
            bounty = data["bounty"]
            content = data["content"]
            skill = data["skill"]

            company_ins = Company.objects.get(id=company_id)
            
            Posting.objects.create(
                company = company_ins,
                position = position,
                bounty = bounty,
                content = content,
                skill = skill
            )
            return JsonResponse({"message" : "Success"}, status = 201)
        except KeyError as ke:
            return JsonResponse({"message" : "Invalid_Key"}, status = 400)
        except json.JSONDecodeError as je:
            return JsonResponse({"message" : "Invalid_Request_Body"}, status = 500)
    
    def patch(self, request):
        try:
            data = json.loads(request.body)

            posting_id = data.get("id", None)
            if posting_id is None:
                raise KeyError
            
            update_items = {key:value for key, value in data.items() if value is not None}
           
            Posting.objects.filter(id=posting_id).update(**update_items)            
            return JsonResponse({"message" : "Success"}, status = 200)
        except KeyError as ke:
            return JsonResponse({"message" : "Invalid_Key"}, status = 400)
        except json.JSONDecodeError as je:
            return JsonResponse({"message" : "Invalid_Request_Body"}, status = 500)
   
    def delete(self, request, posting_id):
        try:
            if posting_id == None:
                raise Exception
            
            posting = Posting.objects.filter(id=posting_id)
            
            if len(posting) == 0:
                raise Posting.DoesNotExist

            posting.delete()

            return JsonResponse({"message" : "Success"}, status = 200)
        except Posting.DoesNotExist as nf :
            return JsonResponse({"message" : "Not_Found"}, status = 404)
        except Exception as e:
            return JsonResponse({"message" : "Invalid_Request"}, status = 500)

class ArticleDetailView(View):
    def get(self, request, posting_id):
        try:
            if posting_id == None:
                raise ValueError

            posting = Posting.objects.get(id = posting_id)
            other_employments = Posting.objects.filter( company_id = posting.company.id)

            response_data = {
                "채용공고_id" : posting.id,
                "회사명" : posting.company.name,
                "국가" : posting.company.country,
                "지역" : posting.company.city,
                "채용포지션" : posting.position,
                "채용보상금": posting.bounty,
                "사용기술" : posting.skill,
                "채용내용" : posting.content,
                "회사의 다른 공고" : [ employ.id for employ in other_employments if employ.id != posting_id] if len(other_employments) > 0 else []
            }
            return JsonResponse({"posting" : response_data }, status = 200)
        
        except KeyError as ke:
            return JsonResponse({"message" : "Key_Error"}, status = 400)
        except Posting.DoesNotExist as nf:
            return JsonResponse({"message" : "Not_Found"}, status = 404)
        except ValueError as ve:
            return JsonResponse({"message" : "Invalid_Request"}, status = 401)
        except TypeError as te:
            print(te)
            return JsonResponse({"message" : "Invalid_Data_Type"}, status = 500) 
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Server_Error"}, status = 500)