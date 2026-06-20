#!/usr/bin/env python3
"""
Process all CSV files in SEO Borchani directory and add SERP data from SE Ranking.

Strategy:
- Submit up to BATCH_SIZE keywords per DATA_getSerpResults call (all run concurrently on SE Ranking)
- Wait ~30-60s for FIRST keyword result (others process simultaneously)
- Use DATA_getSerpTasks (returns last 106 tasks) to find task IDs for remaining keywords
- Retrieve each remaining task result instantly (they're already done)
- Batch size capped at 50 to stay within the 106-task list limit

Key API facts discovered by testing:
- DATA_getSerpTasks field: "query" (not "keyword"), "id" (not "task_id")
- DATA_getSerpTasks returns max ~106 most recent tasks
- DATA_getSerpResults.query array: each keyword becomes a separate concurrent task
- Task IDs within a batch increment by 3 (can use this as fallback)
"""

import csv
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path("/Users/amanyessen/NEW/SEO Borchani")
DATA_API_TOKEN = "29e6055f-4ebd-199c-23d1-e5e740420d23"
PROJECT_API_TOKEN = "c5ca51817120238eedaf73e68d4cc10987e24c9c"
BATCH_SIZE = 10   # SE Ranking API limit: max 10 queries per batch call
US_LOCATION_ID = 2840
SERP_COLS = [
    "Ссылка конкурента 1", "Ссылка конкурента 2", "Ссылка конкурента 3",
    "Заголовок конкурента 1", "Заголовок конкурента 2", "Заголовок конкурента 3",
    "Сниппет конкурента 1", "Сниппет конкурента 2", "Сниппет конкурента 3",
]


