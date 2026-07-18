import git
from pathlib import Path

def clone_repository(repo_url: str) -> str:
    
    repo_name = repo_url.split('/')[-1].replace(".git", "")
    destination_path = Path("../repositories") / repo_name

    try:
        repo = git.Repo.clone_from(repo_url, destination_path)
        print(f"Cloned into {destination_path}")
        return str(destination_path)

    except git.exc.GitCommandError as e:
        print(f"Failed to clone {e}")
        return None