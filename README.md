# Advanced SSH Brute Force Tool

## Overview

The Advanced SSH Brute Force Tool is intended for use in security testing environments and for educational purposes. It makes use of sophisticated capabilities to try SSH brute-force assaults, making efficient use of multi-threaded operations and a polished user interface.

**Disclaimer:** Unauthorized access to computer systems is illegal and unethical. This tool is intended solely for use in authorized security testing and educational environments.

## Features

- **Advanced Encryption**: Utilizes Fernet encryption for secure management of sensitive data.
- **Multi-Protocol Support**: Allows selection between SSH, FTP, and HTTP for attacks (currently focused on SSH).
- **Dynamic Progress Tracking**: Includes a dynamic progress bar to monitor the status of brute-force attacks.
- **Customizable Credentials**: Supports single or multiple usernames and passwords.
- **Automated Results Saving**: Automatically saves successful credentials with timestamped filenames.
- **Professional UI**: Enhanced user interface with color-coded outputs and clear instructions.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/nexussecelite/Advanced-SSH-Brute-Force-Tool.git
   cd Advanced-SSH-Brute-Force-Tool
   ```

2. **Install Dependencies**

   Ensure you have `pip` installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

   Dependencies include:
   - `paramiko` for SSH connections.
   - `tqdm` for progress bars.
   - `cryptography` for encryption.
   - `colorama` for colored terminal output.

## Usage

1. **Run the Tool**

   ```bash
   python brute_force_tool.py
   ```

2. **Follow the Prompts**

   The tool will prompt you for the following inputs:
   - **Target Host IP**: The IP address of the SSH server you wish to test.
   - **Port**: The port number for SSH (default is 22).
   - **Number of Threads**: The number of concurrent threads to use (default is 10).
   - **Username Input Method**: Choose between 'single' for one username or 'multi' for a list of usernames.
   - **Username List File (if 'multi' is selected)**: Path to the file containing a list of usernames.
   - **Password List File**: Path to the file containing a list of passwords.

3. **View Results**

   Successful login attempts will be displayed and saved in a file named `results_<host>_<timestamp>.txt`.

## Example

```bash
Enter the target Host IP: 192.168.1.100
Enter the port (default 22 for SSH): 22
Enter the number of threads to use (default 10): 10
Enter 'single' for a single username or 'multi' for a list of usernames: multi
Enter the path to the username list file: usernames.txt
Enter the path to the password list file: passwords.txt
```

## Advanced Configuration

- **Encryption Key Management**: The encryption key (`FERNET_KEY`) can be configured for managing encrypted data. Modify the `FERNET_KEY` value in the script as needed.
- **Logging**: Detailed logs are stored in `advanced_tool.log` for troubleshooting and record-keeping.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes. Ensure that your contributions align with the tool’s intended educational and ethical use.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact at [hello@nexussec.in].
