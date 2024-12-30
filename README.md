Web Information Tool Guide


Prerequisites

Ensure Python 3 is installed on your system.
Install the required Python libraries:

bash
Copy code
pip install requests beautifulsoup4




Run the tool with a target URL:

bash

Copy code
python tool.py <URL>


Example:

bash
Copy code
python tool.py https://example.com


Fetch Directory Information (Optional)


To enumerate directories, provide a wordlist using the --wordlist option:

bash
Copy code
python tool.py <URL> --wordlist <path_to_wordlist>

Example:

bash
Copy code
python tool.py https://example.com --wordlist /path/to/wordlist.txt
