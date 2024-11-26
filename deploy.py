import subprocess


if __name__ == "__main__":
    cmd = "docker ps"
    output = subprocess.check_output(cmd, shell=True)
    print(output.decode())
