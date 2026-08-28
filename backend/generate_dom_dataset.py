import asyncio
import json
import os
import aiohttp
import pandas as pd
from playwright.async_api import async_playwright
from tqdm.asyncio import tqdm
import zipfile
import io
import re

# === CONFIGURATION ===
MAX_SITES = 1000   # Limit to 1k as requested (Verified)
CONCURRENCY = 25   # Optimization
TIMEOUT_MS = 15000 # 15s Timeout
OUTPUT_FILE = "backend/data/dom_structures_20k.json"

# === TRANCO LIST FETCH ===
async def get_top_domains(limit):
    print("📥 Downloading Tranco Top 1M List...")
    url = "https://tranco-list.eu/top-1m.csv.zip"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception("Failed to download Tranco list")
            data = await resp.read()
    
    print("📦 Extracting list...")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        # The zip usually contains 'top-1m.csv'
        csv_name = z.namelist()[0]
        with z.open(csv_name) as f:
            df = pd.read_csv(f, header=None, names=['rank', 'domain'])
    
    print(f"✅ Loaded {len(df)} domains. Selecting top {limit}...")
    return df['domain'].head(limit).tolist()

# === DOM FEATURE EXTRACTOR ===
JS_EXTRACTOR = """
() => {
    // 1. Tag Sequence (BFS/DFS for first few levels)
    function getStructure() {
        let path = [];
        let root = document.documentElement;
        if(!root) return "empty";
        
        let queue = [{node: root, level: 0}];
        let maxLevel = 3;
        
        while(queue.length > 0) {
            let {node, level} = queue.shift();
            if(level > maxLevel) continue;
            
            let tag = node.tagName ? node.tagName.toLowerCase() : "";
            if(node.id) tag += "#" + node.id;
            // if(node.className) tag += "." + node.className.split(' ')[0]; // Too noisy
            
            path.push(tag);
            
            Array.from(node.children).forEach(child => {
                queue.push({node: child, level: level + 1});
            });
        }
        return path.slice(0, 20).join(' > '); // Limit to first 20 nodes of signature
    }

    // 2. ID Patterns
    function getIds() {
        const ids = Array.from(document.querySelectorAll('[id]'))
                        .map(el => el.id)
                        .filter(id => id.length > 3 && isNaN(id)); // Filter junk
        return ids.slice(0, 15); // Top 15 IDs
    }

    // 3. Metrics
    const allNodes = document.querySelectorAll('*');
    const scripts = document.querySelectorAll('script');
    
    return {
        fingerprint: getStructure(),
        unique_ids: getIds(),
        metrics: {
            node_count: allNodes.length,
            script_count: scripts.length,
            script_ratio: allNodes.length > 0 ? (scripts.length / allNodes.length).toFixed(4) : 0
        }
    };
}
"""

# === WORKER ===
async def process_domain(context, domain, semaphore, pbar):
    async with semaphore:
        page = await context.new_page()
        try:
            # Block heavy resources
            await page.route("**/*.{png,jpg,jpeg,gif,css,font,woff,woff2}", lambda route: route.abort())
            
            url = f"http://{domain}"
            await page.goto(url, timeout=TIMEOUT_MS, wait_until="domcontentloaded")
            
            # Extract
            data = await page.evaluate(JS_EXTRACTOR)
            
            result = {
                "domain": domain,
                "fingerprint": data['fingerprint'],
                "unique_ids": data['unique_ids'],
                "node_count": data['metrics']['node_count'],
                "script_ratio": data['metrics']['script_ratio'],
                "status": "success"
            }
            
        except Exception as e:
            # Graceful failure
            result = {
                "domain": domain,
                "status": "failed",
                "error": str(e)[:50]
            }
        finally:
            await page.close()
            pbar.update(1)
            return result

# === MAIN ===
async def main():
    domains = await get_top_domains(MAX_SITES)
    
    # Reload existing progress if any
    results = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r') as f:
                results = json.load(f)
                processed_domains = {r['domain'] for r in results}
                domains = [d for d in domains if d not in processed_domains]
                print(f"🔄 Resuming... {len(results)} already done. {len(domains)} remaining.")
        except:
            pass
    
    # Browser setup with GPU ACCELERATION
    async with async_playwright() as p:
        print("🚀 Launching Chromium with RTX 2050 Optimization...")
        browser = await p.chromium.launch(
            headless=True, # GPU works in headless=new or standard on newer builds
            args=[
                "--use-gl=angle", 
                "--use-angle=d3d11", # Direct3D 11 for NVIDIA on Windows
                "--enable-gpu-rasterization",
                "--ignore-gpu-blocklist",
                "--disable-software-rasterizer",
                "--accelerated-2d-canvas",
                "--enable-zero-copy",
                "--no-sandbox"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Block heavy stuff to save GPU for DOM layout
            viewport={"width": 1280, "height": 720}
        )
        
        semaphore = asyncio.Semaphore(CONCURRENCY)
        pbar = tqdm(total=MAX_SITES, initial=len(results), desc="Scraping with RTX 2050")
        
        tasks = [process_domain(context, d, semaphore, pbar) for d in domains]
        
        # Gather with intermediate saves could be better, but for 20k, memory is fine (approx 20MB JSON)
        # We will split into chunks if needed, but gather_all is okay for V1.
        
        chunk_size = 50 # Smaller batches for smoother progress
        for i in range(0, len(tasks), chunk_size):
            chunk = tasks[i:i+chunk_size]
            chunk_results = await asyncio.gather(*chunk)
            results.extend([r for r in chunk_results if r['status'] == 'success'])
            
            # Intermediate Save
            print(f"\n💾 Saving progress ({len(results)} records)...")
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(results, f, indent=2)

        await browser.close()
        pbar.close()

    print(f"\n✅ COMPLETED. Saved {len(results)} site structures to {OUTPUT_FILE}")

if __name__ == "__main__":
    if not os.path.exists('backend/data'):
        os.makedirs('backend/data')
    asyncio.run(main())
