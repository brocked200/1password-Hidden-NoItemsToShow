import os
import sys
import getpass
import shutil
import json
from pathlib import Path

def find_chrome_user_data():
    """Find the Chrome User Data directory based on current operating system and username."""
    import platform
    system = platform.system()
    username = getpass.getuser()
    
    user_data_path = None
    
    if system == "Windows":
        # Windows path
        user_data_path = Path(f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data")
        if not user_data_path.exists():
            # Try alternative path for some Windows installs
            user_data_path = Path(f"C:\\Users\\{username}\\Local Settings\\Application Data\\Google\\Chrome\\User Data")
    
    elif system == "Darwin":
        # macOS path
        user_data_path = Path(f"/Users/{username}/Library/Application Support/Google/Chrome")
        if not user_data_path.exists():
            # Try Chromium path
            user_data_path = Path(f"/Users/{username}/Library/Application Support/Chromium")
    
    elif system == "Linux":
        # Linux path
        user_data_path = Path(f"/home/{username}/.config/google-chrome")
        if not user_data_path.exists():
            # Try Chromium path
            user_data_path = Path(f"/home/{username}/.config/chromium")
    
    if user_data_path and user_data_path.exists():
        print(f"Found Chrome User Data directory at: {user_data_path}")
        return user_data_path
    else:
        print(f"Chrome User Data directory not found for {system} system.")
        
        # Ask user to provide the path
        print("\nPlease enter the full path to Chrome User Data directory:")
        custom_path = input("> ").strip()
        
        if custom_path:
            custom_path = Path(custom_path)
            if custom_path.exists():
                print(f"Using custom path: {custom_path}")
                return custom_path
            else:
                print(f"The provided path does not exist: {custom_path}")
        
        return None

def get_profile_name_from_local_state(user_data_path, profile_id):
    """Get profile name from the Local State file for a specific profile ID."""
    local_state_path = user_data_path / "Local State"
    
    try:
        if local_state_path.exists():
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
                
                # Get profile info from profile.info_cache in Local State
                if 'profile' in local_state and 'info_cache' in local_state['profile']:
                    info_cache = local_state['profile']['info_cache']
                    
                    # Get shortcut_name for the specific profile
                    if profile_id in info_cache and 'shortcut_name' in info_cache[profile_id]:
                        return info_cache[profile_id]['shortcut_name']
    except Exception as e:
        print(f"Error reading Local State file: {e}")
    
    # Return the profile ID if no name was found
    return profile_id

def find_extension_in_profiles(user_data_path, extension_id):
    """Find profiles containing the specified extension."""
    profiles_with_extension = []
    
    # Look for folders that could be profiles (Default, Profile 1, etc.)
    potential_profiles = [d for d in user_data_path.iterdir() 
                        if d.is_dir() and (d.name == "Default" or d.name.startswith("Profile "))]
    
    print(f"Found {len(potential_profiles)} potential Chrome profiles.")
    
    for profile_path in potential_profiles:
        extension_path = profile_path / "Extensions" / extension_id
        
        if extension_path.exists():
            # Get profile name from Local State only for profiles that have the extension
            friendly_name = get_profile_name_from_local_state(user_data_path, profile_path.name)
            
            profiles_with_extension.append({
                "profile_name": profile_path.name,
                "friendly_name": friendly_name,
                "extension_path": extension_path
            })
            print(f"Found extension in profile: {profile_path.name}")
    
    return profiles_with_extension

def get_latest_version_path(extension_path):
    """Get the path to the latest version folder of the extension."""
    version_folders = [d for d in extension_path.iterdir() if d.is_dir()]
    
    if not version_folders:
        print(f"No version folders found in {extension_path}")
        return None
    
    # Sort by name - this works for version numbers like "8.10.72.27_0"
    latest_version = sorted(version_folders)[-1]
    print(f"Using latest version: {latest_version.name}")
    
    return latest_version

def modify_menu_files(version_path):
    """Modify the menu.html and menu.js files."""
    import platform
    
    # Use proper path separator based on OS
    if platform.system() == "Windows":
        menu_html_path = version_path / "inline" / "menu" / "menu.html"
        menu_js_path = version_path / "inline" / "menu" / "menu.js"
    else:
        menu_html_path = version_path / "inline" / "menu" / "menu.html"
        menu_js_path = version_path / "inline" / "menu" / "menu.js"
    
    # Check if the files exist
    if not menu_html_path.exists():
        print(f"menu.html not found at: {menu_html_path}")
        return False
    
    if not menu_js_path.exists():
        print(f"menu.js not found at: {menu_js_path}")
        return False
    
    # Create backups
    shutil.copy(menu_html_path, str(menu_html_path) + ".backup")
    shutil.copy(menu_js_path, str(menu_js_path) + ".backup")
    print("Created backups of menu.html and menu.js")
    
    # Modify menu.html
    try:
        with open(menu_html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        new_html_content = html_content.replace(
            "<body>\n\t\t<script type=\"module\" src=\"./menu.js\"></script>\n\t</body>",
            "<body>\n\t</body>\n\t<script type=\"module\" src=\"./menu.js\"></script>"
        )
        
        with open(menu_html_path, 'w', encoding='utf-8') as file:
            file.write(new_html_content)
        
        print("Successfully modified menu.html")
        
        # Verify the changes
        with open(menu_html_path, 'r', encoding='utf-8') as file:
            updated_html = file.read()
        if "<body>\n\t</body>\n\t<script type=\"module\" src=\"./menu.js\"></script>" in updated_html:
            print("Verified: menu.html has been updated correctly")
        else:
            print("Warning: menu.html might not have been updated correctly")
    
    except Exception as e:
        print(f"Error modifying menu.html: {str(e)}")
        return False
    
    # Modify menu.js
    try:
        with open(menu_js_path, 'r', encoding='utf-8') as file:
            js_content = file.read()
        
        new_js_content = js_content.replace(
            "function _k(e){let n,r;return{c(){n=R(\"section\"),r=R(\"p\"),r.textContent=`${e[2](\"No items to show.\")}`,h(n,\"class\",\"emptyItemList\")},m(t,o){E(t,n,o),H(n,r)},p:S,i:S,o:S,d(t){t&&C(n)}}}",
            "function _k(e){return{c(){},m(t,o){document.body.style.display='none'},p:S,i:S,o:S,d(t){document.body.style.display=''}}}"
        )
        
        with open(menu_js_path, 'w', encoding='utf-8') as file:
            file.write(new_js_content)
        
        print("Successfully modified menu.js")
        
        # Verify the changes
        with open(menu_js_path, 'r', encoding='utf-8') as file:
            updated_js = file.read()
        if "function _k(e){return{c(){},m(t,o){document.body.style.display='none'},p:S,i:S,o:S,d(t){document.body.style.display=''}}}" in updated_js:
            print("Verified: menu.js has been updated correctly")
        else:
            print("Warning: menu.js might not have been updated correctly")
    
    except Exception as e:
        print(f"Error modifying menu.js: {str(e)}")
        return False
    
    return True

def display_load_instructions(extension_path):
    """Display instructions for loading the unpacked extension."""
    import platform
    
    system = platform.system()
    
    # Adjust instructions based on OS
    if system == "Windows":
        extensions_url = "chrome://extensions/"
        developer_mode_location = "top-right corner"
    elif system == "Darwin":  # macOS
        extensions_url = "chrome://extensions/"
        developer_mode_location = "top-right corner"
    else:  # Linux
        extensions_url = "chrome://extensions/"
        developer_mode_location = "top-right corner"
    
    instruction_text = f"""
==========================================================================
                    \033[31m[NEXT STEP - DON'T SKIP IT]\033[0m
                HOW TO LOAD THE MODIFIED EXTENSION
==========================================================================

1. First, open Chrome browser and go to: {extensions_url}

2. Enable "Developer mode" using the toggle in the {developer_mode_location}

3. Click the "Load unpacked" button that appears below

4. Navigate to and select this folder:
   
   >>> {extension_path} <<<

5. Done! The modified extension is now loaded and ready to use.
   Enjoy your enhanced browsing experience!

==========================================================================
    """
    print(instruction_text)
    return True

def main():
    """Main function for the Chrome Extension Modifier."""
    import platform
    
    # Print system information
    system = platform.system()
    print(f"Operating System: {system}")
    
    # Extension ID to look for
    extension_id = "aeblfdkhhhdcdjpifhhbdiojplfjncoa"
    
    # Find Chrome User Data directory
    user_data_path = find_chrome_user_data()
    if not user_data_path:
        print("Cannot proceed without Chrome User Data directory.")
        sys.exit(1)
    
    # Find profiles with the extension
    profiles_with_extension = find_extension_in_profiles(user_data_path, extension_id)
    
    if not profiles_with_extension:
        print(f"Extension {extension_id} not found in any Chrome profile.")
        sys.exit(1)
    
    # Let user select a profile
    print("\nProfiles containing the extension:")
    for i, profile in enumerate(profiles_with_extension):
        friendly_name = profile['friendly_name']
        profile_name = profile['profile_name']
        
        # Display both the technical name and the profile name if different
        if friendly_name != profile_name:
            print(f"{i+1}. {profile_name} - Name: '{friendly_name}'")
        else:
            print(f"{i+1}. {profile_name}")
    
    selection = 0
    while selection < 1 or selection > len(profiles_with_extension):
        try:
            selection = int(input(f"\nSelect a profile (1-{len(profiles_with_extension)}): "))
        except ValueError:
            print("Please enter a number.")
    
    selected_profile = profiles_with_extension[selection-1]
    print(f"\nSelected profile: {selected_profile['profile_name']}")
    if selected_profile['friendly_name'] != selected_profile['profile_name']:
        print(f"Profile name: '{selected_profile['friendly_name']}'")
    
    # Get the latest version path
    version_path = get_latest_version_path(selected_profile['extension_path'])
    if not version_path:
        print("Cannot proceed without a valid extension version.")
        sys.exit(1)
    
    # Modify the files
    if modify_menu_files(version_path):
        
        print("\n" + "="*70)
        print(f"Modification completed successfully!")
        print(f"Modified extension at: \033[1;32m{version_path}\033[0m")
        print("="*70 + "\n")
        
        # Display instructions for loading the unpacked extension
        display_load_instructions(version_path)
    else:
        print("\nModification failed.")

if __name__ == "__main__":
    print("Chrome Extension Modifier")
    print("=========================")
    main()