 
import datetime
from cal_setup import get_calendar_service

def main():
   service = get_calendar_service()
   # Call the Calendar API
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   events_result = service.events().list(
       calendarId='63kbvgtn7h74cbei1b4lfbc8fc@group.calendar.google.com', timeMin=now,
       maxResults=10, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

   if not events:
       print('No upcoming events found.')
   for event in events:
       start = event['start'].get('dateTime', event['start'].get('date'))
       print(start, event['summary'], event['id'])

if __name__ == '__main__':
   main()