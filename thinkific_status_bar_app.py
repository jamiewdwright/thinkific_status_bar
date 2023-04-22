import rumps
import requests
import json

# Updated 22 april 1530
# Replace with your Thinkific API key and subdomain
API_KEY = "97303e320f2b1fd16ecccd7ddf1b2c24"
SUBDOMAIN = "stayathomechoir"

THINKIFIC_API_BASE_URL = "https://api.thinkific.com/api/public/v1/courses"
HEADERS = {
    "X-Auth-API-Key": API_KEY,
    "X-Auth-Subdomain": SUBDOMAIN,
    "Content-Type": "application/json",
}

# Fetch Courses from Thinkific API
def fetch_courses():
    response = requests.get(THINKIFIC_API_BASE_URL, headers=HEADERS, params={"page": 1, "limit": 100})

    if response.status_code == 200:
        json_response = response.json()
        return json_response
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response text: {response.text}")
        return None


def save_course_names_to_file(course_names, filename="all_course_names.txt"):
    with open(filename, "w") as file:
        for course_name in course_names:
            file.write(course_name + "\n")

def get_courses_to_show(filename="Show-Hide_Courses.txt"):
    courses_to_show = set()
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line.endswith("*"):
                course_name = line[:-1]
                courses_to_show.add(course_name)
    return courses_to_show


# Fetch courses and print the entire JSON response to the console
courses_json = fetch_courses()
if courses_json:
    print(json.dumps(courses_json, indent=2))
    all_courses = courses_json["items"]

    # Save all course names to a text file
    course_names = [course["name"] for course in all_courses]
    save_course_names_to_file(course_names)

    # Filter courses based on the "Show-Hide Courses" text file
    courses_to_show = get_courses_to_show()
    if courses_to_show:
        courses = [course for course in all_courses if course["name"] in courses_to_show]
    else:
        courses = all_courses[-5:]
else:
    courses = []


class ThinkificStatusBarApp(rumps.App):
    def __init__(self):
        super(ThinkificStatusBarApp, self).__init__("SAHC")
        self.update_courses()

    def update_courses(self):
        self.menu.clear()

        if courses:
            for course in courses:
                self.menu.add(rumps.MenuItem(course["name"]))
        else:
            self.menu.add(rumps.MenuItem("No courses found"))

if __name__ == "__main__":
    ThinkificStatusBarApp().run()
