import hashlib
import json
import os
import shutil
import subprocess

import requests
from rich import print

# remove_dirs = ["/app/custom_nodes/ComfyUI_LLM"]
remove_dirs = []
root_app = "/app"

CACHE_DIR = "__deploy_cache__"
CACHE_FILE = os.path.join(CACHE_DIR, "file_hashes.json")


def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_cache():
    """Load cached file hashes"""
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(cache):
    """Save file hashes to cache"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def copy_file_to_container(container_id, file_path, cache):
    current_hash = calculate_file_hash(file_path)

    # Remove leading ./ if present and join with target directory
    cleaned_path = os.path.normpath(file_path).lstrip("./\\")
    target_dir = os.path.join("/app", os.path.dirname(cleaned_path))

    print(f"Copying {file_path} (modified)...")

    dir_cmd = f"docker exec {container_id} mkdir -p {target_dir}"
    subprocess.run(dir_cmd, shell=True, check=True)

    # Copy file to container
    cmd = f"docker cp {file_path} {container_id}:{target_dir}"
    subprocess.run(cmd, shell=True, check=True)

    # Update cache
    cache[file_path] = current_hash


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
        if "->8188/tcp" in line:
            container_id = line.split(" ")[0].strip()

    if not container_id:
        raise Exception("Could not find ComfyUI container. Is it running?")

    # Load cache
    cache = load_cache()

    # Get all files recursively in current directory
    file_list = []
    for root, dirs, files in os.walk("."):
        # Skip directories that shouldn't be deployed
        excluded_dirs = {".git", ".idea", "__deploy_cache__", "deploy.py"}
        if any(excluded in root for excluded in excluded_dirs):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            current_hash = calculate_file_hash(file_path)
            # Skip if file hasn't changed
            if file_path not in cache or cache[file_path] != current_hash:
                file_list.append(file_path)

    if len(file_list) == 0:
        print("No files have changed. Nothing to deploy.")
        exit()

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
            copy_file_to_container(container_id, file_path, cache)
        except subprocess.CalledProcessError as e:
            print(f"[red]Error copying {file_path}: {e}[/red]")
            exit(1)
    save_cache(cache)

    # Install requirements in container
    print("\n[bold]Installing requirements...[/bold]")
    try:
        cmd = f"docker exec {container_id} sh -c 'cd /app/custom_nodes/ComfyUI_LLM && python -m pip install -r requirements.txt'"
        subprocess.run(cmd, shell=True, check=True)
        print("[green]Requirements installed successfully![/green]")
    except subprocess.CalledProcessError as e:
        print(f"[red]Error installing requirements: {e}[/red]")
        exit(1)

    print("[green]Deployment completed successfully![/green]")

    # Add restart step
    print("\n[bold]Restarting ComfyUI...[/bold]")
    try:
        requests.get("http://localhost:8188/api/manager/reboot")
    except requests.exceptions.RequestException:
        pass
    print("[green]ComfyUI restart initiated successfully![/green]")
    # Delete local web directory
    try:
        shutil.rmtree("./web")
    except:
        pass
