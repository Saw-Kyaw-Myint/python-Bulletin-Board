import os
import sys
import requests
from github import Github, GithubException


def main():
    try:
        # ========== ENV ==========
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
        PR_NUMBER = os.environ.get("PR_NUMBER")
        REPO = os.environ.get("REPO")

        if not all([GEMINI_API_KEY, GITHUB_TOKEN, PR_NUMBER, REPO]):
            raise ValueError("Missing required environment variables")

        PR_NUMBER = int(PR_NUMBER)

        # ========== GitHub ==========
        gh = Github(GITHUB_TOKEN)
        repo = gh.get_repo(REPO)
        pr = repo.get_pull(PR_NUMBER)

        # ========== Collect diffs ==========
        diffs = ""
        for file in pr.get_files():
            if file.filename.endswith(".py") and file.patch:
                diffs += f"\nFile: {file.filename}\n{file.patch}\n"

        if not diffs:
            print("No Python changes found")
            return

        # ========== Prompt ==========
        prompt = f"""
You are a senior Python Flask developer.
Review the following PR changes and give:

- Bugs
- Flask best practices
- Security issues
- Performance improvements

Return bullet points only.

Code:
{diffs}
"""

        # ========== Gemini API ==========
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            },
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Gemini API error {response.status_code}: {response.text}"
            )

        result = response.json()

        review = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text")
        )

        if not review:
            raise RuntimeError("Empty response from Gemini")

        # ========== Post PR Comment ==========
        pr.create_issue_comment(
            f"## 🤖 Gemini AI Code Review\n{review}"
        )

        print("✅ Gemini review posted successfully")

    except GithubException as e:
        print(f"❌ GitHub API error: {e}", file=sys.stderr)
        sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
