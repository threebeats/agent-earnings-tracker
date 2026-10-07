#!/usr/bin/env python3
"""
Agent Earnings Tracker
Track earnings across AI agent platforms from one CLI.
"""

import json
import os
import sys
from datetime import datetime, timezone

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "earnings.json")

def load_data():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"entries": [], "platforms": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def ensure_platform(data, platform):
    """Return the platform record, creating it if missing."""
    if platform not in data["platforms"]:
        data["platforms"][platform] = {
            "name": platform,
            "total_earned": 0,
            "pending": 0,
            "added": datetime.now(timezone.utc).isoformat()
        }
    return data["platforms"][platform]

def cmd_add(args):
    """Add a tracked platform."""
    data = load_data()
    platform = args[0] if args else input("Platform name: ").strip()
    ensure_platform(data, platform)
    save_data(data)
    print(f"✅ Added platform: {platform}")

def cmd_log(args):
    """Log an earning event."""
    data = load_data()
    platform = args[0] if len(args) > 0 else input("Platform: ").strip()
    amount = float(args[1]) if len(args) > 1 else float(input("Amount: "))
    note = args[2] if len(args) > 2 else input("Note (optional): ").strip()
    
    entry = {
        "platform": platform,
        "amount": amount,
        "note": note,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    data["entries"].append(entry)
    
    new_platform = platform not in data["platforms"]
    ensure_platform(data, platform)["total_earned"] += amount
    
    save_data(data)
    suffix = " (new platform auto-added)" if new_platform else ""
    print(f"✅ Logged ${amount:.2f} on {platform}{suffix}")

def cmd_summary(args):
    """Show earnings summary."""
    data = load_data()
    platforms = data.get("platforms", {})
    entries = data.get("entries", [])
    
    print("\n=== Earnings Summary ===\n")
    
    total = sum(p.get("total_earned", 0) for p in platforms.values())
    pending = sum(p.get("pending", 0) for p in platforms.values())
    
    print(f"Platforms tracked: {len(platforms)}")
    print(f"Total entries: {len(entries)}")
    print(f"Total earned: ${total:.2f}")
    print(f"Total pending: ${pending:.2f}")
    print()
    
    if platforms:
        print(f"{'Platform':<20} {'Earned':<12} {'Pending':<12}")
        print("-" * 44)
        for name, p in sorted(platforms.items()):
            print(f"{name:<20} ${p.get('total_earned',0):<8.2f} ${p.get('pending',0):<8.2f}")
    
    if entries:
        print(f"\nRecent entries ({min(5, len(entries))} of {len(entries)}):")
        for e in entries[-5:]:
            print(f"  ${e['amount']:.2f} on {e['platform']} — {e.get('note','')[:30]}")

def cmd_export(args):
    """Export data as CSV."""
    data = load_data()
    csv_path = os.path.join(os.path.dirname(__file__), "data", "earnings.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    with open(csv_path, "w") as f:
        f.write("timestamp,platform,amount,note\n")
        for e in data.get("entries", []):
            f.write(f"{e['timestamp']},{e['platform']},{e['amount']},{e.get('note','')}\n")
    
    print(f"✅ Exported to {csv_path}")

def main():
    commands = {
        "add": cmd_add,
        "log": cmd_log,
        "summary": cmd_summary,
        "export": cmd_export,
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("Usage: python3 earnings.py <command> [args]")
        print("Commands: add, log, summary, export")
        return
    
    commands[sys.argv[1]](sys.argv[2:])

if __name__ == "__main__":
    main()
