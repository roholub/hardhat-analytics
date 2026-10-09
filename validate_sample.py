"""Validate the frozen synthetic fixture without Fabric access or dependencies."""
import ast
import csv
from datetime import date
from decimal import Decimal
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    manifest = json.loads((ROOT / "data/manifest.json").read_text())
    data = {}
    for table, spec in manifest["tables"].items():
        with (ROOT / "data" / (table + ".csv")).open(newline="", encoding="utf-8") as handle:
            records = list(csv.DictReader(handle))
        require(len(records) == spec["rows"], table + " row count")
        key = spec["columns"][0]["name"]
        require(all(row[key] for row in records), table + " null key")
        require(len({row[key] for row in records}) == len(records), table + " duplicate key")
        data[table] = records
    projects = {row["project_id"]: row for row in data["projects"]}
    tasks = {row["task_id"]: row for row in data["tasks"]}
    zones = {row["location_id"]: row for row in data["locations"]}
    for task in tasks.values():
        require(task["project_id"] in projects, "Task project orphan")
        require(task["location_id"] in zones, "Task zone orphan")
        require(zones[task["location_id"]]["project_id"] == task["project_id"], "Task zone mismatch")
        predecessor = task["dependency_task_id"]
        if predecessor:
            require(predecessor in tasks, "Predecessor orphan")
            require(tasks[predecessor]["project_id"] == task["project_id"], "Cross-project predecessor")
        seen, node = set(), task["task_id"]
        while node:
            require(node not in seen, "Dependency cycle")
            seen.add(node)
            node = tasks[node]["dependency_task_id"]
    expected_dependencies = {(t["task_id"], t["dependency_task_id"])
                             for t in tasks.values() if t["dependency_task_id"]}
    actual_dependencies = {(d["successor_task_id"], d["predecessor_task_id"])
                           for d in data["task_dependencies"]}
    require(actual_dependencies == expected_dependencies, "Dependency fixture mismatch")
    evidence = {row["task_id"]: row for row in data["task_evidence"]}
    for key, task in tasks.items():
        require(key in evidence, "Missing task evidence")
        e = evidence[key]
        require(e["completion_evidence"] == (
            "RecordedFinish" if task["actual_end_date"] else "NoRecordedFinish"), "Completion evidence")
        expected_delay = (str((date.fromisoformat(task["actual_end_date"]) -
                               date.fromisoformat(task["planned_end_date"])).days)
                          if task["actual_end_date"] else "")
        require(e["recorded_delay_days"] == expected_delay, "Recorded task variance")
    totals, task_totals = {}, {}
    for cost in data["costs"]:
        require(cost["task_id"] in tasks, "Cost task orphan")
        require(cost["project_id"] == tasks[cost["task_id"]]["project_id"], "Cost project mismatch")
        planned, actual = Decimal(cost["planned_cost"]), Decimal(cost["actual_cost"])
        require(planned >= 0 and actual >= 0, "Negative synthetic cost")
        p = totals.setdefault(cost["project_id"], [Decimal(0), Decimal(0)])
        p[0] += planned
        p[1] += actual
        task_totals[cost["task_id"]] = task_totals.get(cost["task_id"], Decimal(0)) + actual - planned
    for review in data["project_reviews"]:
        key = review["project_id"]
        planned, actual = totals[key]
        require(Decimal(review["planned_cost_total"]) == planned, "Review planned mismatch")
        require(Decimal(review["actual_cost_total"]) == actual, "Review actual mismatch")
        require(Decimal(review["cost_overrun_amount"]) == actual - planned, "Review overrun mismatch")
        project = projects[key]
        delay = ((date.fromisoformat(project["actual_end_date"]) -
                  date.fromisoformat(project["planned_end_date"])).days
                 if project["actual_end_date"] else None)
        require(review["recorded_project_delay_days"] == (str(delay) if delay is not None else ""),
                "Project recorded delay mismatch")
        expected_flag = "" if delay is None else str(
            delay >= 90 and (actual - planned) / planned >= Decimal("0.20")).lower()
        require(review["attention_candidate"] == expected_flag, "Attention criterion mismatch")
    planned, actual = totals["PRJ-0001"]
    require(actual - planned == Decimal("1717393.65"), "Meadowbrook overrun")
    zone_totals = {}
    for key, overrun in task_totals.items():
        if tasks[key]["project_id"] == "PRJ-0001":
            zone = zones[tasks[key]["location_id"]]["zone_name"]
            zone_totals[zone] = zone_totals.get(zone, Decimal(0)) + overrun
    require(zone_totals == {"Floor 2": Decimal("570931.42"), "Floor 3": Decimal("483643.36"),
                           "Basement": Decimal("391303.68"), "Floor 1": Decimal("271515.19")},
            "Zone cost evidence")
    require(tasks["PRJ-0001-T005"]["task_status"] == "On Track", "Concrete Pour status")
    require(tasks["PRJ-0001-T005"]["dependency_task_id"] == "PRJ-0001-T004", "Concrete predecessor")
    require(sum(bool(t["actual_end_date"]) for t in tasks.values()) == 269, "Recorded finish count")
    notebook = json.loads((ROOT / "Load_HardHat_Sample.ipynb").read_text())
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            ast.parse("".join(cell["source"]))
            require(cell["outputs"] == [] and cell["execution_count"] is None, "Notebook outputs")
    measures = (ROOT / "semantic-model/definition/tables/_Measures.tmdl").read_text()
    require("TODAY()" not in measures and "FILTER ( projects, NOT ISBLANK" in measures,
            "Historical delay measures")
    require("formatString: 0.00%" in measures, "Percentage format")
    forbidden = re.compile(
        "(?i)" + r"\b" + "whit" + "ing" + r"\b|\b" + "tur" + "ner" + r"\b|" +
        r"\bWT\b|\bISD\b|" + "roc" + "io|" + "roho" + "lub|" + "m365" + "x|" +
        r"Bearer\s+[A-Za-z0-9._-]+|gh[pousr]_[A-Za-z0-9]+|"
        r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY|"
        r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|"
        r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b|"
        r"[A-Z]:\\Users\\|onelake\.dfs|datawarehouse\.fabric")
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            require(not forbidden.search(path.read_text(encoding="utf-8")),
                    "Public-safety scan failed: " + str(path.relative_to(ROOT)))
    print("PASS: fixture integrity, joins, dependencies, recorded evidence, review calculations,")
    print("      demo results, notebook syntax, historical measures and public-safety pattern scan.")
    print("These are data/package checks, not agent-accuracy or live Fabric deployment claims.")


if __name__ == "__main__":
    main()
