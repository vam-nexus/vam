import requests
import json
from datetime import datetime, timedelta
import os
import pytz

url = "https://api.lu.ma/public/v1/calendar/list-events"

headers = {
    "accept": "application/json",
    "x-luma-api-key": "secret-Du1DtefEcdXTalKLLiXmV7aYq",
}

response = requests.get(url, headers=headers)
events = response.json()

# Get current date and date 10 days from now (as UTC timezone-aware datetimes)
pdt_timezone = pytz.timezone("America/Los_Angeles")
current_date = datetime.now(pdt_timezone)
ten_days_later = current_date + timedelta(days=10)

# Filter and format events for the next 10 days
filtered_events = []
for entry in events["entries"]:
    event = entry["event"]  # Access the nested event data
    # Parse the UTC time and convert to PDT
    start_time_utc = datetime.fromisoformat(event["start_at"].replace("Z", "+00:00"))
    start_time = start_time_utc.astimezone(pdt_timezone)

    # Only include events in the next 10 days
    if current_date <= start_time <= ten_days_later:
        formatted_date = start_time.strftime("%B %d")  # Month and day
        formatted_time = start_time.strftime(
            "%I:%M %p %Z"
        )  # Time in 12-hour format with timezone

        event_info = {
            "name": event["name"],
            "url": event["url"],
            "description": event["description"],
            "date": formatted_date,
            "time": formatted_time,
        }
        filtered_events.append(event_info)

# Sort events by date/time
filtered_events.sort(
    key=lambda x: datetime.strptime(
        f"{x['date']} {x['time'].split(' ')[0]} {x['time'].split(' ')[1]}",
        "%B %d %I:%M %p",
    )
)

# Create markdown content
markdown_content = "# Upcoming Events (Next 10 Days)\n\n"

for event in filtered_events:
    markdown_content += f"## {event['name']}\n\n"
    markdown_content += f"**Date:** {event['date']} at {event['time']}\n\n"
    markdown_content += f"**Description:** {event['description']}\n\n"
    markdown_content += f"**Event Link:** [{event['url']}]({event['url']})\n\n"
    markdown_content += "---\n\n"

# Save to markdown file
output_file = "upcoming_events.md"
with open(output_file, "w") as f:
    f.write(markdown_content)

print(f"Events for the next 10 days have been saved to {output_file}")
