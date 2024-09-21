from django.shortcuts import render
from rest_framework import generics, permissions
from .models import ProductOrder, ServiceOrder
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.error_handle import error_handler
from utils.qr_code import generate_qr_code
from provider_details.models import *
from django.db.models import Sum
from django.db.models import Sum
from decimal import Decimal
from rest_framework.exceptions import NotFound
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.utils.translation import gettext_lazy as _
from utils.notifications import NotificationsHelper,OrdersUpdates
######Product Order Views
class ProductOrderFollow(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            product_order = ProductOrder.objects.get(pk=pk)
        except ProductOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        return Response ({'id':product_order.id,'status':product_order.status,'date':product_order.date,'store_id':product_order.product.store.id})



class ProductOrderListView(generics.ListAPIView):
    serializer_class = ProductOrderBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer=Customer.objects.get(phone=self.request.user.phone)
        
        return ProductOrder.objects.filter(customer=customer)
    
class ProductOrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProductOrderSerializer(data=request.data)
        if serializer.is_valid():
            customer = Customer.objects.get(phone=request.user.phone)
            product=Product.objects.get(id=request.data['product'])
            if product.quantity < request.data['quantity']:
                return Response({'error': _('Quantity is not enough')}, status=status.HTTP_409_CONFLICT)
            product.quantity-=request.data['quantity']
            product.save()
            serializer.save(customer=customer,status=Status.UNCHECKED,product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
class ProductOrderDetails(APIView):
    def post(self, request, pk):
        try:
            product_order = ProductOrder.objects.get(pk=pk)
        except ProductOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        coupon_code=request.data['coupon_code']
        try:
            coupon=Coupon.objects.get(code=coupon_code)
            if coupon.is_expired():
                 return Response({'error': _('Coupon  is expired.')}, status=status.HTTP_303_SEE_OTHER)
            
        except Coupon.DoesNotExist:
            return Response({'error': _('Coupon  not found.')}, status=status.HTTP_404_NOT_FOUND)
        if product_order.coupon:
            return Response({'error': _('There is coupon already.')}, status=status.HTTP_303_SEE_OTHER)
        product_order.coupon=coupon
        product_order.save()
        return Response({'coupon_value':coupon.value},status=status.HTTP_200_OK)
    
    def get(self, request, pk):
        try:
            product_order = ProductOrder.objects.get(pk=pk)
        except ProductOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        serializer=ProductOrderSerializer(product_order)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    
class ProductOrderCheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            product_order = ProductOrder.objects.get(pk=pk)
        except ProductOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)

        product_order.status = Status.PENDING
        product_order.qr_code = generate_qr_code("test", product_order.id)
        product_order.save()
        provider=product_order.product.store.provider
        NotificationsHelper.sendProductOrderUpdates(OrdersUpdates.NEW_PORODUCT_ORDER,product_order,provider)
        serializer = ProductOrderSerializer(product_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomertProductCancelOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            product_order = ProductOrder.objects.get(pk=pk)
        except ProductOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        product_order.status=Status.CANCELLED
        product_order.save()
        provider=product_order.product.store.provider
        NotificationsHelper.sendProductOrderUpdates(OrdersUpdates.CLIENT_CANCEL_PRODUCT_ORDER,product_order,provider)
        return Response({"result":_("The order Canceled")},status=status.HTTP_200_OK)
    
class CustomertProductComplateOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            product_order = ProductOrder.objects.get(pk=pk)
        except ProductOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        product_order.status=Status.COMPLETED
        product_order.save()
        return Response({"result":_("The order Complated")},status=status.HTTP_200_OK)

######Service Order Views
class ServiceOrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ServiceOrderSerializer(data=request.data)
        if serializer.is_valid():
            customer = Customer.objects.get(phone=request.user.phone)
            service=Service.objects.get(id=request.data['service'])
            serializer.save(customer=customer,status=Status.UNCHECKED,duration=service.duration)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


    

class ServiceOrderCheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            service_order = ServiceOrder.objects.get(pk=pk)
        except ServiceOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)

        service_order.status = Status.PENDING
        service_order.qr_code = generate_qr_code("test", service_order.id)
        service_order.save()
        provider=service_order.service.store.provider
        NotificationsHelper.sendServiceOrderUpdates(OrdersUpdates.NEW_SERVICE_ORDER,service_order,provider)
        serializer = ServiceBookOrderSerializer(service_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ServiceOrderDetails(APIView):
    def post(self, request, pk):
        try:
            service_order = ServiceOrder.objects.get(pk=pk)
        except ServiceOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        coupon_code=request.data['coupon_code']
        try:
            coupon=Coupon.objects.get(code=coupon_code)
            if coupon.is_expired():
                 return Response({'error': _('Coupon  is expired.')}, status=status.HTTP_303_SEE_OTHER)
            
        except Coupon.DoesNotExist:
            return Response({'error': _('Coupon  not found.')}, status=status.HTTP_404_NOT_FOUND)
        if service_order.coupon:
            return Response({'error': _('There is coupon already.')}, status=status.HTTP_303_SEE_OTHER)
        service_order.coupon=coupon
        service_order.save()
        return Response({'coupon_value':coupon.value},status=status.HTTP_200_OK)
    def get(self, request, pk):
        try:
            service_order = ServiceOrder.objects.get(pk=pk)
        except ServiceOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        serializer=ServiceBookOrderSerializer(service_order)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
class ServiceOrderListView(generics.ListAPIView):
    serializer_class = ServiceBookOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        customer=Customer.objects.get(phone=self.request.user.phone)
        return ServiceOrder.objects.filter(customer=customer)
    
class CustomertServiceCancelOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            service_order = ServiceOrder.objects.get(pk=pk)
        except ServiceOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        service_order.status=Status.CANCELLED
        service_order.save()
        provider=service_order.service.store.provider
        NotificationsHelper.sendServiceOrderUpdates(OrdersUpdates.CLIENT_CANCEL_SERVICE_ORDER,service_order,provider)
        return Response({"result":_("The order Canceled")},status=status.HTTP_200_OK)
    
class CustomertServiceComplateOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            service_order = ServiceOrder.objects.get(pk=pk)
        except ServiceOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        service_order.status=Status.COMPLETED
        service_order.save()
        return Response({"result":_("The order Complated")},status=status.HTTP_200_OK)
    
class ServiceOrderFollow(APIView):
    def get(self, request, pk):
        try:
            service_order = ServiceOrder.objects.get(pk=pk)
        except ServiceOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        return Response ({'id':service_order.id,'status':service_order.status,'date':service_order.date,"time":service_order.time_start,'store_id':service_order.service.store.id})

    
class CurrentOrderCustomerListView(APIView):
    # serializer_class = ServiceOrderProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        customer = Customer.objects.get(phone=request.user.phone)
        service_orders = ServiceOrder.objects.filter(
            Q(customer=customer) &
            (Q(status=Status.PENDING) | Q(status=Status.IN_PROGRESS)))
        
        product_orders = ProductOrder.objects.filter(
            Q(customer=customer) &
            (Q(status=Status.PENDING) | Q(status=Status.IN_PROGRESS)))

        service_srializer = CustomerServiceOrderListSerializer(service_orders, many=True)
        product_srializer = CustomerProductOrderListSerializer(product_orders, many=True)
        
        data = {
            'service_orders':service_srializer.data,
            'product_orders':product_srializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
class PreviousOrderCustomerListView(APIView):
    # serializer_class = ServiceOrderProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        customer = Customer.objects.get(phone=request.user.phone)
        service_orders = ServiceOrder.objects.filter(
            Q(customer=customer) &
            (Q(status=Status.CANCELLED) | Q(status=Status.COMPLETED) | Q(status=Status.REJECTED))
        )
        product_orders = ProductOrder.objects.filter(
            Q(customer=customer) &
            (Q(status=Status.CANCELLED) | Q(status=Status.COMPLETED) | Q(status=Status.REJECTED))
        )
        
        
        service_srializer = CustomerServiceOrderListSerializer(service_orders, many=True)
        product_srializer = CustomerProductOrderListSerializer(product_orders, many=True)
        
        data = {
            'service_orders':service_srializer.data,
            'product_orders':product_srializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

### provider

class CurrentServiceOrderProviderListView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        provider = Provider.objects.get(phone=request.user.phone)
        service_orders = ServiceOrder.objects.filter(
            Q(service__store__provider=provider) &
            (Q(status=Status.PENDING) | Q(status=Status.IN_PROGRESS)))
        
        accepted_orders=service_orders.filter(status=Status.IN_PROGRESS)
        new_order=service_orders.filter(status=Status.PENDING)
        # Calculate the number of orders
        order_count = service_orders.count()
        
        # Calculate the total price of orders
        total_price = service_orders.aggregate(total_price=Sum('service__price'))['total_price']
        
        
        new_orders_serializer = ServiceOrderProviderSerializer(new_order, many=True)
        in_progress_serializer = ServiceOrderProviderSerializer(accepted_orders, many=True)
        data = {
            'order_count': order_count,
            'total_price': total_price if total_price else 0,
            'new_orders': new_orders_serializer.data,
            'in_progress_orders':in_progress_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
class PreviousServiceOrderProviderListView(APIView):
    # serializer_class = ServiceOrderProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        provider = Provider.objects.get(phone=request.user.phone)
        service_orders = ServiceOrder.objects.filter(
            Q(service__store__provider=provider) &
            (Q(status=Status.CANCELLED) | Q(status=Status.COMPLETED) | Q(status=Status.REJECTED))
        )
        accomplished_orders = service_orders.filter(status=Status.COMPLETED)
        rejected_orders = service_orders.filter(status=Status.REJECTED)
        canceled_orders = service_orders.filter(status=Status.CANCELLED)

        # Calculate the number of orders
        order_count = accomplished_orders.count()

        # Calculate the total price of orders
        total_price = service_orders.aggregate(total_price=Sum('service__price'))['total_price']

        accomplished_serializer = ServiceOrderProviderSerializer(accomplished_orders, many=True)
        rejected_serializer = ServiceOrderProviderSerializer(rejected_orders, many=True)
        canceled_serializer = ServiceOrderProviderSerializer(canceled_orders, many=True)
        
        data = {
            'order_count': order_count,
            'total_price': total_price if total_price else 0,
            'accomplished_orders': accomplished_serializer.data,
            'canceled_orders': canceled_serializer.data,
            'rejected_orders': rejected_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    

class CurrentProductOrderProviderListView(APIView):
    # serializer_class = ServiceOrderProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        provider = Provider.objects.get(phone=request.user.phone)
        product_orders = ProductOrder.objects.filter(Q(product__store__provider=provider) &
            (Q(status=Status.PENDING) | Q(status=Status.IN_PROGRESS)))
        accepted_orders=product_orders.filter(status=Status.IN_PROGRESS)
        new_order=product_orders.filter(status=Status.PENDING)
        # Calculate the number of orders
        order_count = product_orders.count()
        
        # Calculate the total price of orders
        total_price = product_orders.aggregate(total_price=Sum('product__price'))['total_price']
        
        
        new_orders_serializer = ProductOrderBookSerializer(new_order, many=True)
        in_progress_serializer = ProductOrderBookSerializer(accepted_orders, many=True)
        data = {
            'order_count': order_count,
            'total_price': total_price if total_price else 0,
            'new_orders': new_orders_serializer.data,
            'in_progress_orders':in_progress_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
class PreviousProductOrderProviderListView(APIView):
    serializer_class = ProductOrderBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        provider = Provider.objects.get(phone=request.user.phone)
        product_orders = ProductOrder.objects.filter(
            Q(product__store__provider=provider) &
            (Q(status=Status.CANCELLED) | Q(status=Status.COMPLETED) | Q(status=Status.REJECTED))
        )
        accomplished_orders = product_orders.filter(status=Status.COMPLETED)
        rejected_orders = product_orders.filter(status=Status.REJECTED)
        canceled_orders = product_orders.filter(status=Status.CANCELLED)

        # Calculate the number of orders
        order_count = accomplished_orders.count()

        # Calculate the total price of orders
        total_price = product_orders.aggregate(total_price=Sum('product__price'))['total_price']

        accomplished_serializer = ProductOrderBookSerializer(accomplished_orders, many=True)
        rejected_serializer = ProductOrderBookSerializer(rejected_orders, many=True)
        canceled_serializer = ProductOrderBookSerializer(canceled_orders, many=True)
        
        data = {
            'order_count': order_count,
            'total_price': total_price if total_price else 0,
            'accomplished_orders': accomplished_serializer.data,
            'canceled_orders': canceled_serializer.data,
            'rejected_orders': rejected_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


    
class ProductOrderProviderAccomplishedclassView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            product_order = ProductOrder.objects.get(pk=pk)
        except ProductOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)
        if product_order.status==Status.COMPLETED:
            return Response({'error': 'Product order already complated.'}, status=status.HTTP_409_CONFLICT)
        product_order.status = Status.COMPLETED
        product_order.save()

        return Response({'order_status':product_order.status})
        
        
class ServiceOrderProviderAccomplishedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            service_order = ServiceOrder.objects.get(pk=pk)
        except ServiceOrder.DoesNotExist:
            return Response({'error': _("order does not found!")}, status=status.HTTP_404_NOT_FOUND)

        if service_order.status==Status.COMPLETED:
            return Response({'error': _('Service order already complated.')}, status=status.HTTP_409_CONFLICT)
        service_order.status = Status.COMPLETED
        service_order.save()

        return Response({'order_status':service_order.status})
        

class ProductOrderProviderAcceptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductOrder.objects.get(pk=pk)
        except ProductOrder.DoesNotExist:
            raise NotFound({"error": _("Order not found")})

    def get(self, request, pk, format=None):
        product_order = self.get_object(pk)
        serializer = ProductOrderBookSerializer(product_order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product_order = self.get_object(pk)
        accepted=request.data['accepted']
        if accepted==True:
            product_order.status=Status.IN_PROGRESS
            product_order.save()
            # Notify the user
        else:
            product_order.status=Status.REJECTED
            product_order.save()
   

class ServiceOrderProviderAcceptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return ServiceOrder.objects.get(pk=pk)
        except ServiceOrder.DoesNotExist:
            return Response({"error":"Oreder not found"})
    def get(self, request, pk, format=None):
        service_order = self.get_object(pk)
        serializer = ServiceBookOrderSerializer(service_order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        service_order = self.get_object(pk)
        accepted=request.data['accepted']
        if accepted==True:
            service_order.status=Status.IN_PROGRESS
            service_order.save()
        else:
            service_order.status=Status.REJECTED
            service_order.save()
        service_order.status-Status.IN_PROGRESS
        return Response({'order_status':service_order.status})
            
        


class ServiceAndProductListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # Retrieve the service and product objects from the database
        provider = Provider.objects.get(username=request.user.username)
        product_queryset=ProductOrder.objects.filter(product__store__provider=provider,accomplished=False)
        service_queryset= ServiceOrder.objects.filter(service__store__provider=provider,accomplished=False)
      

        # Serialize the service and product objects
        product_serializer = ProductOrderSerializer(product_queryset, many=True)
        service_serializer = ServiceOrderSerializer(service_queryset, many=True)

        
        return Response({
                            'service': service_serializer.data,
                            'product': product_serializer.data
                       })



class CartAPIView(APIView):
    def get(self, request):
        customer=Customer.objects.get(username=request.user.username)
        cart ,created= Cart.objects.get_or_create(customer=customer)
        serializer=CartSerializer(cart)
        items = CartItem.objects.filter(cart=cart)
        return Response(serializer.data)
    
class CartCheckoutAPIView(APIView):
    def post(self, request):
        cart = Cart.objects.get(customer=request.user.customer)
        cart_items = CartItem.objects.filter(cart=cart)

        # Create product orders
        for cart_item in cart_items:
            product_order = ProductOrder.objects.create(
                customer=cart.customer,
                product=cart_item.product,
                quantity=cart_item.quantity,
                accept=False
            )
            product_order.save()

        # Create service orders
        service_cart_items = ServiceCartItem.objects.filter(cart=cart)
        
        for service_cart_item in service_cart_items:
            print(service_cart_item.date.time())
            service_order = ServiceOrder.objects.create(
                customer=cart.customer,
                service=service_cart_item.service,
                specialist=service_cart_item.specialist,
                date=service_cart_item.date,
                duration=service_cart_item.duration,
                accept=False
            )
            service_order.save()

        # Clear the cart
        cart_items.delete()
        service_cart_items.delete()

        return Response({"message": _("Order confirmed successfully.")}, status=status.HTTP_200_OK)
    
    



class CartItemAPIView(APIView):
    
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart = Cart.objects.get_or_create(customer=request.user.customer)

            product = serializer.validated_data.get('product')
            quantity = serializer.validated_data.get('quantity')
            price=0.0
            productObj=Product.objects.get(id=product)
            if productObj.offers:
                price=productObj.price_after_offer
            else:
                price=productObj.price
            
            # Check if the item already exists in the cart
            existing_item = CartItem.objects.filter(cart=cart[0], product=product).first()

            if existing_item:
                # If the item exists, increase the quantity
                existing_item.quantity += quantity
                existing_item.save()
                serializer = CartItemSerializer(existing_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If the item doesn't exist, create a new cart item
                serializer.save(cart=cart[0])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(CartItemSerializer(item).data,status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error":_("The Product not found in the cart")},status=status.HTTP_404_NOT_FOUND)

class ServiceCartItemAPIView(APIView):
    def get(self,request):
        service_cart_item=ServiceCartItem.objects.all()
        serializer = ServiceCartItemSerializer(service_cart_item,many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = ServiceCartItemSerializer(data=request.data)
        cart = Cart.objects.get_or_create(customer=request.user.customer)
        if serializer.is_valid():
            serializer.save(cart=cart[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        try:
            item = ServiceCartItem.objects.get(id=item_id)
            item.delete()
            return Response({"message": _("Deleted successfully.")},status=status.HTTP_204_NO_CONTENT)
        except ServiceCartItem.DoesNotExist:
            return Response({"error": _("Not found.")},status=status.HTTP_404_NOT_FOUND)
        
        
class SpecialistAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,service_id):
        try:
            service=Service.objects.get(id=service_id)
            print(service.main_service)
            specialists=StoreSpecialist.objects.filter(specialistworks=service.main_service)
            specialists_serializer=StoreSpecialistBookSerializer(specialists,many=True)
        except Service.DoesNotExist:
            return Response({"error":_("service does not found!")})
                     
        return Response(specialists_serializer.data)
    def post(self,request,service_id):
        date = request.data.get("date")
        specialist_id = request.data.get("specialist_id")
        try:
            service=Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"error":_("service does not found!")})
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        # Get the day from the datetime object
        day = parsed_date.strftime("%A")
        try:
         specialist = StoreSpecialist.objects.get(id=specialist_id)
        except StoreSpecialist.DoesNotExist:
            return Response({"error":_("The specialist is not exist")})
        try:
            storeopening = StoreOpening.objects.get(store=specialist.store, day=day)
        except StoreOpening.DoesNotExist:
            return Response({"error":_("In this day the store is closed")})
        orders = ServiceOrder.objects.filter(
            specialist=specialist,
            date__date=parsed_date,
            status=Status.IN_PROGRESS
        )
        hours_range = []
        current_time = storeopening.time_start
        while current_time < storeopening.time_end:
            slot_available = True
            for order in orders:
                order_start_time = datetime.combine(parsed_date.today(), order.date.time())
                order_end_time = order_start_time + timedelta(minutes=order.duration)
                if (current_time >= order_start_time.time() and current_time < order_end_time.time()):
                    slot_available = False
                    break
            if slot_available:
                hours_range.append(current_time.strftime('%H:%M'))
            current_time = (datetime.combine(parsed_date.today(), current_time) + timedelta(minutes=service.duration)).time()
        return Response(hours_range)

    

    
###########REPORTs
class ServiceReport(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        provider = Provider.objects.get(phone=request.user.phone)
        service_orders = ServiceOrder.objects.filter(Q(service__store__provider=provider) )