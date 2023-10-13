import subprocess

# List of commands to run
commands = [
    ".\\parse-yahoo-com.py",
    ".\\parse-aol-com.py",
    ".\\parse-ask-com.py",
    ".\\parse-bing-com.py",
    ".\\parse-ecosia-org.py",
    ".\\parse-google-com.py",
]

# Iterate through the list of commands and run them one by one
for command in commands:
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Return code: {e.returncode}")
        # You can handle the error as needed

print("All commands have been executed.")
