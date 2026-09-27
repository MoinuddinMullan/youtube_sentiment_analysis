import os

base_dir = r"d:\moin\youtube_sentiment_analysis\frontend"
src_dir = os.path.join(base_dir, "src")

dirs = [
    base_dir,
    src_dir,
    os.path.join(src_dir, "styles"),
    os.path.join(src_dir, "api"),
    os.path.join(src_dir, "components", "layout"),
    os.path.join(src_dir, "components", "ui"),
    os.path.join(src_dir, "components", "charts"),
    os.path.join(src_dir, "components", "comments"),
    os.path.join(src_dir, "components", "upload"),
    os.path.join(src_dir, "pages", "Dashboard"),
    os.path.join(src_dir, "pages", "Importer"),
    os.path.join(src_dir, "pages", "CommentExplorer"),
    os.path.join(src_dir, "pages", "Insights"),
    os.path.join(src_dir, "pages", "SingleAnalysis"),
    os.path.join(src_dir, "hooks"),
    os.path.join(src_dir, "utils"),
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

print("Directories created.")
