# Remove "No items to show" message from 1Password extension

A cross-platform Python utility to modify Chrome extension with ID `aeblfdkhhhdcdjpifhhbdiojplfjncoa` (1Password – Password Manager) by updating specific UI components to improve user experience.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Automated Method](#automated-method)
  - [Manual Method](#manual-method)
- [What This Modification Does](#what-this-modification-does)
- [Supported Platforms](#supported-platforms)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- ✅ Automatically detects Chrome profiles with the extension installed
- ✅ Shows profile names for easy identification
- ✅ Works on Windows, macOS, and Linux
- ✅ Modifies specific HTML and JavaScript files to hide UI elements
- ✅ Provides clear instructions for loading the modified extension
- ✅ Creates backups of original files before modifications

## Usage

### Automated Method

1. Run the script:
   ```
   python3 1password_chrome_extension_patched.py
   ```

2. The script will automatically:
   - Detect your Chrome User Data directory
   - Find all profiles with the extension installed
   - Display a list of profiles to choose from

3. Select a profile by entering its number

4. After the script completes the modifications, follow the on-screen instructions to:
   - Go to `chrome://extensions/`
   - Enable Developer mode
   - Click "Load unpacked"
   - Select the folder indicated by the script

#### Result
- Before

![image](https://github.com/user-attachments/assets/35444af4-baa5-48d7-8e7f-fc984ed08b10)

- After

![image](https://github.com/user-attachments/assets/e9e9d979-c485-4920-ab04-472c17237268)



### Manual Method

If you prefer to make the changes manually, follow these steps:

1. Locate the extension files on your system:

   - **Windows**: `C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\<Profile>\Extensions\aeblfdkhhhdcdjpifhhbdiojplfjncoa\`
   - **macOS**: `/Users/<YourUsername>/Library/Application Support/Google/Chrome/<Profile>/Extensions/aeblfdkhhhdcdjpifhhbdiojplfjncoa/`
   - **Linux**: `/home/<YourUsername>/.config/google-chrome/<Profile>/Extensions/aeblfdkhhhdcdjpifhhbdiojplfjncoa/`

2. Inside this folder, find the version folder (e.g., `8.10.72.27_0`)

3. Modify the `menu.html` file:
   - Path: `<version_folder>/inline/menu/menu.html`
   - Replace:
     ```html
     <body>
         <script type="module" src="./menu.js"></script>
     </body>
     ```
   - With:
     ```html
     <body>
     </body>
     <script type="module" src="./menu.js"></script>
     ```

4. Modify the `menu.js` file:
   - Path: `<version_folder>/inline/menu/menu.js`
   - Replace:
     ```javascript
     function _k(e){let n,r;return{c(){n=R("section"),r=R("p"),r.textContent=`${e[2]("No items to show.")}`,h(n,"class","emptyItemList")},m(t,o){E(t,n,o),H(n,r)},p:S,i:S,o:S,d(t){t&&C(n)}}}
     ```
   - With:
     ```javascript
     function _k(e){return{c(){},m(t,o){document.body.style.display='none'},p:S,i:S,o:S,d(t){document.body.style.display=''}}}
     ```

5. Load the modified extension:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" using the toggle in the top-right corner
   - Click the "Load unpacked" button
   - Navigate to and select the version folder

## Supported Platforms

- ✅ Windows
- ✅ macOS
- ✅ Linux

The script automatically detects the appropriate paths for each operating system.

## Troubleshooting

### Common Issues:

- **Cannot find Chrome User Data directory**: The script will prompt you to enter the path manually
- **Extension not working after modification**: Make sure Chrome was completely closed before loading the unpacked extension
- **Cannot find the extension in any profile**: Verify that the extension is installed in at least one Chrome profile
- **Permission issues**: Try running the script with administrator privileges

### For Additional Help:

- Check Chrome's developer tools console for any error messages
- Verify the modifications were correctly applied to the files
- Make sure you're selecting the correct folder when using "Load unpacked"

## License

MIT
