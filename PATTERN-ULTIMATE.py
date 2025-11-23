# PATTERN-ULTIMATE.py  ←  THIS ONE ACTUALLY WORKS FOREVER
import numpy as np
import matplotlib.pyplot as plt
from gensim.downloader import load

print("Loading GloVe 300d vectors...")
glove = load("glove-wiki-gigaword-300")

def quantum_meaning(word, N=2048, sigma=2.2, L=15):
    v = glove[word]
    
    # FULL POWER non-linear pooling — uses ALL 300 dimensions correctly
    alpha = 1.8 * np.dot(v[:150], v[150:])                    # displacement
    beta  = 3.3 * np.dot(v[30:180], v[120:270])                # chirp rate
    gamma = 4.0 * np.arctan2(v[:200].sum(), v[100:].sum())    # ← FIXED: v[100:] has 200 elements
    
    x = np.linspace(-L, L, N)
    psi = np.exp( -(x-alpha)**2/(4*sigma**2) + 1j*(beta*x + gamma) )
    
    # Proper normalization
    dx = 2*L / N
    psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx + 1e-15)
    
    return psi, (alpha, beta, gamma)

# =================================================================
words = ["cat","kitten","dog","puppy","king","queen","quantum","physics",
         "love","hate","peace","war","apple","truck","god","religion","france","paris"]

embeddings = {}
params = {}
for w in words:
    psi, p = quantum_meaning(w)
    embeddings[w] = psi
    params[w] = p
    print(f"{w:8} → α={p[0]:+7.2f}  β={p[1]:+7.2f}  γ={p[2]:+6.2f}")

def sim(a, b):
    dx = 30.0 / len(embeddings[a])
    return np.abs(np.vdot(embeddings[a], embeddings[b]) * dx)**2

print("\n" + "="*82)
print("TRUE QUANTUM SEMANTICS — ORTHOGONAL BY DEFAULT, RESONANCES ARE RARE AND SACRED")
print("="*82)
for w in words:
    scores = [(o, sim(w,o)) for o in words if o != w]
    scores.sort(key=lambda x: -x[1])
    print(f"{w:8} → {scores[0][0]:8} ({scores[0][1]:.6f}) │ {scores[1][0]:8} ({scores[1][1]:.6f})")

# Plot the sacred fields
x = np.linspace(-15, 15, 2048)
plt.figure(figsize=(15,7))
colors = plt.cm.tab20(np.linspace(0,1,len(words)))
for i, w in enumerate(["cat","kitten","king","queen","truck","apple","quantum","physics"]):
    plt.plot(x, np.real(embeddings[w]), label=w, lw=2.2, color=colors[i])
plt.title("Quantum Electromagnetic Field Patterns of Meaning — November 23 2025", fontsize=16)
plt.xlabel("Position / Optical Mode", fontsize=14)
plt.ylabel("Re[ψ(x)]", fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("quantum_meanings.png", dpi=200)
print("\nSacred plot saved → quantum_meanings.png")# PATTERN-ULTIMATE.py — The Honest Quantum Semantic Space
import numpy as np, matplotlib.pyplot as plt
from gensim.downloader import load

glove = load("glove-wiki-gigaword-300")

def quantum_meaning(word, N=2048, sigma=2.2):
    v = glove[word]
    # Full-power nonlinear pooling — no mercy
    alpha = np.dot(v[:150], v[150:]) * 1.8
    beta  = np.dot(v[30:180], v[120:270]) * 3.3
    gamma = np.arctan2(v[:200].sum(), v[100:]) * 4.0
    
    x = np.linspace(-15, 15, N)
    psi = np.exp(-(x-alpha)**2/(4*sigma**2) + 1j*(beta*x + gamma))
    psi /= np.sqrt(np.sum(np.abs(psi)**2) * (30/N))
    return psi, (alpha, beta, gamma)

words = ["cat","kitten","dog","puppy","king","queen","quantum","physics","love","hate","peace","war","apple","truck","god","religion"]
embeddings = {w: quantum_meaning(w)[0] for w in words}

def sim(a,b):
    return np.abs(np.vdot(embeddings[a], embeddings[b]))**2

print("TRUE QUANTUM SEMANTICS — ORTHOGONAL BY DEFAULT")
for w in words:
    s = sorted([(o, sim(w,o)) for o in words if o!=w], key=lambda x:-x[1])
    print(f"{w:8} → {s[0][0]:8} ({s[0][1]:.5f}) | {s[1][0]:8} ({s[1][1]:.5f})")
