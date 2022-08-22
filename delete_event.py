## Script to delete events from google calendar

    from cal_setup import get_calendar_service

    def main():
       # Delete the event
       service = get_calendar_service()
       try:
           service.events().delete(
               calendarId='63kbvgtn7h74cbei1b4lfbc8fc@group.calendar.google.com',
               eventId='p7eu20cbmffatgb4iu90rd3ff4',
           ).execute()
       except googleapiclient.errors.HttpError:
           print("Failed to delete event")

       print("Event deleted")

    if __name__ == '__main__':
       main()