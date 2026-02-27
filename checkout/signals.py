"""
Signals for automatic cache invalidation when card pricing is updated
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import CardPricing
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CardPricing)
def invalidate_pricing_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate pricing cache whenever a CardPricing instance is saved
    """
    cache_key = 'active_pricing_plans'
    cache.delete(cache_key)
    
    action = "created" if created else "updated"
    logger.info(f"CardPricing '{instance.name}' was {action}. Cache invalidated.")


@receiver(post_delete, sender=CardPricing)
def invalidate_pricing_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate pricing cache whenever a CardPricing instance is deleted
    """
    cache_key = 'active_pricing_plans'
    cache.delete(cache_key)
    
    logger.info(f"CardPricing '{instance.name}' was deleted. Cache invalidated.")
