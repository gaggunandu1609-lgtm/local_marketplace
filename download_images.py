import urllib.request
import os

media_path = "media/services"
os.makedirs(media_path, exist_ok=True)

images = {
    "carpentry.jpg": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&q=80&w=600",
    "painting.jpg": "https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&q=80&w=600",
    "appliance.jpg": "https://images.unsplash.com/photo-1550624239-ce541c039f29?auto=format&fit=crop&q=80&w=600"
}

# Add some portfolio images too
portfolio_path = "media/portfolio"
os.makedirs(portfolio_path, exist_ok=True)
portfolio_images = {
    "p1.jpg": "https://images.unsplash.com/photo-1581578731522-74b74a4d9542?auto=format&fit=crop&q=80&w=600",
    "p2.jpg": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&q=80&w=600",
    "p3.jpg": "https://images.unsplash.com/photo-1541123437800-1bb1317badc2?auto=format&fit=crop&q=80&w=600"
}

def download(urls, base_dir):
    for filename, url in urls.items():
        path = os.path.join(base_dir, filename)
        print(f"Downloading {filename}...")
        try:
            # Add user-agent to avoid being blocked
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"  Saved to {path}")
        except Exception as e:
            print(f"  Failed: {e}")

download(images, media_path)
download(portfolio_images, portfolio_path)
print("Download complete.")
