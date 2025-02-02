import os
import shutil
from pathlib import Path

def create_directory_structure():
    base_dir = Path('/Users/sohag/Projects/CareerCanvas/CareerCanvas.Jobs')
    
    directories = [
        'config/settings',
        'services/job_api/routes',
        'services/job_scraper/providers',
        'services/shared/database',
        'services/shared/middleware',
        'services/shared/utils',
        'tests/integration/services',
        'tests/unit/services',
        'scripts',
        'deployment/docker',
        'deployment/kubernetes',
        'deployment/terraform'
    ]
    
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        (full_path / '__init__.py').touch()

if __name__ == "__main__":
    create_directory_structure()