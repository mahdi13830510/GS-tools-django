from django.db import models
from django.db.models import Case, DecimalField, F, OuterRef, Subquery, Value, When
from django.db.models.functions import Coalesce, Greatest
from django.utils import timezone


class ProductQuerySet(models.QuerySet):
    def with_discounted_price(self):
        from django.contrib.contenttypes.models import ContentType

        from gs_tools_django.products.models import Discount

        now = timezone.now()
        ct_product = ContentType.objects.get_for_model(self.model)

        # compute discounted price using the *outer* product.price
        discount_price_expr = Case(
            When(
                discount_type="percentage",
                then=OuterRef("price") * (Value(1) - F("value") / Value(100)),
            ),
            When(discount_type="fixed", then=Greatest(OuterRef("price") - F("value"), Value(0))),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        )

        # pick the lowest discounted price among all active discounts
        discount_subquery = (
            Discount.objects.filter(
                content_type=ct_product,
                object_id=OuterRef("pk"),
                start_date__lte=now,
                end_date__gte=now,
            )
            .annotate(discounted_price=discount_price_expr)
            .order_by("discounted_price")
            .values("discounted_price")[:1]
        )

        # annotate each product with either the subquery result or its own price
        return self.annotate(
            discounted_price=Coalesce(
                Subquery(
                    discount_subquery, output_field=DecimalField(max_digits=10, decimal_places=2)
                ),
                F("price"),
            )
        )
