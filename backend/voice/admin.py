from django.contrib import admin

from .models import Poll, PollOption, PollVote


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "closes_at", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("question", "description")
    inlines = (PollOptionInline,)


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ("label", "poll", "position")
    list_filter = ("poll",)
    search_fields = ("label", "poll__question")
    autocomplete_fields = ("poll",)


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ("poll", "option", "voter", "updated_at")
    list_filter = ("poll", "updated_at")
    search_fields = ("poll__question", "option__label", "voter__email")
    autocomplete_fields = ("poll", "option", "voter")
