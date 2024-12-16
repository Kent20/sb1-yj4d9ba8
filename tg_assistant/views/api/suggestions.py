"""
API endpoint for getting message suggestions
"""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ...services.response.service import ResponseService

@login_required
def generate_suggestions(request):
    """Generate AI suggestions for messages"""
    try:
        service = ResponseService()
        suggestions = service.generate_responses()
        return JsonResponse({'suggestions': suggestions})
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)