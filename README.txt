HARD HAT ANALYTICS
From project signals to connected evidence.

A small, historical, fully synthetic construction portfolio for exploring
defined measurements, business relationships and evidence-based questions.
No real customer records, tenant configuration, credentials or personal
identifiers are included. Project names and locations are fictional examples;
city names are public geographic labels, not locations of real projects.

WHAT IS INCLUDED
- data/: frozen CSV fixtures, including the exact records used in the example.
- Load_HardHat_Sample.ipynb: a Fabric import notebook for a NEW lakehouse.
- semantic-model/: portable TMDL calculations and table relationships.
- ontology-setup.txt: optional business-context setup and example questions.
- validate_sample.py: local data/definition checks using Python standard library.

FAST START
1. Run locally: python validate_sample.py
2. In your own Fabric workspace, create a NEW schema-enabled lakehouse.
3. Upload the files inside data/ to its Files/hardhat_sample folder.
4. Import Load_HardHat_Sample.ipynb and attach that lakehouse as default.
5. Run the notebook. It refuses to overwrite existing sample tables.
6. Optionally configure the semantic model and ontology as described below.

SEMANTIC MODEL
The TMDL definition binds projects, tasks, costs and locations using Direct Lake
and supplies cost totals, overrun amount/rate, recorded project delay and
recorded-finish counts. It does not infer a missing finish date from today.

In semantic-model/definition/expressions.tmdl replace:
  YOUR_SQL_ENDPOINT: the target lakehouse's SQL analytics endpoint hostname.
  YOUR_SQL_DATABASE_ID: its SQL analytics endpoint database identifier.
Do not replace with passwords or access tokens.

Create an empty Direct Lake semantic model against your new lakehouse, then
import the TMDL through your supported modeling tool (for example, TMDL view
in Power BI Desktop or a model-management tool supporting TMDL), or submit
these definition parts through the Fabric semantic-model public API.
definition.pbism belongs at the definition root; the files in definition/
are the model parts. This directory is not a complete PBIP/report project.
Apply your own authentication, permissions and capacity configuration.
Configure the two placeholders before deployment. No model refresh,
sharing, permission changes or deployment is performed by this repository.

EVIDENCE EXAMPLE
Meadowbrook Apartments / PRJ-0001:
  Recorded project finish variance: 164 days.
  Planned cost: 5,239,663.92; actual cost: 6,957,057.57.
  Cost overrun: 1,717,393.65 (32.78%).
  Floor 2: three Delayed-status tasks and 570,931.42 cost overrun.
  Largest Floor 2 task overruns: Painting 197,787.95;
  Flooring 128,630.93; Glazing 124,641.76.
  Concrete Pour PRJ-0001-T005: Floor 2, On Track, 13-day finish variance;
  recorded predecessor Structural Steel PRJ-0001-T004, Basement, On Track.

The same facts can support a recommendation to START A REVIEW on Floor 2.
They cannot establish the cause of an overrun or an operational action.

SEMANTICS AND GUARDRAILS
- All dates are historical. This is not current operational data.
- Source task labels: <=0 days Complete; 1-14 On Track;
  15-39 At Risk; 40+ Delayed. These are synthetic thresholds, not standards.
- Status is not completion evidence. A recorded finish may coexist with
  an On Track or Delayed label. Missing finish means unknown, not active work.
- Generated risk_score is illustrative, not a validated predictive model.
- Predecessor links are synthetic references, not a validated construction
  sequence, critical path, enforced prerequisite or causal relationship.
- Some activity-to-zone assignments are illustrative and not engineering
  geometry (for example, a generic landscaping activity may be in Basement).
- Cost grain: one task/category row. Aggregate once before other joins.
  Money in review tables is computed at cent precision.
- project_reviews flags delay >=90 days AND overrun ratio >=20%.
  Missing recorded project finish is NeedsEvidence. This is an illustrative
  sample criterion, not production policy. OtherEvidenceToReview is not
  an assurance of low risk or a recommendation to ignore a project.
- No subcontractor, margin/revenue, change-order, inspection approval,
  journal or operating-procedure evidence is modeled.
- Do not infer blame, readiness, safety, financial causation or savings.
- Prompts and status labels are not access controls. Apply source permissions.
- Expected results are data references, not an agent accuracy guarantee.
- Useful agents and relational queries do not require an ontology.

SCOPE
No application, hosted agent, customer presentation, transcript, captured
conversation or tenant deployment is included. The data and semantic model
stand alone. The optional ontology instructions identify their requirements.
Use your own environments; do not submit secrets or real records in issues.
