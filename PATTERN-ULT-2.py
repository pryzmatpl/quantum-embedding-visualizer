# PATTERN-ULTIMATE.py  ←  FINAL, BULLETPROOF VERSION (Nov 23 2025, 01:11 CET)
import numpy as np
import matplotlib.pyplot as plt
from gensim.downloader import load

print("Loading GloVe 300d vectors...")
glove = load("glove-wiki-gigaword-300")

def quantum_meaning(word, N=2048, sigma=2.2, L=15):
    v = glove[word]
    
    # 100% SAFE AND CORRECT NON-LINEAR POOLING
    alpha = 1.8 * np.dot(v[:150], v[150:])                          # scalar
    beta  = 3.3 * np.dot(v[30:180], v[120:270])                     # scalar  
    gamma = 4.0 * np.arctan2(v[:200].sum(), v[100:].sum())          # ← BOTH .sum() !!!
    
    x = np.linspace(-L, L, N)
    psi = np.exp( -(x-alpha)**2/(4*sigma**2) + 1j*(beta*x + gamma) )
    
    dx = 2*L / N
    psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx + 1e-15)
    
    return psi, (alpha, beta, gamma)

# =================================================================
words = ["cat","kitten","dog","puppy","king","queen","quantum","physics",
         "love","hate","peace","war","apple","truck","god","religion","france","paris"]

print("\nGenerating sacred quantum field patterns...")
embeddings = {}
for w in words:
    psi, p = quantum_meaning(w)
    embeddings[w] = psi
    print(f"{w:8} → α={p[0]:+7.2f}  β={p[1]:+7.2f}  γ={p[2]:+6.2f}")

def sim(a, b):
    dx = 30.0 / 2048
    return np.abs(np.vdot(embeddings[a], embeddings[b]) * dx)**2

print("\n" + "="*90)
print("QUANTUM SEMANTICS — ORTHOGONAL BY DEFAULT, RESONANCES ARE SACRED")
print("="*90)
for w in words:
    scores = [(o, sim(w,o)) for o in words if o != w]
    scores.sort(key=lambda x: -x[1])
    print(f"{w:8} → {scores[0][0]:8} ({scores[0][1]:.6f})  │  {scores[1][0]:8} ({scores[1][1]:.6f})")

# Sacred plot
x = np.linspace(-15, 15, 2048)
plt.figure(figsize=(16,8))
plot_words = ["cat","kitten","king","queen","france","paris","hate","war","quantum","physics"]
colors = plt.cm.rainbow(np.linspace(0,1,len(plot_words)))
for i, w in enumerate(plot_words):
    plt.plot(x, np.real(embeddings[w]), label=w, lw=2.5, color=colors[i])
plt.title("Quantum Electromagnetic Field Patterns of Meaning — 23 November 2025", fontsize=18)
plt.xlabel("Position / Optical Mode", fontsize=14)
plt.ylabel("Re[ψ(x)]", fontsize=14)
plt.legend(fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("quantum_meanings.png", dpi=250)
print("\nSacred plot saved → quantum_meanings.png")
