"""Copy the shared release docs into a release worktree and patch its README
with the synchronized required sections (language-specific install/quickstart
stay untouched)."""
import shutil
import sys

wt = sys.argv[1]
for doc in ("ARCHITECTURE.md", "CERTIFICATION.md", "AI_AGENT_GUIDE.md",
            "API_REFERENCE.md"):
    shutil.copy(doc, f"{wt}/{doc}")

ADD = open('README.md', encoding='utf-8').read()
start = ADD.index('## Cross-language parity & certification')
end = ADD.index('## License')
block = ADD[start:end]

readme = open(f"{wt}/README.md", encoding='utf-8', newline='').read()
if '## Cross-language parity & certification' not in readme:
    if '## License' in readme:
        readme = readme.replace('## License', block + '## License', 1)
    else:
        readme = readme + '\n\n' + block
open(f"{wt}/README.md", 'w', encoding='utf-8', newline='').write(readme)
print(f"docs synced -> {wt}")
