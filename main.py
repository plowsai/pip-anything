import gitpython
import subprocess
import argparse
import tempfile

def clone_repo(repo_url, local_path):
    gitpython.Repo.clone_from(repo_url, local_path)

def generate_setup_py(local_path, package_name, version, description, author, author_email):
    setup_py_content = f"""from setuptools import setup, find_packages

setup(
    name='{package_name}',
    version='{version}',
    description='{description}',
    author='{author}',
    author_email='{author_email}',
    packages=find_packages(),
    install_requires=[],
)
"""
    with open(f'{local_path}/setup.py', 'w') as f:
        f.write(setup_py_content)

def create_readme(local_path, package_name):
    readme_content = f"""# {package_name}

This is a Python package generated from a GitHub repository.

## Installation

"""
    with open(f'{local_path}/README.md', 'w') as f:
        f.write(readme_content)

def package_project(local_path):
    subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], cwd=local_path)

def install_package(local_path):
    subprocess.run(['pip', 'install', '.'], cwd=local_path)

def main():
    parser = argparse.ArgumentParser(description='Turn a GitHub repo into a Python package and install it globally.')
    parser.add_argument('repo_url', help='The URL of the GitHub repository.')
    parser.add_argument('package_name', help='The desired package name.')
    args = parser.parse_args()

    # Prompt the user for package details
    version = input("Enter the package version (default: 0.1.0): ") or '0.1.0'
    description = input("Enter the package description: ")
    author = input("Enter the package author: ")
    author_email = input("Enter the package author's email: ")

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone the repository into the temporary directory
        clone_repo(args.repo_url, temp_dir)
        # Generate setup.py and README.md
        generate_setup_py(temp_dir, args.package_name, version, description, author, author_email)
        create_readme(temp_dir, args.package_name)
        # Package the project
        package_project(temp_dir)
        # Install the package globally
        install_package(temp_dir)

    print(f"Package '{args.package_name}' installed globally.")

if __name__ == '__main__':
    main()
