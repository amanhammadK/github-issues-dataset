import json, random, os, math
from pathlib import Path
from datetime import datetime, timedelta

HERE = Path(__file__).parent
DATA_DIR = HERE.parent / "data"

def gen_github(n=2000):
    random.seed(42)
    titles = [
        "Bug: Application crashes on startup", "Feature: Add dark mode support",
        "Enhancement: Improve loading performance", "Bug: Memory leak in worker thread",
        "Documentation: Update API reference", "Bug: CSS layout broken on mobile",
        "Feature: Implement user authentication", "Bug: Database connection timeout",
        "Enhancement: Add search functionality", "Bug: File upload fails silently",
        "Feature: Export data to CSV", "Bug: Incorrect date formatting",
        "Enhancement: Optimize database queries", "Feature: Add notification system",
        "Bug: Session expires too quickly", "Bug: Error 500 on form submission",
        "Feature: Multi-language support", "Enhancement: Cache API responses",
        "Bug: Image compression not working", "Feature: Add webhook support",
        "Bug: Pagination offset incorrect", "Feature: Batch operations API",
        "Enhancement: Rate limiting improvements", "Bug: Authentication bypass",
        "Feature: Real-time collaboration", "Bug: Memory overflow on large files",
        "Enhancement: Add retry logic", "Feature: Custom dashboard widgets",
        "Bug: Sorting algorithm regression", "Feature: Implement OAuth2"
    ]
    title_types = {"Bug": 0.35, "Feature": 0.30, "Enhancement": 0.20, "Documentation": 0.15}
    type_weights = list(title_types.values())
    labels_pool = ["bug", "feature", "enhancement", "documentation", "priority:high",
                   "priority:medium", "priority:low", "status:open", "status:in-progress",
                   "status:resolved", "good first issue", "help wanted", "needs-triage"]
    label_category = {"bug": "bug", "feature": "feature", "enhancement": "enhancement",
                      "documentation": "documentation"}
    priority_labels = ["priority:high", "priority:medium", "priority:low"]
    assignees = [f"dev_{random.randint(1,50)}" for _ in range(20)]
    contributor_activity = {a: random.gauss(20, 10) for a in assignees}
    closure_times = {"bug": (1, 14), "feature": (7, 60), "enhancement": (3, 30), "documentation": (1, 7)}
    out = []
    base_time = datetime(2024, 1, 1)
    for i in range(n):
        title_type = random.choices(list(title_types.keys()), weights=type_weights, k=1)[0]
        matching_titles = [t for t in titles if t.startswith(title_type)]
        title = random.choice(matching_titles) if matching_titles else random.choice(titles)
        state = random.choices(["open", "closed"], weights=[35, 65], k=1)[0]
        created = base_time + timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
        min_days, max_days = closure_times.get(title_type, (3, 30))
        if state == "closed":
            closure_days = max(1, int(random.gauss((min_days + max_days) / 2, (max_days - min_days) / 4)))
            closed = created + timedelta(days=closure_days)
        else:
            closed = None
        primary_label = title_type.lower()
        if primary_label == "documentation":
            primary_label = "documentation"
        labels = [primary_label]
        if state == "closed":
            labels.append("status:resolved")
        elif random.random() < 0.3:
            labels.append(random.choice(["status:open", "status:in-progress"]))
        labels.append(random.choices(priority_labels, weights=[15, 60, 25], k=1)[0])
        if random.random() < 0.1:
            labels.append("good first issue")
        if random.random() < 0.08:
            labels.append("help wanted")
        if random.random() < 0.15:
            labels.append("needs-triage")
        labels = list(set(labels))
        assigned = random.sample(assignees, random.randint(0, min(3, len(assignees))))
        comments = 0
        if title_type == "bug":
            comments = int(random.lognormvariate(1.5, 0.8))
        elif title_type == "feature":
            comments = int(random.lognormvariate(2.0, 0.7))
        else:
            comments = int(random.lognormvariate(1.2, 0.6))
        reactions = int(comments * random.uniform(0.3, 2.0))
        out.append({
            "id": f"gh_{i:06d}",
            "number": i + 1000,
            "title": title,
            "body": f"Reported issue: {title}. Steps to reproduce and expected behavior documented.",
            "state": state,
            "type": title_type,
            "labels": labels,
            "assignees": assigned,
            "author": random.choice(assignees),
            "created_at": created.isoformat(),
            "closed_at": closed.isoformat() if closed else None,
            "comments_count": min(comments, 200),
            "reactions_count": min(reactions, 500),
            "milestone": random.choice([None, "v2.0", "v2.1", "Sprint 12", "Q1 2024"]),
            "pull_request": random.random() < (0.5 if title_type == "Feature" else 0.2),
            "days_to_close": (closed - created).days if closed else None,
            "has_assignee": len(assigned) > 0,
            "label_count": len(labels),
            "priority": next((l.split(":")[1] for l in labels if l.startswith("priority:")), "medium"),
            "created_day_of_week": created.strftime("%A"),
            "created_hour": created.hour,
        })
    return out

def main():
    data = gen_github()
    DATA_DIR.mkdir(exist_ok=True)
    out = DATA_DIR / "dataset.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Generated {len(data)} GitHub issue records")
    print(f"Saved to {out}")

if __name__ == "__main__":
    main()
