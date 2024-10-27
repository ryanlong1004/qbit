## Creating the `.env` file

To create a `.env` file for this script, follow these steps. The .env file will securely store sensitive configuration details required by the script, like your API connection credentials.

### Open a Text Editor:

Use any text editor, such as Notepad (Windows), TextEdit (Mac), or Vim/VSCode (Linux/Windows/Mac).
Define the Environment Variables:

### Add the following four lines to the file. Replace the placeholder values with your actual connection details:

```
HOST=your_api_host_url
PORT=your_api_port
USERNAME=your_username
PASSWORD=your_password
```

#### Here's a breakdown of each line:

- HOST: This should be the URL or IP address of the server hosting the API (e.g., http://localhost or https://api.example.com).
- PORT: Enter the port number for the API. Common values include 80 for HTTP, 443 for HTTPS, or a specific port your API uses.
- USERNAME: Your username for accessing the API.
- PASSWORD: The password associated with your username.

### Save the File:

Save this file as .env in the same directory where your script is located. Make sure it has no file extension (e.g., .txt).
Secure the .env File:

Since this file contains sensitive information, ensure it’s excluded from version control (e.g., by adding .env to your .gitignore file if using Git).
Restrict file permissions if you’re on a shared system to prevent unauthorized access.

### Example .env File

```
HOST=https://api.example.com
PORT=8080
USERNAME=yourUser
PASSWORD=yourSecretPassword
```

After creating this file, your script will automatically load these variables at runtime using load_dotenv(), and you’ll be ready to connect to the API securely.
