import os
import subprocess

from rich import print

if __name__ == "__main__":
    # Export requirements.txt from poetry
    subprocess.run(
        [
            "poetry",
            "export",
            "-f",
            "requirements.txt",
            "--output",
            "requirements.txt",
            "--without-hashes",
        ],
        check=True,
    )

    cmd = "docker ps"
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode().split("\n")
    container_id = None

    for line in lines:
        if "comfyui-comfyui" in line:
            container_id = line.split(" ")[0].strip()

    if not container_id:
        raise Exception("Could not find ComfyUI container. Is it running?")

    # Get all files recursively in current directory
    file_list = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".idea" in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    print("[bold]Files to deploy:[/bold]")
    for file_path in file_list:
        print(f"└── {file_path}")
    # Ask for confirmation before proceeding
    confirmation = input("Do you want to proceed with deployment? (yes/no): ").lower()
    if confirmation != "yes":
        print("Deployment cancelled.")
        exit()
