class AdvApi(APIView):

    def get(self, request):
        try:
            print("HERE cnjsacnkSL")
            size = request.GET['size']
            temp_key = request.GET['temp_key']
            advertisementapi = AdvanceAdvertAPI(request, temp_key, size)
            advertisement_html = advertisementapi.get_advertisement()
            print('get request was made')
            return JsonResponse({'advert': advertisement_html}, safe=False)
        except Exception as e:
            return JsonResponse("The Advertisement could not be displayed", safe=False)
    
    def post(self, request):
        try:
            user_key = request.data['key']
            try:
                a = AdvanceKeyAPI(user_key)
                temp_key = a.get_temporary_key()
                res = {'temporary-key': temp_key}
                return JsonResponse(res, safe=False)
            except Exception as e:
                print("Here")
                raise e
        except Exception as e:
            print(e)
            return JsonResponse("The temporary Key could not be generated", safe=False)


