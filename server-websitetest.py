import requests
import threading
import time
import sys
import pyfiglet

# Function to print colorful text
def print_colored(text, color_code, bold=False):
    if bold:
        sys.stdout.write(f"\033[{color_code};1m{text}\033[0m\n")  # Bold text
    else:
        sys.stdout.write(f"\033[{color_code}m{text}\033[0m\n")

# Function to print name in large board-like font
def print_big_name():
    big_name = pyfiglet.figlet_format("NEPOMODZ")
    print_colored(big_name, "35")  # Display in purple color

# Function to print disclaimer on the right side
def print_disclaimer():
    disclaimer = "DON'T USE THIS FOR HARMFUL PURPOSES. THIS IS ONLY FOR EDUCATIONAL PURPOSES."
    terminal_width = 80  # Assuming terminal width
    padding = terminal_width - len(disclaimer)  # Calculate the padding required
    # Color codes for a gradient effect: Pink, Green, Blue, Yellow, Red
    colors = [35, 32, 34, 33, 31]  # Purple, Green, Blue, Yellow, Red
    colored_disclaimer = ""
    color_index = 0
    for char in disclaimer:
        colored_disclaimer += f"\033[{colors[color_index % len(colors)]}m{char}\033[0m"
        color_index += 1
    print_colored(f"{' ' * padding}{colored_disclaimer}", "0")  # Print with padding on the right

# Ask for confirmation to continue the stress test
def ask_for_confirmation():
    while True:
        print_colored("Do you want to continue this stress test? (Y/N):", "36", bold=True)  # Cyan color with bold
        answer = input().strip().lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            print_colored("Stress test aborted.", "31")  # Red text for abortion
            sys.exit()
        else:
            print_colored("Invalid input, please enter Y or N.", "33")  # Yellow text for invalid input

# Ask for the URL
def get_url():
    print_colored("Enter your URL for the stress test:", "31")  # Red text for URL input
    url = input().strip()
    return url

# Parameters for stress test
requests_per_minute = 100  # How many requests you want to make per minute
test_duration_minutes = 500000 # Duration of the stress test (in minutes)

# Helper function to make a request
def make_request(url):
    try:
        response = requests.get(url)
        print(f"Request successful: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Function to control the number of requests
def stress_test(url):
    total_requests = requests_per_minute * test_duration_minutes
    requests_made = 0
    start_time = time.time()

    while requests_made < total_requests:
        threading.Thread(target=make_request, args=(url,)).start()
        requests_made += 1
        time.sleep(6 / requests_per_minute)  # Control the request rate

    # Wait until all threads are done
    elapsed_time = time.time() - start_time
    print_colored(f"Stress test completed in {elapsed_time:.2f} seconds. Total requests: {total_requests}", "32")  # Green text for completion

# Run the script
if __name__ == "__main__":
    print_big_name()  # Display your name in a big font
    print_disclaimer()  # Print the disclaimer on the right side
    if ask_for_confirmation():
        url = get_url()
        stress_test(url)