class SEMCPClient:
    def __init__(self):
        self.proc = None
        self.req_id = 0

    def start(self):
        cmd = [
            "docker", "run", "-i", "--rm",
            "-e", f"DATA_API_TOKEN={DATA_API_TOKEN}",
            "-e", f"PROJECT_API_TOKEN={PROJECT_API_TOKEN}",
            "se-ranking/seo-data-api-mcp-server"
        ]
        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self._initialize()

    def _send(self, obj):
        line = json.dumps(obj) + "\n"
        self.proc.stdin.write(line)
        self.proc.stdin.flush()

    def _recv_for_id(self, req_id, timeout=300):
        deadline = time.time() + timeout
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("MCP server closed connection")
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if obj.get("id") == req_id:
                    return obj
            except json.JSONDecodeError:
                continue
        raise TimeoutError(f"Timeout waiting for response to request {req_id}")

    def _initialize(self):
        self.req_id += 1
        self._send({
            "jsonrpc": "2.0",
            "id": self.req_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "serp-processor", "version": "1.0"}
            }
        })
        self._recv_for_id(self.req_id, timeout=30)
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})

    def call_tool(self, name, args, timeout=300):
        self.req_id += 1
        rid = self.req_id
        self._send({
            "jsonrpc": "2.0",
            "id": rid,
            "method": "tools/call",
            "params": {"name": name, "arguments": args}
        })
        return self._recv_for_id(rid, timeout=timeout)

    def get_all_tasks(self):
        """Get all SERP tasks from last 24h (up to ~106). Fields: id, query, is_completed."""
        try:
            resp = self.call_tool("DATA_getSerpTasks", {}, timeout=30)
            content = resp.get("result", {}).get("content", [])
            text = content[0]["text"] if content else "{}"
            data = json.loads(text)
            tasks = data if isinstance(data, list) else data.get("data", data.get("tasks", []))
            return tasks if isinstance(tasks, list) else []
        except Exception as e:
            print(f"  Warning: get_all_tasks failed: {e}")
            return []

    def get_task_result(self, task_id, max_polls=12, poll_interval=5):
        """Get results for a specific completed task."""
        for attempt in range(max_polls):
            try:
                resp = self.call_tool("DATA_getSerpTaskResults", {"task_id": task_id}, timeout=60)
                content = resp.get("result", {}).get("content", [])
                text = content[0]["text"] if content else "{}"
                data = json.loads(text)
                if data.get("status") == "processing":
                    time.sleep(poll_interval)
                    continue
                return data
            except Exception as e:
                print(f"  Warning: get_task_result({task_id}) attempt {attempt+1}: {e}")
                time.sleep(2)
        return {}

    def submit_batch(self, keywords):
        """
        Submit up to BATCH_SIZE keywords concurrently.
        Returns dict: {keyword: top3_results_list}
        """
        kw_set = set(keywords)

        # Snapshot task IDs before submission
        tasks_before_ids = {t["id"] for t in self.get_all_tasks() if "id" in t}

        # Submit all keywords; API creates one task per keyword running concurrently
        # Tool polls for FIRST keyword result (~30-60s), others finish simultaneously
        t0 = time.time()
        resp = self.call_tool("DATA_getSerpResults", {
            "query": keywords,
            "language_code": "en",
            "location_id": US_LOCATION_ID,
            "device": "desktop",
            "poll_interval_ms": 5000,
            "max_wait_ms": 180000,
        }, timeout=220)
        elapsed = time.time() - t0

        # Parse first keyword result from the response
        first_top3 = self._parse_serp_response(resp)
        first_task_id = self._get_task_id_from_response(resp)

        results = {keywords[0]: first_top3}

        # Find remaining task IDs via task list
        tasks_after = self.get_all_tasks()
        # Build map: query -> task_id for NEW tasks only
        task_map = {}
        for task in tasks_after:
            tid = task.get("id")
            kw = task.get("query", "")  # NOTE: field is "query" not "keyword"
            if tid and kw in kw_set and tid not in tasks_before_ids:
                # Keep highest task_id if duplicate keyword
                if kw not in task_map or tid > task_map[kw]:
                    task_map[kw] = tid

        # Fallback: if task_map is incomplete, try predicting task IDs from first_task_id
        # (Tasks within a batch increment by 3 each)
        # Fallback: predict task IDs from first_task_id (tasks within a batch increment by 3)
        if first_task_id and len(task_map) < len(keywords) - 1:
            for i, kw in enumerate(keywords[1:], 1):
                if kw not in task_map:
                    for delta in [3, 6, 9, 1, 2, 4, 5]:  # try likely gaps
                        predicted_id = first_task_id + i * delta
                        # Only use if not already taken by another keyword
                        if predicted_id not in task_map.values():
                            task_map[kw] = predicted_id
                            break

        missing = []
        # Retrieve results for remaining keywords
        for kw in keywords[1:]:
            task_id = task_map.get(kw)
            if task_id:
                data = self.get_task_result(task_id)
                items = data.get("items", [])
                results[kw] = self._extract_top3(items)
            else:
                results[kw] = []
                missing.append(kw)

        if missing:
            print(f"  Warning: could not find task_id for {len(missing)} keywords (will have empty SERP data)")

        return results, elapsed

    def _get_task_id_from_response(self, resp):
        """Extract task_id from DATA_getSerpResults response."""
        try:
            content = resp.get("result", {}).get("content", [])
            text = content[0]["text"] if content else "{}"
            data = json.loads(text)
            return data.get("task_id")
        except Exception:
            return None

    def _parse_serp_response(self, resp):
        """Parse DATA_getSerpResults response into top-3 organic items list."""
        try:
            content = resp.get("result", {}).get("content", [])
            text = content[0]["text"] if content else "{}"
            data = json.loads(text)
            items = data.get("results", {}).get("items", [])
            return self._extract_top3(items)
        except Exception:
            return []

    def _extract_top3(self, items):
        """Extract top 3 organic results from items list."""
        organic = [i for i in items if i.get("type") == "organic"]
        top3 = []
        for item in organic[:3]:
            url = item.get("url", "")
            if not url:
                links = item.get("links", [])
                url = links[0].get("url", "") if links else ""
            top3.append({
                "url": url,
                "title": item.get("title", ""),
                "snippet": item.get("description", item.get("snippet", "")),
            })
        return top3

    def stop(self):
        if self.proc:
            try:
                self.proc.stdin.close()
                self.proc.wait(timeout=5)
            except Exception:
                self.proc.kill()


def detect_keyword_column(headers):
    candidates = ["keyword", "ключевое слово", "query", "kw", "keywords"]
    headers_lower = [h.lower().strip() for h in headers]
    for c in candidates:
        if c in headers_lower:
            return headers[headers_lower.index(c)]
    return None


def has_serp_data(row):
    """True if first competitor link already filled."""
    return bool(row.get("Ссылка конкурента 1", "").strip())


def fill_serp_row(row, top3):
    for i in range(3):
        idx = i + 1
        if i < len(top3):
            item = top3[i]
            row[f"Ссылка конкурента {idx}"] = item.get("url", "")
            row[f"Заголовок конкурента {idx}"] = item.get("title", "")
            row[f"Сниппет конкурента {idx}"] = item.get("snippet", "")
        else:
            row[f"Ссылка конкурента {idx}"] = ""
            row[f"Заголовок конкурента {idx}"] = ""
            row[f"Сниппет конкурента {idx}"] = ""
    return row


