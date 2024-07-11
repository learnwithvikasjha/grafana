```
import requests
from requests.auth import HTTPBasicAuth

# Define your Grafana credentials and URL
username = 'admin'
password = 'admin'
base_url = 'http://localhost:3000'

# Define the headers for the requests
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# Function to get the list of dashboards
def get_dashboards():
    url = f'{base_url}/api/search'
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to retrieve dashboards:', response.status_code, response.text)
        return []

# Function to take a screenshot of a dashboard
def screenshot_dashboard(uid, title):
    url = f'{base_url}/render/d/{uid}?orgId=1&width=1800&height=1900&kiosk=1'
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=headers)
    if response.status_code == 200:
        filename = f"{title.replace(' ', '_')}.png"
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'Dashboard image saved as {filename}')
    else:
        print(f'Failed to render the dashboard {title}:', response.status_code, response.text)

# Main function to get dashboards and take screenshots
def main():
    dashboards = get_dashboards()
    for dashboard in dashboards:
        if 'uid' in dashboard:
            uid = dashboard['uid']
            title = dashboard['title']
            screenshot_dashboard(uid, title)

# Run the main function
if __name__ == '__main__':
    main()
```
