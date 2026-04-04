from django.conf import settings
from django.db import migrations, models


def backfill_coin_ledger_entries(apps, schema_editor):
    CoinLedgerEntry = apps.get_model("store", "CoinLedgerEntry")
    BrandStoreRedemption = apps.get_model("store", "BrandStoreRedemption")
    PostReaction = apps.get_model("feed", "PostReaction")
    Comment = apps.get_model("feed", "Comment")
    Post = apps.get_model("feed", "Post")
    BookRequisition = apps.get_model("learning", "BookRequisition")

    def create_entry(
        *,
        user_id,
        entry_type,
        event_key,
        amount,
        reference_key,
        occurred_at,
        summary,
        metadata,
    ):
        CoinLedgerEntry.objects.get_or_create(
            reference_key=reference_key,
            defaults={
                "user_id": user_id,
                "entry_type": entry_type,
                "event_key": event_key,
                "amount": amount,
                "occurred_at": occurred_at,
                "summary": summary,
                "metadata": metadata,
            },
        )

    for reaction in PostReaction.objects.select_related("post", "user").filter(reaction_type="like"):
        create_entry(
            user_id=reaction.user_id,
            entry_type="earn",
            event_key="reaction_given",
            amount=1,
            reference_key=f"reaction:{reaction.id}:reaction_given:earn:1",
            occurred_at=reaction.created_at,
            summary=f"Liked '{reaction.post.title}'",
            metadata={"post_id": reaction.post_id, "reaction_type": reaction.reaction_type},
        )

    for comment in Comment.objects.select_related("post", "author").filter(moderation_status="published"):
        create_entry(
            user_id=comment.author_id,
            entry_type="earn",
            event_key="published_comment",
            amount=10,
            reference_key=f"comment:{comment.id}:published_comment:earn:1",
            occurred_at=comment.created_at,
            summary=f"Commented on '{comment.post.title}'",
            metadata={"post_id": comment.post_id},
        )

    for post in Post.objects.select_related("author"):
        metadata = post.metadata or {}
        if post.module != "employee_posts" or post.moderation_status != "published":
            continue
        if metadata.get("town_hall_response"):
            event_key = "question_asked"
        elif metadata.get("ceo_desk_request"):
            event_key = "ceo_request"
        elif metadata.get("submission_key") == "share_idea":
            event_key = "idea_shared"
        else:
            continue

        amount = 1000 if event_key in {"question_asked", "ceo_request"} else 500
        create_entry(
            user_id=post.author_id,
            entry_type="earn",
            event_key=event_key,
            amount=amount,
            reference_key=f"post:{post.id}:{event_key}:earn:1",
            occurred_at=post.published_at or post.created_at,
            summary=f"Approved '{post.title}'",
            metadata={
                "post_id": post.id,
                "submission_key": metadata.get("submission_key", ""),
            },
        )

    for requisition in BookRequisition.objects.select_related("book", "requester").filter(status="returned"):
        create_entry(
            user_id=requisition.requester_id,
            entry_type="earn",
            event_key="book_returned",
            amount=100,
            reference_key=f"book_requisition:{requisition.id}:book_returned:earn:1",
            occurred_at=requisition.returned_at or requisition.updated_at,
            summary=f"Returned '{requisition.book.title}'",
            metadata={"book_id": requisition.book_id},
        )

    for redemption in BrandStoreRedemption.objects.select_related("item", "requester"):
        metadata = {"item_id": redemption.item_id, "redemption_id": redemption.id}
        create_entry(
            user_id=redemption.requester_id,
            entry_type="hold",
            event_key="store_request",
            amount=redemption.points_locked,
            reference_key=f"redemption:{redemption.id}:store_request:hold",
            occurred_at=redemption.created_at,
            summary=f"Requested {redemption.item.name}",
            metadata=metadata,
        )

        if redemption.status in {"cancelled", "declined", "approved", "fulfilled"}:
            create_entry(
                user_id=redemption.requester_id,
                entry_type="release",
                event_key="store_request",
                amount=redemption.points_locked,
                reference_key=f"redemption:{redemption.id}:store_request:release",
                occurred_at=redemption.reviewed_at or redemption.updated_at,
                summary=f"Released hold for {redemption.item.name}",
                metadata=metadata,
            )

        if redemption.status in {"approved", "fulfilled"}:
            create_entry(
                user_id=redemption.requester_id,
                entry_type="spend",
                event_key="store_request",
                amount=redemption.points_locked,
                reference_key=f"redemption:{redemption.id}:store_request:spend",
                occurred_at=redemption.reviewed_at or redemption.updated_at,
                summary=f"Collected {redemption.item.name}",
                metadata=metadata,
            )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feed", "0004_narrow_post_modules"),
        ("learning", "0002_book_catalog_fields_and_seed"),
        ("store", "0002_brand_store_coin_workflow"),
    ]

    operations = [
        migrations.CreateModel(
            name="CoinLedgerEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("entry_type", models.CharField(choices=[("earn", "Earn"), ("earn_reversal", "Earn reversal"), ("hold", "Hold"), ("release", "Release"), ("spend", "Spend")], max_length=24)),
                ("event_key", models.CharField(max_length=64)),
                ("amount", models.PositiveIntegerField()),
                ("reference_key", models.CharField(max_length=180, unique=True)),
                ("summary", models.CharField(blank=True, max_length=280)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("occurred_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="coin_ledger_entries", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("-occurred_at", "-id"),
            },
        ),
        migrations.AddIndex(
            model_name="coinledgerentry",
            index=models.Index(fields=["user", "occurred_at"], name="store_coinl_user_id_d65b26_idx"),
        ),
        migrations.AddIndex(
            model_name="coinledgerentry",
            index=models.Index(fields=["user", "entry_type"], name="store_coinl_user_id_70d3f2_idx"),
        ),
        migrations.RunPython(backfill_coin_ledger_entries, migrations.RunPython.noop),
    ]
