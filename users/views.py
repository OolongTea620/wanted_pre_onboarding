import json
from django.views import View
from django.http import JsonResponse

from users.models import User
from postings.models import Posting

from django.db.utils import IntegrityError

class SignInView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            items = { key:value for key, value in data.items()}
            
            User.objects.create(name = items["name"] , email=items["email"])

            return JsonResponse({"message" : "Add_User"}, status = 201)
        
        except KeyError as ke:
            return JsonResponse({"message" : "Key_Error"}, status = 400)
        
        except IntegrityError as ve:
            return JsonResponse({"message" : "email_invalid"}, status = 400)
        
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Server_Error"}, status = 500)

    
    def get(self, request):
        """
            Users 데이터 조회용(데이터 확인용)
        """
        users = User.objects.all()
        users_info = [{
            "name" : user.name,
            "eamil" : user.email,
            "id" :user.id,
            "apply" : user.posting.id if user.posting is not None else None
        }for user in users]
        return JsonResponse({"users" : users_info}, status = 400)

class UserApplyView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            items = { key:value for key, value in data.items()}
            
            user = User.objects.filter( id = items["user_id"] )
            user_get = user.get()
            if  user_get.posting is not None:
                return JsonResponse({"message" : "Already_Apply"}, status = 403)
            
            user.update(
                posting = items["posting_id"]
            )
            return JsonResponse({"message" : "Apply_success"}, status = 201)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message" : str(ke)}, status = 400)    
        
        except User.DoesNotExist as nu:
            return JsonResponse({"message" : str(nu)}, status = 403)
        
        except Posting.DoesNotExist as np:
            print(np)
            return JsonResponse({"message" : str(np)}, status = 403)
        
        except IntegrityError as ie:
            return JsonResponse({"message" : "Invalid user or posting index"}, status = 403)
        
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Server_Error", "detail" : str(e)}, status = 500)