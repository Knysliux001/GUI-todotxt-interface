from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def main():
   # creates one hour event tomorrow 10 AM IST
   service = get_calendar_service()

   d = datetime.now().date()
   tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
   # start = tomorrow.isoformat()
   # end = (tomorrow + timedelta(hours=1)).isoformat()

   event_result = service.events().insert(calendarId='63kbvgtn7h74cbei1b4lfbc8fc@group.calendar.google.com',
       body={
           "summary": 'An all day event from PyCharm',
           "description": 'This is a tutorial example',
           "start": {"date": d.isoformat()},
           "end": {"date": d.isoformat()},
           # "start": {"dateTime": start, "timeZone": 'Europe/Vilnius'},
           # "end": {"dateTime": end, "timeZone": 'Europe/Vilnius'},
       }
   ).execute()

   print("created event")
   print("id: ", event_result['id'])
   print("summary: ", event_result['summary'])
   print("starts at: ", event_result['start']['date'])
   print("ends at: ", event_result['end']['date'])

if __name__ == '__main__':
   main()