from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    #
    path("users/api/", include("users.urls")),
    path("organizations/api/", include("organizations.urls")),
    path("calls/api/", include("calls.urls")),
    # path("chat/api/", include("chat.urls")),
    # path("web/", include("web.urls")),
    #
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