def process_csv(filepath, client, global_processed):
    print(f"\n{'='*60}")
    print(f"File: {filepath.relative_to(BASE_DIR)}")

    with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        original_fields = reader.fieldnames or []

    if not rows:
        print("  Empty file, skipping.")
        return 0

    kw_col = detect_keyword_column(original_fields)
    if not kw_col:
        print(f"  No keyword column found in {original_fields}. Skipping.")
        return 0

    # Ensure SERP columns exist
    new_fields = list(original_fields)
    for col in SERP_COLS:
        if col not in new_fields:
            new_fields.append(col)
    for row in rows:
        for col in SERP_COLS:
            if col not in row:
                row[col] = ""

    # Find rows needing processing (skip already-filled ones)
    pending = [(i, row[kw_col].strip()) for i, row in enumerate(rows)
               if row.get(kw_col, "").strip() and not has_serp_data(row)]

    if not pending:
        print(f"  All rows processed or no keywords. Skipping.")
        return 0

    print(f"  Rows to process: {len(pending)}")
    total_processed = 0

    for batch_start in range(0, len(pending), BATCH_SIZE):
        batch = pending[batch_start:batch_start + BATCH_SIZE]
        batch_indices = [b[0] for b in batch]
        batch_keywords = [b[1] for b in batch]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE

        print(f"  Batch {batch_num}/{total_batches}: {len(batch_keywords)} keywords...", end="", flush=True)

        try:
            serp_results, elapsed = client.submit_batch(batch_keywords)
            print(f" done in {elapsed:.0f}s")

            for idx, kw in zip(batch_indices, batch_keywords):
                top3 = serp_results.get(kw, [])
                rows[idx] = fill_serp_row(rows[idx], top3)
                total_processed += 1

        except Exception as e:
            print(f" ERROR: {e}")
            import traceback
            traceback.print_exc()
            for idx in batch_indices:
                fill_serp_row(rows[idx], [])
            total_processed += len(batch_indices)

        global_processed[0] += len(batch_keywords)
        pct = global_processed[0] / TOTAL_KEYWORDS * 100 if TOTAL_KEYWORDS else 0
        print(f"  File: {total_processed}/{len(pending)} | Global: {global_processed[0]:,}/{TOTAL_KEYWORDS:,} ({pct:.1f}%)")

        # Save after each batch
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=new_fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    print(f"  File complete: {total_processed} keywords.")
    return total_processed


def count_pending_keywords(csv_files):
    """Count total keywords needing processing across all files."""
    total = 0
    for filepath in csv_files:
        try:
            with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                headers = reader.fieldnames or []
            kw_col = detect_keyword_column(headers)
            if not kw_col:
                continue
            for row in rows:
                kw = row.get(kw_col, "").strip()
                if kw and not has_serp_data(row):
                    total += 1
        except Exception:
            pass
    return total


def main():
    global TOTAL_KEYWORDS

    csv_files = sorted(BASE_DIR.rglob("*.csv"))
    csv_files = [f for f in csv_files if f.name != "process_serp.py"]

    print(f"Counting pending keywords...")
    TOTAL_KEYWORDS = count_pending_keywords(csv_files)
    print(f"Found {len(csv_files)} CSV files, {TOTAL_KEYWORDS:,} keywords to process.")
    print(f"Settings: location=US (id={US_LOCATION_ID}), language=en, device=desktop, batch={BATCH_SIZE}")
    print(f"Estimated time: ~{TOTAL_KEYWORDS / BATCH_SIZE * 50 / 3600:.1f} hours")

    print("\nStarting SE Ranking MCP server (Docker)...")
    client = SEMCPClient()
    try:
        client.start()
        print("MCP server started.")
    except Exception as e:
        print(f"Failed to start MCP server: {e}")
        sys.exit(1)

    total_files_done = 0
    total_keywords_done = 0
    global_processed = [0]
    start_time = time.time()

    try:
        for csv_file in csv_files:
            try:
                count = process_csv(csv_file, client, global_processed)
                if count > 0:
                    total_files_done += 1
                    total_keywords_done += count
            except KeyboardInterrupt:
                print("\n\nInterrupted. Progress saved to files.")
                break
            except Exception as e:
                print(f"\nERROR in {csv_file.name}: {e}")
                import traceback
                traceback.print_exc()
    finally:
        client.stop()

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"FINISHED in {elapsed/3600:.1f} hours")
    print(f"Files with new data: {total_files_done}")
    print(f"Total keywords processed: {total_keywords_done:,}")


TOTAL_KEYWORDS = 0

if __name__ == "__main__":
    main()
