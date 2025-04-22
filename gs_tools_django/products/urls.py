from django.urls import include, path
from rest_framework.routers import SimpleRouter

from gs_tools_django.products.views import (
    BrandViewSet,
    CategoryViewSet,
    DiscountViewSet,
    ImageViewSet,
    ProductSpecificationViewSet,
    ProductViewSet,
    TagViewSet,
)
from gs_tools_django.products.views.catalog import CatalogViewSet
from gs_tools_django.products.views.variant import VariantViewSet

# Root router for top-level resources
router = SimpleRouter()
router.register("brands", BrandViewSet, basename="brands")
router.register("categories", CategoryViewSet, basename="categories")
router.register("tags", TagViewSet, basename="tags")
router.register("products", ProductViewSet, basename="products")

# Nested router for per-product content (discounts, catalogs, specs)
content_router = SimpleRouter()
content_router.register(
    "discounts",
    DiscountViewSet,
    basename="product-discounts",
)
content_router.register(
    "catalogs",
    CatalogViewSet,
    basename="product-catalogs",
)
content_router.register(
    "specifications",
    ProductSpecificationViewSet,
    basename="product-specifications",
)

# Nested router for product variants
variant_router = SimpleRouter()
variant_router.register(
    "variants",
    VariantViewSet,
    basename="product-variants",
)

# Nested router for images under a catalog
image_router = SimpleRouter()
image_router.register("images", ImageViewSet, basename="catalog-images")

urlpatterns = [
    # Top-level endpoints
    path("", include(router.urls)),
    # /products/{product_id}/discounts/, /catalogs/, /specifications/, /variants/
    path(
        "products/<uuid:product_id>/",
        include(content_router.urls + variant_router.urls),
    ),
    # /products/{product_id}/variants/{variant_id}/{discounts,catalogs,specifications}/
    path(
        "products/<uuid:product_id>/variants/<uuid:variant_id>/",
        include(content_router.urls),
    ),
    # /catalogs/{catalog_id}/images/
    path(
        "catalogs/<uuid:catalog_id>/",
        include(image_router.urls),
    ),
]
