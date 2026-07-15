import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <number> <directory>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("First argument must be an integer")
        sys.exit(1)
    directory = sys.argv[2]
    with open("disks", "w") as f:
        for _ in range(n):
            f.write(directory + "\n")
    print(f"Written '{directory}' {n} times to disks")

if __name__ == "__main__":
    main()
