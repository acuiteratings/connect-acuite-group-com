from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from feed.models import Comment, Post, PostReaction
from learning.models import BookRequisition

from .models import BrandStoreRedemption
from .services import (
    reverse_coin_ledger_for_comment,
    reverse_coin_ledger_for_reaction,
    sync_coin_ledger_for_book_requisition,
    sync_coin_ledger_for_comment,
    sync_coin_ledger_for_post,
    sync_coin_ledger_for_reaction,
    sync_coin_ledger_for_redemption,
)


@receiver(post_save, sender=PostReaction, dispatch_uid="store_coin_ledger_reaction_save")
def store_coin_ledger_reaction_save(instance, raw=False, **kwargs):
    if raw:
        return
    sync_coin_ledger_for_reaction(instance)


@receiver(post_delete, sender=PostReaction, dispatch_uid="store_coin_ledger_reaction_delete")
def store_coin_ledger_reaction_delete(instance, **kwargs):
    reverse_coin_ledger_for_reaction(instance)


@receiver(post_save, sender=Comment, dispatch_uid="store_coin_ledger_comment_save")
def store_coin_ledger_comment_save(instance, raw=False, **kwargs):
    if raw:
        return
    sync_coin_ledger_for_comment(instance)


@receiver(post_delete, sender=Comment, dispatch_uid="store_coin_ledger_comment_delete")
def store_coin_ledger_comment_delete(instance, **kwargs):
    reverse_coin_ledger_for_comment(instance)


@receiver(post_save, sender=Post, dispatch_uid="store_coin_ledger_post_save")
def store_coin_ledger_post_save(instance, raw=False, **kwargs):
    if raw:
        return
    sync_coin_ledger_for_post(instance)


@receiver(post_save, sender=BookRequisition, dispatch_uid="store_coin_ledger_book_requisition_save")
def store_coin_ledger_book_requisition_save(instance, raw=False, **kwargs):
    if raw:
        return
    sync_coin_ledger_for_book_requisition(instance)


@receiver(post_save, sender=BrandStoreRedemption, dispatch_uid="store_coin_ledger_redemption_save")
def store_coin_ledger_redemption_save(instance, raw=False, **kwargs):
    if raw:
        return
    sync_coin_ledger_for_redemption(instance)
