import json
import os
FILE_NAME = "data.json"
class Event:
    def __init__(self, event_id, title, date, start, end, dept, event_type):
        self.event_id = event_id
        self.title = title
        self.date = date
        self.start = start
        self.end = end
        self.dept = dept
        self.type = event_type
    def to_dict(self):
        return self.__dict__
rooms = {}
events = {}
bookings = []
def load_data():
    global rooms, events, bookings
    if not os.path.exists(FILE_NAME):
        return
    with open(FILE_NAME, "r") as f:
        data = json.load(f)
        rooms = data.get("rooms", {})
        bookings = data.get("bookings", [])
        events.clear()
        for k, v in data.get("events", {}).items():
            events[k] = Event(**v)
def save_data():
    data = {
        "rooms": rooms,
        "events": {k: v.to_dict() for k, v in events.items()},
        "bookings": bookings
    }
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)
def check_availability(room_id, date, start, end):
    for b in bookings:
        if b["room_id"] == room_id and b["date"] == date:
            if start < b["end"] and end > b["start"]:
                return False
    return True
def add_room():
    room_id = input("Enter Room ID: ").strip()
    if room_id in rooms:
        print("Room already exists!\n")
        return
    capacity = input("Enter Capacity: ").strip()
    features = input("Enter Features (comma separated): ").strip()
    rooms[room_id] = {
        "capacity": capacity,
        "features": features
    }
    print("Room added successfully!\n")
def add_event():
    event_id = input("Enter Event ID: ").strip()
    if event_id in events:
        print("Event already exists!\n")
        return
    title = input("Enter Title: ").strip()
    date = input("Enter Date (YYYY-MM-DD): ").strip()
    start = input("Enter Start Time (HH:MM): ").strip()
    end = input("Enter End Time (HH:MM): ").strip()
    dept = input("Enter Department: ").strip()
    event_type = input("Enter Event Type: ").strip()
    events[event_id] = Event(event_id, title, date, start, end, dept, event_type)
    print("Event added successfully!\n")
def book_room():
    event_id = input("Enter Event ID: ").strip()
    room_id = input("Enter Room ID: ").strip()
    if event_id not in events:
        print("Event not found!\n")
        return
    if room_id not in rooms:
        print("Room not found!\n")
        return
    event = events[event_id]
    if check_availability(room_id, event.date, event.start, event.end):
        bookings.append({
            "event_id": event_id,
            "room_id": room_id,
            "date": event.date,
            "start": event.start,
            "end": event.end
        })
        print("Room booked successfully!\n")
    else:
        print("Conflict detected! Room not available.\n")
def view_events():
    if not events:
        print("No events found.\n")
        return
    for e in events.values():
        print("\n-------------------")
        print(f"ID: {e.event_id}")
        print(f"Title: {e.title}")
        print(f"Date: {e.date}")
        print(f"Time: {e.start} - {e.end}")
        print(f"Department: {e.dept}")
        print(f"Type: {e.type}")
def view_bookings():
    if not bookings:
        print("No bookings available.\n")
        return
    for b in bookings:
        print(f"{b['event_id']} -> Room {b['room_id']} | {b['date']} {b['start']}-{b['end']}")
def search_event():
    keyword = input("Enter keyword: ").lower()
    found = False
    for e in events.values():
        if keyword in e.title.lower() or keyword in e.date:
            print(f"{e.event_id} | {e.title} | {e.date} {e.start}-{e.end}")
            found = True
    if not found:
        print("No matching events found.\n")
def report():
    print("\n===== REPORT =====")
    print("Total Rooms:", len(rooms))
    print("Total Events:", len(events))
    print("Total Bookings:", len(bookings))
def main():
    load_data()
    while True:
        print("\n===== Smart Event & Space Scheduler =====")
        print("1. Add Room")
        print("2. Add Event")
        print("3. Book Room")
        print("4. View Events")
        print("5. View Bookings")
        print("6. Generate Report")
        print("7. Search Event")
        print("8. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_room()
        elif choice == "2":
            add_event()
        elif choice == "3":
            book_room()
        elif choice == "4":
            view_events()
        elif choice == "5":
            view_bookings()
        elif choice == "6":
            report()
        elif choice == "7":
            search_event()
        elif choice == "8":
            save_data()
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice! Try again.\n")
if __name__ == "__main__":
    main()