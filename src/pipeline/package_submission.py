"""
Automated Submission Packaging Script (Section 5: Deliverables Packaging)
Bundles all deliverables into lanna_power_outage_submission.zip
according to the official competition folder structure.
"""

import os
import zipfile

def package_submission():
    base_dir = r"C:\Users\Surface\Documents\MrG"
    output_zip = os.path.join(base_dir, "lanna_power_outage_submission.zip")
    
    # Target directories to include
    include_dirs = ["data", "docs", "notebooks", "src"]
    include_files = [
        "package.json", "next.config.js", "tailwind.config.js",
        "postcss.config.js", "Dockerfile", "run_local.bat", "README.md", "AGENTS.md"
    ]

    print("Creating submission archive...")
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        # Add files from directories
        for d in include_dirs:
            full_d = os.path.join(base_dir, d)
            if not os.path.exists(full_d):
                continue
            for root, _, files in os.walk(full_d):
                for f in files:
                    file_path = os.path.join(root, f)
                    rel_path = os.path.relpath(file_path, base_dir)
                    z.write(file_path, rel_path)
                    print(f"  Added: {rel_path}")

        # Add root configuration files
        for f in include_files:
            file_path = os.path.join(base_dir, f)
            if os.path.exists(file_path):
                z.write(file_path, f)
                print(f"  Added: {f}")

    size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f"\nSUCCESS: Created {output_zip} ({size_mb:.2f} MB)")
    return output_zip

if __name__ == "__main__":
    package_submission()
