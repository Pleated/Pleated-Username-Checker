import requests
import string
import itertools
import time
import random
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

try:
    import colorama
    from colorama import Fore, Back, Style
    from termcolor import colored
    colorama.init()
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False
    print("For the best experience, install colorama and termcolor:")
    print("pip install colorama termcolor")
    input("Press Enter to continue anyway...")

class RainbowText:
    def __init__(self):
        self.colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA] if COLOR_SUPPORT else [""]
        self.current_color = 0
    
    def print_rainbow_text(self, text, delay=0.03):
        """Print text with rainbow effect"""
        if not COLOR_SUPPORT:
            print(text)
            return
            
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print each character with a different color
        rainbow_text = ""
        for char in text:
            if char == '\n':
                rainbow_text += char
                continue
                
            rainbow_text += self.colors[self.current_color] + char + Style.RESET_ALL
            self.current_color = (self.current_color + 1) % len(self.colors)
        
        # Print the rainbow text
        for line in rainbow_text.split('\n'):
            print(line)
            time.sleep(delay)
        
        # Reset cursor position for animation
        print("\033[F" * (text.count('\n') + 1))
    
    def animate_title(self, title, frames=3):
        """Animate the title with changing colors"""
        if not COLOR_SUPPORT:
            print(title)
            return
            
        for _ in range(frames):
            self.print_rainbow_text(title)
            time.sleep(0.3)
        print("\n" * (title.count('\n') + 2))  # Move cursor down after animation

class UsernameChecker:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.available_usernames = []
        self.checked_count = 0
        self.platforms = {
            "reddit": self.check_reddit,
            "spotify": self.check_spotify,
            "roblox": self.check_roblox,
            "xbox": self.check_xbox
        }
        self.rainbow = RainbowText()
    
    def check_reddit(self, username):
        """Check if a username is available on Reddit"""
        url = f"https://www.reddit.com/api/username_available.json?user={username}"
        headers = {"User-Agent": self.user_agent}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                is_available = response.json()
                if is_available:
                    return True
            return False
        except Exception as e:
            self.print_error(f"Error checking Reddit username {username}: {e}")
            return False
    
    def check_spotify(self, username):
        """Check if a username is available on Spotify"""
        url = f"https://open.spotify.com/user/{username}"
        headers = {"User-Agent": self.user_agent}
        
        try:
            response = requests.get(url, headers=headers)
            # If we get a 404, the username is available
            if response.status_code == 404:
                return True
            return False
        except Exception as e:
            self.print_error(f"Error checking Spotify username {username}: {e}")
            return False
    
    def check_roblox(self, username):
        """Check if a username is available on Roblox"""
        url = f"https://auth.roblox.com/v1/usernames/validate"
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json"
        }
        data = {
            "username": username,
            "birthday": "1990-01-01T00:00:00.000Z",
            "context": "Signup"
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                # If the API says the username is valid (code 0), it's available
                if result.get("code") == 0:
                    return True
            return False
        except Exception as e:
            self.print_error(f"Error checking Roblox username {username}: {e}")
            return False
    
    def check_xbox(self, username):
        """Check if a username is available on Xbox"""
        url = f"https://profile.xboxlive.com/users/gt({username})/profile/settings"
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            # If we get a 404, the gamertag is available
            if response.status_code == 404:
                return True
            return False
        except Exception as e:
            self.print_error(f"Error checking Xbox username {username}: {e}")
            return False
    
    def generate_usernames(self, length, count):
        """Generate random usernames of specified length"""
        characters = string.ascii_lowercase + string.digits
        usernames = []
        
        # Get all possible combinations if user asks for too many
        total_possibilities = len(characters) ** length
        count = min(count, total_possibilities)
        
        # For 2-letter usernames, we can enumerate all possibilities if the count is close to total
        if length == 2 and count > total_possibilities * 0.5:
            self.print_warning(f"For 2-letter usernames, there are {total_possibilities} total possibilities.")
            self.print_warning(f"Generating all possible combinations and selecting {count} random ones.")
            all_combinations = [''.join(combo) for combo in itertools.product(characters, repeat=length)]
            return random.sample(all_combinations, count)
        
        # Generate random usernames without duplicates
        while len(usernames) < count:
            username = ''.join(random.choice(characters) for _ in range(length))
            if username not in usernames:
                usernames.append(username)
        
        return usernames
    
    def print_progress(self, progress, total):
        """Print a fancy progress bar"""
        if not COLOR_SUPPORT:
            print(f"Progress: {progress}/{total}", end="\r")
            return
            
        bar_length = 30
        filled_length = int(bar_length * progress / total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        percentage = round(100.0 * progress / total, 1)
        progress_text = f" {Fore.CYAN}[{bar}] {percentage}% ({progress}/{total}){Style.RESET_ALL}"
        
        print(progress_text, end="\r")
        sys.stdout.flush()
    
    def print_success(self, message):
        """Print success message in green"""
        if COLOR_SUPPORT:
            print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        else:
            print(message)
    
    def print_error(self, message):
        """Print error message in red"""
        if COLOR_SUPPORT:
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")
        else:
            print(message)
    
    def print_warning(self, message):
        """Print warning message in yellow"""
        if COLOR_SUPPORT:
            print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
        else:
            print(f"WARNING: {message}")
    
    def check_username(self, platform, username):
        """Check a single username on the specified platform"""
        is_available = self.platforms[platform](username)
        self.checked_count += 1
        
        # Print progress
        self.print_progress(self.checked_count, self.total_usernames)
        
        if is_available:
            self.available_usernames.append(username)
            self.print_success(f"\nUsername '{username}' is AVAILABLE on {platform}!")
        
        # Add a small delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 1.5))
        
        return is_available
    
    def check_multiple_usernames(self, platform, usernames):
        """Check multiple usernames using thread pool for faster processing"""
        print(f"\n{Fore.YELLOW if COLOR_SUPPORT else ''}Checking {len(usernames)} usernames on {platform.capitalize()}...{Style.RESET_ALL if COLOR_SUPPORT else ''}")
        self.available_usernames = []
        self.checked_count = 0
        self.total_usernames = len(usernames)
        
        # Warning about 2-letter usernames
        if len(usernames[0]) == 2:
            self.print_warning("Checking 2-letter usernames. These are rare and most are likely taken.")
            self.print_warning("This process might take longer due to rate limiting.")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda u: self.check_username(platform, u), usernames))
        
        print(f"\n{'=' * 50}")
        self.print_success(f"✓ Finished checking {len(usernames)} usernames on {platform.capitalize()}")
        
        if self.available_usernames:
            print(f"\n{Fore.CYAN if COLOR_SUPPORT else ''}Found {len(self.available_usernames)} available usernames:{Style.RESET_ALL if COLOR_SUPPORT else ''}")
            
            for i, username in enumerate(self.available_usernames, 1):
                color = self.rainbow.colors[i % len(self.rainbow.colors)] if COLOR_SUPPORT else ""
                print(f"{color}➤ {username}{Style.RESET_ALL if COLOR_SUPPORT else ''}")
        else:
            self.print_error("No available usernames found.")
        
        return self.available_usernames
    
    def save_results(self, platform, length):
        """Save results to a file with timestamp"""
        if not self.available_usernames:
            return None
            
        # Create a filename with platform name, length and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{platform}_{length}letter_usernames_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(f"Available {length}-letter usernames on {platform.capitalize()}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total checked: {self.total_usernames}\n")
            f.write(f"Total available: {len(self.available_usernames)}\n")
            f.write("=" * 40 + "\n\n")
            
            for username in self.available_usernames:
                f.write(f"{username}\n")
        
        return filename

