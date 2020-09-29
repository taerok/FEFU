from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import User, ProductInfo, MainCategoryInfo, MediumCategoryInfo, SubCategoryInfo, PurchaseDetails, ViewDetails
from .serializers import ProductSerializer, PurchaseDetailsSerializer, ViewDetailsSerializer, ProductDetailSerializer

from datetime import date


# Create your views here.

# The actions provided by the ModelViewSet class are 
# .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().

class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.order_by("-pk")
    serializer_class = ProductSerializer

    #create category json
    category_group = dict()
    main_categories = MainCategoryInfo.objects.all()
    medium_categories = MediumCategoryInfo.objects.all()
    sub_categories = SubCategoryInfo.objects.all()

    for main_cat in main_categories:
        category_group[(main_cat.main_category_name, main_cat.no)] = dict()
    for med_cat in medium_categories:        
        category_group[(med_cat.main_category_no.main_category_name, med_cat.main_category_no.no)][(med_cat.medium_category_name, med_cat.no)] = []
    for sub_cat in sub_categories:        
        main_name = sub_cat.medium_category_no.main_category_no.main_category_name
        main_no = sub_cat.medium_category_no.main_category_no.no
        med_name = sub_cat.medium_category_no.medium_category_name
        med_no = sub_cat.medium_category_no.no
        category_group[(main_name, main_no)][(med_name, med_no)].append((sub_cat.sub_category_name, sub_cat.no))

    # general view override -----------------------------------------------------------


    # 전체 상품 목록 / 검색
    def list(self, request, *args, **kwargs):
        main_category = request.GET.get('mainCategory',None)
        medium_category = request.GET.get('mediumCategory', None)
        search_word = request.GET.get('content', None)
        curPage = request.GET.get('pageNum', 1)
        
        products = self.queryset

        if main_category:
            products = products.filter(main_category_no=main_category)
            if medium_category:
                products = products.filter(medium_category_no=medium_category)
        if search_word:

            products = products.filter(title__icontains=search_word)

        perPageNum = 12 #페이지 당 글 수
        paginator = Paginator(products, perPageNum)
        totalCount = paginator.count # 글 개수
        
        curPage_products = paginator.get_page(curPage) #curPage의 글 목록
        startPage = 1 #시작 페이지
        endPage = paginator.num_pages #총 페이지 수
        prev_bool = curPage_products.has_previous()
        next_bool = curPage_products.has_next()
        startIndex = curPage_products.start_index()
        serializer = self.serializer_class(curPage_products, many=True)
        page = {"curPage":curPage, "perPageNum":perPageNum, "totalCount":totalCount, "startPage":startPage, "endPage":endPage, "prev":prev_bool, "next":next_bool, "startIndex":startIndex}
        return Response({"page":page, "list": serializer.data}, status=200)
    
    #상품 상세 정보 가져오기
    def retrieve(self, request, pk):
        product = self.queryset.get(no=pk)
        product_detail = ProductDetailSerializer(product)
        return Response(product_detail.data, status=200)




    #상품 등록
    def create(self, request, *args, **kwargs):
        #로그인된 사용자일 경우에만
        username = request.META["HTTP_X_USERNAME"]
        if username != 'anonymousUser':
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid(raise_exception=True):
                
                serializer.save()
                return Response("resource created successfully", status=201)
        else:
            return Response("unauthorized user", status=401)

    #상품 수정
    def patch(self, request, *args, **kwargs):
        # 나 == 글작성자
        username = request.META["HTTP_X_USERNAME"]
        writer = request.data["writer"]
        product_no = request.data["product_no"]
        if username == writer:
            kwargs['partial'] = True
            partial = kwargs.pop('partial', False)
            instance = get_object_or_404(ProductInfo, pk=product_no)
            serializer = self.serializer_class(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("resource updated successfully", status=200)
        else:
            return Response("forbidden user", status=403)

    #상품 삭제
    def destroy(self, request, pk):
        username = request.META["HTTP_X_USERNAME"]
        instance = get_object_or_404(ProductInfo, no=pk)
        writer = instance.writer.username
        pk = pk
        if username == writer:
            instance.delete()
            return Response("resource deleted successfully", status=204)
        else:
            return Response("forbidden user", status=403)
    

    
    # custom functions -----------------------------------------------------------------
    @action(detail=False)
    def get_latest_products(self, reqeust):
        latest_queryset = self.queryset[:3]
        serialzier = self.serializer_class(latest_queryset, many=True)
        return Response(serialzier.data, status=200)

    
    @action(detail=True, methods=["POST"] )
    def viewed(self, request, pk=None):
        username = request.META["HTTP_X_USERNAME"]
        # product_no = request.data["product_no"]
        product_no = pk
        sub_category_no = request.data["sub_category_no"]
        # print(product_no, sub_category_no)
        today = date.today()
        serializer = ViewDetailsSerializer(data={"user":username, "product_no":product_no, "sub_category_no":sub_category_no, "reg_time":today})
        if serializer.is_valid(raise_exception=True):
            today_viewed_products = ViewDetails.objects.filter(reg_time__date=today)

            if not today_viewed_products.filter(user=username, product_no=product_no, sub_category_no=sub_category_no).exists():
                serializer.save()
                return Response("resource created successfully", status=201)
            return Response("resource already created", status=200)
    
    @action(detail=False)
    def top_three_viewed_today(self, request):
        today = date.today()
        today_viewed_products = ViewDetails.objects.filter(reg_time__date=today) # 오늘 조회
        queryset = today_viewed_products.values('product_no_id').annotate(count=Count('product_no_id')).values('product_no_id')
        queryset = queryset.order_by("-count")
        queryset = queryset[:3]
        top_product_ids = []
        
        for q in queryset:
            top_product_ids.append(q["product_no_id"])
        
        top_products = ProductInfo.objects.filter(no__in=top_product_ids)
        serializer = self.serializer_class(top_products, many=True)
        return Response(serializer.data, status=200)



        



    @action(detail=False)
    def recommendation(self, request):
        # 상품 추천 로직
        # 추천 상품 목록 리턴
        pass
    
    @action(methods=["PATCH"], detail=True)
    def sold(self, request, pk):
        # 요청 보내는 사람과 판매글 작성자가 같은지 확인
        username = request.META["HTTP_X_USERNAME"]
        # username = request.data["username"]
        buyer = request.data["buyer"]
        product = self.queryset.get(pk=pk)
        seller = product.writer.username
        status = product.status


        if username == seller:
            if status == 1: #팔 -> 안팔
                product_serializer = ProductSerializer(product, data={"status": 0}, partial=True)
                # purchase_detail = PurchaseDetails.objects.get(product_no=pk)
                # purchase_detail.delete()

            else: # 안팔 -> 팔
                product_serializer = ProductSerializer(product, data={"status": 1}, partial=True)
                # purchase_serializer = PurchaseDetailsSerializer(data={"seller": seller, "buyer": buyer, "product_no": pk})
                # purchase_serializer.is_valid(raise_exception=True)
                # if purchase_serializer.is_valid():
                #     purchase_serializer.save()
                

            if product_serializer.is_valid():
                product_serializer.save()
                return Response("resource updated successfully", status=200)
        
        return Response("forbidden user", status=403)



    @action(detail=False)
    def categories(self, request):
        
        return Response(self.category_group, status=200)
        
        
class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = PurchaseDetails.objects.all()
    serializer_class = PurchaseDetailsSerializer
    # print("=================purchase")


    def create(self, request, *args, **kwargs):
        username = request.META["HTTP_X_USERNAME"]
        product_no = request.data["product_no"]
        buyer = request.data["buyer"]
        product = ProductInfo.objects.get(no=product_no)
        seller = product.writer.username
        
        if username == seller:
            serializer = self.serializer_class(data={"seller":seller, "buyer":buyer, "product_no":product_no})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response("resource created successfully", status=201)
        else:
            return Response("forbidden user", status=403)
    
    def destroy(self, request, pk):
        username = request.META["HTTP_X_USERNAME"]
        seller = request.data["seller"]
        if username == seller:
            instance = get_object_or_404(PurchaseDetails, no=pk)
            instance.delete()
            return Response("resource deleted successfully", status=204)
        else:
            return Response("forbidden user", status=403)




    

    

