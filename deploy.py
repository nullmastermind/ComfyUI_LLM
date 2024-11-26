import os
import subprocess

from rich import print


def copy_file_to_container(container_id, file_path):
    # Remove leading ./ if present and join with target directory
    cleaned_path = os.path.normpath(file_path).lstrip("./\\")
    target_dir = os.path.join(
        "/app/custom_nodes/ComfyUI_LLM", os.path.dirname(cleaned_path)
    )

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
