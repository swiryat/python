# export_requirements.py
import sys
import pkg_resources

site_packages = r"C:\Users\swer\AppData\Local\Programs\Python\Python312\Lib\site-packages"
sys.path.insert(0, site_packages)

with open("foreign_requirements.txt", "w", encoding="utf-8") as f:
    for dist in pkg_resources.working_set:
        f.write(f"{dist.project_name}=={dist.version}\n")
