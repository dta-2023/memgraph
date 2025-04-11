
from gqlalchemy import Memgraph, create, match

# Connect to Memgraph
memgraph = Memgraph(host="127.0.0.1", port=7687)

# Optional: Reset the graph before starting
memgraph.execute("MATCH (n) DETACH DELETE n")

# --------------------------
# EXERCISE 1 – Create Drivers
# --------------------------
create().node(labels="Driver", name="John", id="D001").execute()
create().node(labels="Driver", name="Jane", id="D002").execute()
create().node(labels="Driver", name="Mike", id="D003").execute()

print("✅ Exercise 1 complete: Drivers created.")

# --------------------------
# EXERCISE 2 – Build Invoice Graph
# --------------------------
create().node(labels="Invoice", invoice_id="F001", amount=9400).execute()
create().node(labels="Invoice", invoice_id="F002", amount=9800).execute()
create().node(labels="Bank", iban="CH93-0000-0000-0000-0001").execute()

match().node(labels="Driver", name="John", variable="d1")    .match().node(labels="Invoice", invoice_id="F001", variable="i1")    .create().node(variable="d1").to("SENT").node(variable="i1")    .execute()

match().node(labels="Driver", name="Jane", variable="d2")    .match().node(labels="Invoice", invoice_id="F002", variable="i2")    .create().node(variable="d2").to("SENT").node(variable="i2")    .execute()

match().node(labels="Invoice", invoice_id="F001", variable="i1")    .match().node(labels="Bank", iban="CH93-0000-0000-0000-0001", variable="b")    .create().node(variable="i1").to("PAID_INTO").node(variable="b")    .execute()

print("✅ Exercise 2 complete: Mini graph created.")

# --------------------------
# EXERCISE 3 – List Sent Invoices
# --------------------------
results = memgraph.execute_and_fetch("""
MATCH (d:Driver)-[:SENT]->(i:Invoice)
RETURN d.name AS driver, i.invoice_id AS invoice
""")
print("🧾 Exercise 3 results:")
for row in results:
    print(f"{row['driver']} sent invoice {row['invoice']}")

# --------------------------
# EXERCISE 4 – Detect IBAN Reuse (Fraud)
# --------------------------
memgraph.execute("CREATE (:Driver {name: 'Fraudy', id: 'D004'})")
memgraph.execute("CREATE (:Invoice {invoice_id: 'F003', amount: 9300})")
memgraph.execute("""
MATCH (d:Driver {name: 'Fraudy'}), (i:Invoice {invoice_id: 'F003'})
CREATE (d)-[:SENT]->(i)
""")
memgraph.execute("""
MATCH (i:Invoice {invoice_id: 'F003'}), (b:Bank {iban: 'CH93-0000-0000-0000-0001'})
CREATE (i)-[:PAID_INTO]->(b)
""")

results = memgraph.execute_and_fetch("""
MATCH (d:Driver)-[:SENT]->(:Invoice)-[:PAID_INTO]->(b:Bank)
WITH b.iban AS iban, collect(DISTINCT d.name) AS drivers, count(DISTINCT d.name) AS nb
WHERE nb > 1
RETURN iban, drivers, nb
""")
print("🚨 Exercise 4 fraud detection:")
for row in results:
    print(f"⚠️ IBAN {row['iban']} used by {row['nb']} drivers: {row['drivers']}")

# --------------------------
# EXERCISE 5 – Fraud Detection Function
# --------------------------
def detect_fraud():
    frauds = []
    results = memgraph.execute_and_fetch("""
    MATCH (d:Driver)-[:SENT]->(:Invoice)-[:PAID_INTO]->(b:Bank)
    WITH b.iban AS iban, collect(DISTINCT d.name) AS drivers, count(DISTINCT d.name) AS nb
    WHERE nb > 2
    RETURN iban, drivers, nb
    """)
    for row in results:
        frauds.append(f"🚩 IBAN {row['iban']} shared by {row['nb']} drivers: {row['drivers']}")
    return frauds

print("📦 Exercise 5: detect_fraud() returns:")
print(detect_fraud())

# --------------------------
# EXERCISE 6 – Full Manipulation Cycle
# --------------------------
memgraph.execute("CREATE (:Driver {name: 'Temp User', id: 'TEMP123'})")
results = memgraph.execute_and_fetch("MATCH (d:Driver {id: 'TEMP123'}) RETURN d.name, d.id")
print("👀 Exercise 6 - Before update:", list(results))

memgraph.execute("""
MATCH (d:Driver {id: 'TEMP123'})
SET d.name = 'Temp Updated'
""")
results = memgraph.execute_and_fetch("MATCH (d:Driver {id: 'TEMP123'}) RETURN d.name, d.id")
print("✏️ After update:", list(results))

memgraph.execute("MATCH (d:Driver {id: 'TEMP123'}) DETACH DELETE d")
results = memgraph.execute_and_fetch("MATCH (d:Driver {id: 'TEMP123'}) RETURN d")
print("🗑 After delete (should be empty):", list(results))

print("✅ Exercise 6 complete.")
