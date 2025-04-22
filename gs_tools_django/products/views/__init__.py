from .brand import BrandViewSet
from .category import CategoryViewSet
from .discount import DiscountViewSet
from .image import ImageViewSet
from .product import ProductViewSet
from .product_specification import ProductSpecificationViewSet
from .tag import TagViewSet

__all__ = [
    "BrandViewSet",
    "CategoryViewSet",
    "DiscountViewSet",
    "ImageViewSet",
    "ProductSpecificationViewSet",
    "ProductViewSet",
    "TagViewSet",
]
