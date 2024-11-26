import os
import subprocess

import requests
from rich import print

remove_dirs = ["/app/custom_nodes/ComfyUI_LLM"]
root_app = "/app"


def copy_file_to_container(container_id, file_path):
    # Remove leading ./ if present and join with target directory
    cleaned_path = os.path.normpath(file_path).lstrip("./\\")
    target_dir = os.path.join("/app", os.path.dirname(cleaned_path))

    print("target_dir:", target_dir)

    dir_cmd = f"docker exec {container_id} mkdir -p {target_dir}"
    subprocess.run(dir_cmd, shell=True, check=True)

    # Copy file to container
    cmd = f"docker cp {file_path} {container_id}:{target_dir}"
    subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    # Export requirements.txt from poetry
    subprocess.run(
        [
            "poetry",
            "export",
            "-f",
            "requirements.txt",
            "--output",
            "custom_nodes/ComfyUI_LLM/requirements.txt",
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
    confirmation = input("Do you want to proceed with deployment? ([y]/n): ").lower()
    if confirmation == "" or confirmation == "yes" or confirmation == "y":
        pass
    else:
        print("Deployment cancelled.")
        exit()

    # Remove existing directories in container
    print("\n[bold]Removing existing directories...[/bold]")
    for dir_path in remove_dirs:
        try:
            subprocess.run(
                f"docker exec {container_id} rm -rf {dir_path}",
                shell=True,
                check=True,
            )
            print(f"Removed {dir_path}")
        except:
            pass

    # Copy each file to the container
    print("\n[bold]Deploying files...[/bold]")
    for file_path in file_list:
        try:
            print(f"Copying {file_path}...")
            copy_file_to_container(container_id, file_path)
        except subprocess.CalledProcessError as e:
            print(f"[red]Error copying {file_path}: {e}[/red]")
            exit(1)

    print("[green]Deployment completed successfully![/green]")

    # Add restart step
    print("\n[bold]Restarting ComfyUI...[/bold]")
    try:
        requests.get("http://localhost:8188/api/manager/reboot")
    except requests.exceptions.RequestException:
        pass
    print("[green]ComfyUI restart initiated successfully![/green]")
