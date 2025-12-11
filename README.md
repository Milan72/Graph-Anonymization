# Graph-Anonymization (NetGUC)

A comprehensive graph anonymization toolkit implementing various baseline and advanced anonymization techniques with utility preservation metrics.

---

## 📋 Project Structure

```
main.py                                    # GUI launcher
scripts/
  1. display_graph.py                    # Visualization
  2. naive_anonymization.py              # Naïve baselines
  3. random_add_delete.py                # Edge modification
  4. random_switch.py                    # Edge swapping
  5. random_walk.py                      # Random walk based
  6. util_*.py                           # Utility metrics
```

---

## 🎯 Anonymization Techniques

### **1. Display Graph**
**What it does:** Visualizes the original graph with labels.
- Loads MTX format network files
- Displays nodes and edges
- Reference baseline for comparison

### **2. Naïve Anonymization (NIR)**
**What it does:** Removes node identities by relabeling with generic IDs (0, 1, 2...).

**Concept:** 
- Preserves 100% of graph structure
- Only removes node labels
- Minimal privacy (structural fingerprints remain)

**Privacy:** N/A  
**Utility:** Perfect  
**Use case:** Baseline to show and compare graphs

---

### **3. Random Add/Delete**
**What it does:** Randomly adds non-existing edges and deletes existing edges k times.

**Concept:**
- Each iteration: add 1 random non-existing edge
- Each iteration: delete 1 random existing edge
- Repeats k times (k = parameter)

**Process:**
1. Find all possible edges that don't exist
2. Add one randomly
3. Delete one existing edge randomly
4. Repeat k times

**Preserves:** 
- Degree distribution (changes)
- Structural properties (disrupted)

**Privacy:** Medium  
**Utility:** Medium-Low  
**Use case:** Strong anonymization but loses utility

---

### **4. Random Switch**
**What it does:** Swaps edge endpoints k times while preserving degree distribution.

**Concept:**
- Pick two random edges: (a,b) and (c,d)
- Remove them, add (a,d) and (b,c)
- Validation: all 4 nodes distinct, new edges don't exist
- Repeats k times

**Preserves:**
- Node degrees (degree-preserving)
- Approximate clustering
- Not: Local neighborhoods (disrupted)

**Privacy:** Medium  
**Utility:** High  
**Use case:** Balance privacy and utility, preserve degree distribution

---

### **5. Random Walk Anonymization**
**What it does:** Replaces each edge with a probabilistically similar edge via random walk.

**Concept:**
- For each edge (u, v):
  1. Start random walk from v
  2. Walk k steps
  3. Reach endpoint x
  4. Replace (u, v) with (u, x)

**Preserves:**
- Degree (partially - only source node u)
- Global structure (approximately)
- Local neighborhoods (randomized)

**Privacy:** Medium  
**Utility:** Medium-High  
**Use case:** Preserve global structure while disrupting local patterns

---

## 📊 Utility Metrics

### **Betweenness Centrality (util_betweenness_centrality.py)**
**Measures:** How many shortest paths pass through each node.

- Computes normalized betweenness for all nodes
- **Utility metric:** % of nodes with betweenness ≥ k
- Visualized with viridis colormap (yellow=high, purple=low)
- Higher utility = better preservation of node importance
- **Learn more:** [Basic Definition](https://www.youtube.com/watch?v=HnnMAn-2Q6c)

### **Closeness Centrality (util_closeness_centrality.py)**
**Measures:** Average distance from a node to all others.

- Computes closeness for all nodes
- **Utility metric:** % of nodes with closeness ≥ k
- Visualized with plasma colormap
- Higher utility = nodes stay "close" to network center
- **Learn more:** [Basic Definition](https://www.youtube.com/watch?v=mYU_ql-hHTA)

### **K-Core (util_k_core.py)**
**Measures:** Dense subgraph where all nodes have degree ≥ k.

- Extracts k-core from graph
- **Utility metric:** (nodes in k-core) / (total nodes)
- Highlights core nodes in orange
- Higher utility = core structure preserved
- **Learn more:** [Basic Definition](https://www.youtube.com/watch?v=rHVrgbc_3JA)

### **K-Shell (util_k_shell.py)**
**Measures:** Nodes at specific density layer (exactly in k-core, not (k+1)-core).

- Extracts exactly k-shell
- **Utility metric:** (nodes in k-shell) / (total nodes)
- Highlights shell layer in orange
- Higher utility = layer structure preserved

---

## 🚀 Usage

### **Launch GUI:**
```bash
python main.py
```

### **How to Use:**
1. Select anonymization or utility script from dropdown
2. Enter k value (number of iterations/steps)
3. Click "Choose File and Run"
4. Select MTX format network file
5. View visualization and utility metrics

### **Input Format:**
MTX (Matrix Market) format - edge list with headers:
```
% Comment lines
rows cols edges
u1 v1
u2 v2
...
```

---

## 🔍 Privacy-Utility Trade-off

- **High Privacy, Low Utility:** Add/Delete
- **Medium Privacy, High Utility:** Switch, Random Walk
- **Low Privacy, High Utility:** Naïve (baseline only)



---

---

## 🔮 Future Work

| **Algorithms & Techniques** | **Utility Metrics** |
|----------------------------|---------------------|
| Differential privacy-based anonymization | PageRank centrality |
| k-anonymity for graphs | Eigenvector centrality |
| Edge differential privacy | Assortativity coefficient |
| Graph clustering-based anonymization | Modularity preservation |
| Machine learning-guided anonymization | Path length distribution |
| Community structure preservation | Triangle count preservation |
| Multi-level anonymization strategies | Graph diameter preservation |

---

## 📚 References

- Hay et al. (Graph anonymization via structural subgraph perturbation)
- SecGraph framework (graph anonymization evaluation)