def display_title():
    title_art = """
    ██████╗ ██╗     ███████╗ █████╗ ████████╗███████╗██████╗     
    ██╔══██╗██║     ██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗    
    ██████╔╝██║     █████╗  ███████║   ██║   █████╗  ██║  ██║    
    ██╔═══╝ ██║     ██╔══╝  ██╔══██║   ██║   ██╔══╝  ██║  ██║    
    ██║     ███████╗███████╗██║  ██║   ██║   ███████╗██████╔╝    
    ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝     
                                                                  
     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗      
    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗     
    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝     
    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗     
    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║     
     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     
                                                                  
    """
    rainbow = RainbowText()
    rainbow.animate_title(title_art)
    
    if COLOR_SUPPORT:
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Username Availability Checker | Find Available Usernames{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
    else:
        print("=" * 60)
        print("Username Availability Checker | Find Available Usernames")
        print("=" * 60)

def main():
    display_title()
    checker = UsernameChecker()
    
    # Platform selection
    print("Select a platform to check username availability:")
    if COLOR_SUPPORT:
        print(f"{Fore.RED}1. Reddit{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Spotify{Style.RESET_ALL}")
        print(f"{Fore.BLUE}3. Roblox{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Xbox{Style.RESET_ALL}")
    else:
        print("1. Reddit")
        print("2. Spotify")
        print("3. Roblox")
        print("4. Xbox")
    
    while True:
        choice = input("\nEnter your choice (1-4): ")
        if choice == "1":
            platform = "reddit"
            break
        elif choice == "2":
            platform = "spotify"
            break
        elif choice == "3":
            platform = "roblox"
            break
        elif choice == "4":
            platform = "xbox"
            break
        else:
            checker.print_error("Invalid choice. Please enter a number between 1 and 4.")
    
    # Username length
    while True:
        length = input("\nEnter username length (2, 3, or 4): ")
        if length in ["2", "3", "4"]:
            length = int(length)
            
            # Special warning for 2-letter usernames
            if length == 2:
                checker.print_warning("Note: 2-letter usernames are rare and highly sought after.")
                checker.print_warning("Most are likely already taken. Continue? (y/n)")
                confirm = input()
                if confirm.lower() != 'y':
                    continue
            break
        else:
            checker.print_error("Invalid length. Please enter 2, 3, or 4.")
    
    # Number of usernames to check
    max_suggestion = 100 if length == 2 else 1000
    while True:
        try:
            count = int(input(f"\nHow many {length}-letter usernames do you want to check? (suggested max: {max_suggestion}): "))
            if count > 0:
                if count > max_suggestion:
                    checker.print_warning(f"Checking more than {max_suggestion} usernames might get your IP rate-limited.")
                    confirm = input("Continue with checking this many usernames? (y/n): ")
                    if confirm.lower() != 'y':
                        continue
                
                # Special consideration for 2-letter usernames
                if length == 2:
                    total_combos = (len(string.ascii_lowercase) + len(string.digits)) ** 2
                    if count > total_combos:
                        checker.print_warning(f"There are only {total_combos} possible 2-letter combinations.")
                        count = total_combos
                        checker.print_warning(f"Setting count to maximum: {count}")
                
                break
            else:
                checker.print_error("Please enter a positive number.")
        except ValueError:
            checker.print_error("Please enter a valid number.")
    
    # Generate and check usernames
    usernames = checker.generate_usernames(length, count)
    available = checker.check_multiple_usernames(platform, usernames)
    
    # Save results to file
    if available:
        filename = checker.save_results(platform, length)
        if filename:
            checker.print_success(f"\n✓ Available usernames saved to {filename}")
    
    if COLOR_SUPPORT:
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Thank you for using Pleated Checker!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    else:
        print("\n" + "=" * 60)
        print("Thank you for using Pleated Checker!")
        print("=" * 60)

if __name__ == "__main__":
    main()