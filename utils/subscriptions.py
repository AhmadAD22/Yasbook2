from auth_login.models import ProviderSubscription
from provider_details.models import Store


def active_stores():
    # Get the active ProviderSubscription
        subscriptions = ProviderSubscription.objects.all()
        active_providers=[]
        for subscription in subscriptions:
            if subscription.is_duration_finished()==False:
                active_providers.append(subscription.provider)
                
        stores=Store.objects.filter(provider__in=active_providers)
        return stores
            