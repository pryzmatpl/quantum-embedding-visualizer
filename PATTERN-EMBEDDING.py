import numpy as np
import matplotlib.pyplot as plt  # Optional: for plotting wavefunctions

# -------------------------------------------------
# 1. Simulate infinite family → mathematical EM field patterns
# -------------------------------------------------
def quantum_embedding(word, num_points=256, sigma=2.0):
    """
    ψ(x) = N * exp( - (x - alpha)^2 / (2 sigma^2) + i * (beta * x + gamma) )
    - Envelope: Gaussian (normalizable, unlike raw |x|)
    - Phase: linear chirp (your β x term) + global (your γ)
    - Displaced by alpha for uniqueness
    """
    # Deterministic hash for unique params per word
    h = hash(word)
    np.random.seed(h % (2**32))
    alpha = np.random.uniform(-3, 3)      # center shift
    beta  = np.random.uniform(-4, 4)      # linear phase chirp (your γx)
    gamma = np.random.uniform(0, 2*np.pi) # global phase (your ϕ)

    # x grid (position basis, like EM field modes)
    x = np.linspace(-10, 10, num_points)
    
    # Complex wavefunction ψ(x)
    psi = np.exp( - (x - alpha)**2 / (2 * sigma**2) + 1j * (beta * x + gamma) )
    
    # Normalize: ∫ |ψ|^2 dx ≈ sum |psi|^2 * dx (discretized)
    dx = x[1] - x[0]
    norm = np.sqrt( np.sum(np.abs(psi)**2) * dx )
    psi /= norm
    
    return psi, (alpha, beta, gamma, sigma)

# -------------------------------------------------
# 2. Words → field patterns
# -------------------------------------------------
words = [
    "cat", "kitten", "dog", "puppy",
    "car", "truck", "apple", "banana",
    "king", "queen", "quantum", "physics", "love", "hate"
]

embeddings = {}
for w in words:
    psi, params = quantum_embedding(w)
    embeddings[w] = psi
    print(f"{w:8} → α={params[0]:+5.2f}, β={params[1]:+5.2f}, γ={params[2]:.2f}, σ={params[3]:.1f}")

# -------------------------------------------------
# 3. Quantum similarity = |⟨ψ|φ⟩|² (Born rule overlap)
# -------------------------------------------------
def quantum_similarity(a, b):
    psi_a = embeddings[a]
    psi_b = embeddings[b]
    # Proper discrete inner product with dx factor
    dx = 20.0 / len(psi_a)  # x goes from -10 to +10 → total width 20
    raw_overlap = np.vdot(psi_a, psi_b) * dx
    fidelity = np.abs(raw_overlap) ** 2
    return fidelity

# -------------------------------------------------
# 4. Results
# -------------------------------------------------
print("\n" + "="*60)
print("Quantum semantic similarity (higher = more similar via field overlap)")
print("="*60)
for w in words:
    scores = [(o, quantum_similarity(w, o)) for o in words if o != w]
    scores.sort(key=lambda x: -x[1])
    top1, top2 = scores[0], scores[1]
    print(f"{w:8} → {top1[0]:8} ({top1[1]:.4f}) | {top2[0]:8} ({top2[1]:.4f})")

# -------------------------------------------------
# 5. Bonus: Plot two example wavefunctions (Re[ψ(x)] vs x)
# -------------------------------------------------
if len(words) >= 2:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot |cat> and |kitten> real parts
    x = np.linspace(-10, 10, 256)
    ax1.plot(x, np.real(embeddings["cat"]), label="Re[ψ_cat](x)", color="blue")
    ax1.plot(x, np.real(embeddings["kitten"]), label="Re[ψ_kitten](x)", color="red", linestyle="--")
    ax1.set_title("Real Part: Chirped EM Fields")
    ax1.set_xlabel("x (position/mode)")
    ax1.legend()
    
    # Fidelity visualization (bar chart)
    sims = [quantum_similarity("cat", o) for o in words if o != "cat"]
    ax2.bar(range(len(words)-1), sims)
    ax2.set_title("Fidelity from 'cat'")
    ax2.set_xticks(range(len(words)-1))
    ax2.set_xticklabels([o for o in words if o != "cat"], rotation=45)
    ax2.set_ylabel("|⟨cat|other⟩|²")
    
    plt.tight_layout()
    plt.savefig("quantum_fields.png")  # Saves plot to file
    print(f"\nPlotted wavefunctions & similarities → saved as 'quantum_fields.png'")
    # plt.show()  # Uncomment to display interactively
