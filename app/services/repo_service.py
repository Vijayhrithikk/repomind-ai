from pathlib import Path
import tempfile

from git import Repo

class RepoService:
    def clone_repo(self,url: str) -> str:
        temp_dir=tempfile.mkdtemp()
        Repo.clone_from(url,temp_dir)
        return temp_dir
    
    def get_go_files(self,repo_path: str):

        repo = Path(repo_path)

        return list(repo.rglob("*.go"))

