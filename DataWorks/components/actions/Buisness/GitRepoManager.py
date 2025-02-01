import os
import shutil
from urllib.parse import urlparse
from dataclasses import dataclass
from DataWorks.logger import logging

@dataclass
class GitRepoManager:
    repo_url: str
    commit_message: str = "DataWorks commit"
    branch: str = "main"

    def clone_and_commit(self) -> bool:
        if not self.repo_url:
            raise ValueError("Repo URL must be specified")

        github_token = os.environ.get("PAT_TOKEN_GITHUB")
        if not github_token:
            logging.error("Error: GITHUB_TOKEN is not set!")
            return False

        repo_name = os.path.basename(self.repo_url).replace(".git", "")

        # Remove existing repo folder if it exists
        if os.path.exists(repo_name):
            shutil.rmtree(repo_name)

        # Format authenticated URL
        parsed_url = urlparse(self.repo_url)
        auth_url = f"https://{github_token}@{parsed_url.netloc}{parsed_url.path}"

        logging.info(f"Cloning repository: {auth_url}")
        os.system(f"git clone {auth_url}")

        os.chdir(repo_name)
        os.system(f"git checkout {self.branch}")
        os.system(f"echo {self.commit_message} > random_.txt")
        os.system("git add .")
        os.system(f'git commit -am "{self.commit_message}"')
        os.system("git push -u origin main")

        logging.info(f"{self.repo_url} cloned and changes committed successfully")
