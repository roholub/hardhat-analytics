# Hard Hat Analytics
## From project signals to connected evidence

Ever looked at a red project dashboard and wondered, **"Where should we start?"**

This small Microsoft Fabric sample helps you explore that question with **fictional construction data**. Load the data, use the semantic model for defined calculations, and optionally add an ontology to make the business connections explicit.

**20 projects. 347 tasks. 1,041 cost records. 116 zones.**

All data is synthetic, and project names are made up. Any resemblance to real projects is purely coincidental.

## The story

**Meadowbrook Apartments** has a recorded project delay of **164 days** and a **$1.72 million cost overrun**.

Those numbers tell us there is something to review. They do not tell us where to start.

Connect the activities to their zones and cost records, and the picture gets more useful:

| Zone | Tasks labeled Delayed | Recorded cost overrun |
|---|---:|---:|
| **Floor 2** | **3** | **$570,931.42** |
| Floor 3 | 1 | $483,643.36 |
| Basement | 1 | $391,303.68 |
| Floor 1 | 0 | $271,515.19 |

**Start the review on Floor 2**, with Painting, Flooring and Glazing.

That is a starting point backed by records, **not proof of what caused the overrun**. Floor 2's total includes all five activities there, not just those three.

## Who does what?

| Component | Its job |
|---|---|
| **Lakehouse** | Holds the sample records. |
| **Semantic model** | Defines calculations such as cost overrun and recorded finish variance. |
| **Ontology, optional** | Describes projects, tasks, zones, costs and how they connect. |
| **Agent, when configured** | Uses that context to investigate a question and return evidence. |

Think of the ontology as **a shared business map, not a new data store**.

Semantic models already contain meaning and relationships. Ontology can extend that context; it does not replace them. You do not need an ontology for every query or agent.

## Start here

You need Python 3 locally, plus a Fabric workspace and capacity for the Fabric steps.

1. Download or clone this repository.
2. Check the sample locally:
   ```powershell
   python validate_sample.py
   ```
3. Create a **new, schema-enabled lakehouse** in Fabric.
4. Upload the files inside `data/` to `Files/hardhat_sample`.
5. Import [`Load_HardHat_Sample.ipynb`](Load_HardHat_Sample.ipynb), attach that lakehouse as its default, and run it.

**The notebook never overwrites existing sample tables.** If a run stops after some tables were written, inspect the error and use another new lakehouse before retrying.

## Add the business context

**For the semantic model:** replace `YOUR_SQL_ENDPOINT` and `YOUR_SQL_DATABASE_ID` in [`expressions.tmdl`](semantic-model/definition/expressions.tmdl) with your own lakehouse connection details. Import the TMDL using supported model tooling or the Fabric public API.

These are model definitions, **not a complete PBIP project or report**. See the [setup reference](README.txt) for details.

**For the optional ontology:** follow the [entity mappings, relationships and example questions](ontology-setup.txt). Fabric Ontology is currently in **preview**; availability depends on your environment.

## What is in the box?

| Path | What you get |
|---|---|
| [`data/`](data/) | Frozen synthetic records and a column/count manifest. |
| [`Load_HardHat_Sample.ipynb`](Load_HardHat_Sample.ipynb) | Safe import into a new Fabric lakehouse. |
| [`semantic-model/`](semantic-model/) | Portable TMDL definitions and calculations. |
| [`ontology-setup.txt`](ontology-setup.txt) | Optional setup instructions and expected answers. |
| [`validate_sample.py`](validate_sample.py) | Local checks for joins, calculations and sample integrity. |

**Not included:** a Fabric app, hosted agent, deployment automation or access configuration.

## Keep the conclusions honest

**This is historical, synthetic data, not a live construction system.**

- A missing finish date means **missing evidence**, not confirmed active work.
- **On Track is a sample label, not zero variance.** Concrete Pour has a 13-day finish variance and is labeled On Track because this sample uses a below-15-day threshold.
- Predecessor links and zone assignments are illustrative, not a validated construction sequence or engineering model.
- Cost records are one row per task and category. **Count each row once.**
- No subcontractor attribution, revenue/margin or approval evidence is included. Do not invent blame, readiness or savings.
- Expected answers help you evaluate results; they do not guarantee agent accuracy.
- Apply your own source permissions. **A prompt is not an access control.**

The aim is simple: **connect the evidence, focus the review, and be clear about what you do not know.**

[MIT license](LICENSE).
