from app.frontend.models import OrganizationSetting

def organization_settings(request):
    organization = OrganizationSetting.objects.first()  # Get the first organization settings
    return {'organization': organization}
