from comicsdb.models.announcement import Announcement


def announcement_context_processor(request):
    return {"active_announcements": Announcement.active_announcements()}
