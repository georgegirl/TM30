from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Cart
from .serializers import CategorySerializer,ProductSerializer, CartSerializer, UserProductSerializer, CRequestSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.permissions import IsAdmin, IsUser
from account.models import User
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes

# Create your views here.

class CategoryView(APIView):
    """This Method Retrives and Post a category Instance"""

    authentication_classes = [JWTAuthentication] #a given authentication scheme
    permission_classes = [IsAdmin]
    def get(self, request, format=None):
        obj= Category.objects.all()
        serializer = CategorySerializer(obj, many=True)

        data= {
            'message': 'success',
            'data_count': obj.count(),
            'data': serializer.data,

        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method="post", request_body= CategorySerializer())
    @action(methods=["POST"], detail= True)
    def post(self, request, Format=None):
        """This method is used to create a new category instance"""

        serializer= CategorySerializer(data=request.data)#this gets the data and deserializes it

        if serializer.is_valid():
            serializer.save()
            data={
                "message": "Category Created"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data={
                "message": "Failed to Create",
                "error": serializer.errors,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    """This Method Retrives category instances, Updates category instance and Delete category instance."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin, IsUser]
    def get_object(self, category_id):
        """This method returns a single instance using the category_id(identification)"""
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
         raise NotFound(detail={
                "message": "Category does not exist"
        })
        
    def get(self, request, category_id, format=None):
        objs = self.get_object(category_id)
        serializer= CategorySerializer(objs)


        data={
            "message": "Data fetched successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method="put", request_body= CategorySerializer())
    @action(methods=["PUT"], detail= True)
    def put(self, request, category_id, format=None):
        """This Method enables the admin to change the resource data. it acts as a put and patch method that is the admin could change a single profiling in the data or the whole data"""

        if request.user.is_active == True:
            obj= self.get_object(category_id)
            serializer= CategorySerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()


                data= {
                    "message": "Success"

                }
                return Response (data, status=status.HTTP_201_CREATED)
            else:
                data ={
                    "message": "failed",
                    "error": serializer.errors
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method="delete")
    @action(methods=["DELETE"], detail= True)
    def delete(self, request, category_id, format=None):
        """This method delets a specified category that has no available item within its category"""
        # if User.is_IsAdmin]:
        if request.user.is_active == True:
            obj = self.get_object(category_id)

            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied(detail={"message": "Permission denied"})

class ProductView(APIView):
    """This method Retrives, Deletes and Updates a Product instance"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser, IsAdmin ]

    def get(self, request, format=None):
        

        obj= Product.objects.all()
        serializer = ProductSerializer(obj, many=True)

        data= {
            'message': 'Available Products',
            'data_count': obj.count(),
            'data': serializer.data,

        }
        return Response(data, status=status.HTTP_200_OK)
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin ]
    @swagger_auto_schema(method="post", request_body=ProductSerializer())
    @action(methods=["POST"], detail= True)
    def post(self, request, format=None):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            data= {
                "message": "Success"
            }
            return Response(data, status=status.HTTP_201_CREATED)

        else:

            data= {
       
                "message": "failed",
                "error": serializer.errors,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    """This Method Retrive, Updates and Delete Products"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin, IsUser]
    def get_object(self, product_id):

        try:
            return Product.objects.get(id=product_id) 
        except Product.DoesNotExist:
            raise NotFound(DETAIL={
                "message": "Product not found"
            })

    def get(self, request, product_id, format=None):
            obj= self.get_object(product_id)
            serializer= ProductSerializer(obj)

            data ={
            "message": "success",
            "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method="put", request_body= ProductSerializer())
    @action(methods=["PUT"], detail= True)
    def put(self,request, product_id, format=None):
        obj= self.get_object(product_id)
        serializer= ProductSerializer(obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()

            data={
                "message": "Success"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data={
                "message": "failed",
                "error": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method="delete")
    @action(methods=["DELETE"], detail= True)
    def delete(self, request, product_id, format=None):
        """Deletes an existing item from the database.
           It is only accessible by the admin .
        """
        if request.user.is_staff and request.user.is_active == True: #makes it delete all unavailable
            obj=  self.get_object(product_id)
            if obj.status == "unavailabe":
                obj.delete()

                data={
                    "message": "Product deleted successfully"
                }
                return Response(data,status=status.HTTP_204_NO_CONTENT)
                
            raise PermissionDenied(detail={"message": "Permission denied"})

class CartView(APIView):
    '''This method provides info on a cart of a user '''
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsUser]
    def get(self, request, format=None):

        '''This method returns a authenticated users Cart'''
        if request.user in User.objects.all():
            own_id = request.user.id
            ojs = User.objects.get(id=own_id)
            obj = ojs.now.all()
            print(obj)
            serializer = CartSerializer(obj, many=True)

            data= {
                "message": "success",
                "data": serializer.data
            } 
            return Response(data, status=status.HTTP_200_OK)


    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin, IsUser]
    @swagger_auto_schema(method='post', request_body=CRequestSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """
        Adds items to the cart of a user in the database to the cart model only if the  
        item quantity available in the database is greater than quantity demanded.
        """  
        data = {}
        data1=request.data
        data['Items'] = data1['Items']
        data['quantity'] = data1['quantity']
        data['owner'] = request.user.id
        try:
            carts = Product.objects.get(id=data['Items'])          
            cart_p = carts.price
            data['price'] = data['quantity'] * cart_p
            data['status'] = 'True'

            if request.user in User.objects.all():
                
                if data['quantity'] > carts.Stock:
                    return Response(data={'message': 'Products Ordered is currently out of stock'}, status=status.HTTP_403_FORBIDDEN)

                else:
                    carts.Stock -= data['quantity'] 
                    carts.save()
                    serializer = CartSerializer(data=data)
                    
                    if serializer.is_valid():
                        serializer.save()
                        
                        data = {
                            "message":"item successfully added to cart",
                        }

                        return Response(data, status = status.HTTP_200_OK)

                    else:
                        data = {
                            "message":"failed",
                            "error":serializer.errors
                        }
                    
                    return Response(data, status = status.HTTP_400_BAD_REQUEST)

            else:
                raise PermissionDenied(detail={'message': 'AnonymousUser are forbidden to perform this action.'})

        except Product.DoesNotExist:
            raise NotFound(detail={'message': 'Item with id does not exist'})
    
    
class CartDetailView(APIView):
    """"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin, IsUser]
    def get_object(self, item_id):
        """this Method Retrives the object(Cart) from the database using a given identification 'item-id'"""

        try:
            return Cart.objects.get(id=item_id)
        except Cart.DoesNotExist:
            raise Response(data={'error': 'Cart does not exist'})


    @swagger_auto_schema(method='delete')
    @action(methods=['DELETE'], detail=True)
    def delete(self, request, item_id, format=None):
        """Delete a single item in a cart belonging to a logged in user.
           when a pending cart item is deleted the quantity is added to the quantity of the item model.
        """
        try:
            cus_id = request.user.id
            confirm = User.objects.get(id=cus_id)

            
            if request.user == confirm and request.user in User.objects.all():
                obj = self.get_object(item_id=item_id)
                try: 
                    p= Product.objects.get(Items=obj)
                    p.Stock += obj.quantity
                    p.save()
                
                    obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except Cart.DoesNotExist:
                    raise NotFound(detail={'message': 'Cart does not exist'})

            else:
                raise PermissionDenied(detail={'message': 'Not Your Cart.'})
            
        except User.DoesNotExist:
            raise NotFound(detail={'message': 'User Not Confirmed.'})



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsUser])
def shopping_status(request, item_id):
    """Allows User to change the status of a cart, if done shopping"""
    
    if request.method == 'GET':
        try:
            shop = Cart.objects.get(id= item_id, Done_shopping ="False")
            shop.status = 'True'
            shop.save()
       
            return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"error":"Cart not found","message":"failed"}, status=status.HTTP_404_NOT_FOUND)


