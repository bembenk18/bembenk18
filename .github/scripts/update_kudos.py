import json
import re
import urllib.request

USERNAME = "bembenk"
API_URL = f"https://kudos.opensuse.org/api/badges/user/{USERNAME}"

def main():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "GitHub-Action-Kudos-Updater"})
    with urllib.request.urlopen(req) as resp:
        badges = json.loads(resp.read().decode("utf-8"))

    html_parts = []
    for b in badges:
        title = b.get("title", "")
        share_url = b.get("shareUrl") or b.get("permalink") or f"https://kudos.opensuse.org/badge/{b.get('slug')}/earned-by/{USERNAME}/share"
        picture = b.get("picture", "")
        if picture.startswith("/badges/"):
            pic = picture.replace("/badges/", "/badges/previews/800/")
        else:
            pic = picture
        img_url = f"https://kudos.opensuse.org{pic}"
        html_parts.append(
            f'  <a href="{share_url}" target="_blank" rel="noopener noreferrer">\n'
            f'    <img src="{img_url}" width="115" alt="{title}" title="{title}" />\n'
            f'  </a>'
        )

    badges_html = "\n  &nbsp;\n".join(html_parts)
    replacement = (
        "<!-- KUDOS_BADGES:START -->\n"
        f"{badges_html}\n"
        "  <p>\n"
        f'    <sub>Verified on <a href="https://kudos.opensuse.org/user/{USERNAME}" target="_blank" rel="noopener noreferrer">openSUSE Kudos</a></sub>\n'
        "  </p>\n"
        "  <!-- KUDOS_BADGES:END -->"
    )

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r"<!-- KUDOS_BADGES:START -->.*?<!-- KUDOS_BADGES:END -->", re.DOTALL)
    if not pattern.search(content):
        print("Marker <!-- KUDOS_BADGES:START --> not found in README.md")
        return

    updated_content = pattern.sub(replacement, content)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("README.md successfully updated with latest kudos badges.")

if __name__ == "__main__":
    main()
