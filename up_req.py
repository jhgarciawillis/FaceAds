import pkg_resources
import re
import os
import sys
import subprocess

def update_requirements_file(requirements_path):
    # Check if we're in a virtual environment
    in_virtualenv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_virtualenv:
        print(f"Running in virtual environment: {sys.prefix}")
    else:
        print("Warning: Not running in a virtual environment. This might update requirements based on system packages.")
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Alternative method to get installed packages using pip freeze
    try:
        installed_packages = {}
        pip_freeze_output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8')
        
        for line in pip_freeze_output.splitlines():
            if '==' in line:
                package_name, version = line.split('==', 1)
                installed_packages[package_name.lower()] = version
        
        print(f"Found {len(installed_packages)} installed packages in environment")
    except Exception as e:
        print(f"Warning: Could not get installed packages using pip freeze. Using pkg_resources instead. Error: {e}")
        installed_packages = None
    
    # Read existing requirements file
    with open(requirements_path, 'r') as f:
        requirements = f.readlines()
    
    updated_requirements = []
    
    for req in requirements:
        req = req.strip()
        if not req or req.startswith('#'):
            updated_requirements.append(req)
            continue
        
        # Extract package name and version specifier
        match = re.match(r'^([a-zA-Z0-9_\-\.]+)([<>=~!].*)$', req)
        if match:
            package_name = match.group(1)
        else:
            package_name = req
        
        try:
            # Try to get version from pip freeze first (more reliable in virtual envs)
            if installed_packages is not None and package_name.lower() in installed_packages:
                installed_version = installed_packages[package_name.lower()]
                updated_req = f"{package_name}=={installed_version}"
                updated_requirements.append(updated_req)
                print(f"Updated: {req} -> {updated_req}")
            else:
                # Fallback to pkg_resources
                installed_version = pkg_resources.get_distribution(package_name).version
                updated_req = f"{package_name}=={installed_version}"
                updated_requirements.append(updated_req)
                print(f"Updated: {req} -> {updated_req}")
        except pkg_resources.DistributionNotFound:
            updated_requirements.append(req)
            print(f"Package not installed, keeping: {req}")
        except Exception as e:
            updated_requirements.append(req)
            print(f"Error processing {req}: {str(e)}")
    
    # Write updated requirements
    with open(requirements_path, 'w') as f:
        f.write('\n'.join(updated_requirements) + '\n')
    
    print(f"\nUpdated requirements saved to {requirements_path}")

if __name__ == "__main__":
    requirements_path = "requirements.txt"
    if not os.path.exists(requirements_path):
        requirements_path = input("Enter path to requirements.txt: ")
    
    update_requirements_file(requirements_path)