import importlib.metadata

def read_requirements(file_path):
    with open(file_path, 'r') as f:
        requirements = f.readlines()
    return [req.strip() for req in requirements if req.strip()]

packages = read_requirements('requirements.txt')

print("Packages from requirements.txt:",packages)

# Remove "-e ." fom the list

if "-e ." in packages:
    packages.remove("-e .")

for pkg in packages:
    try:
        version = importlib.metadata.version(pkg)
        print(f"{pkg}=={version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{pkg} (not installed)")