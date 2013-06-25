'''
Created on 24-Jun-2013

@author: arun
'''


from django.utils.functional import SimpleLazyObject
from django.contrib.sites.models import RequestSite

from saas.models import Tenant



class OrganizationMiddleware(object):
    
    def process_request(self, request):
        
        request.tenant = SimpleLazyObject(lambda: self.get_tenant(request))
        
        
    def get_tenant(self, request):
        if not hasattr(request, "_cached_tenant"):
            request._cached_tenant = self._get_tenant(request)
        return request._cached_tenant

    def _get_tenant(self, request):
        site = RequestSite(request)
        subdomain = self._get_subdomain(site)
        try:
            tenant = Tenant.objects.get(domain_name=subdomain)
        except Tenant.DoesNotExist:
            tenant = None
        return tenant

    def _get_subdomain(self, site):
        """
            Takes site object as argument.
            if the current request is being made from sub-domain(tenant)
            then this will extract the subdomain name, else None
        """
        splited_domain_name = site.domain.split(".")
        subdomain = splited_domain_name[0] if len(splited_domain_name) >=3 else ""
        return subdomain