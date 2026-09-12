# TARGET D7: Covariant Completion

**Status:** D7_REWRITTEN_TO_AeST (2026-09-12). The action is now Skordis–Złośnik AeST
(arXiv:2007.00082 eq. 5), matching `TARGET_D9` §1. The previous generalized-Einstein-aether
action (free function of the *vector* kinetic scalar `K` + disformal matter coupling) is
retracted **[X]**, and with it the cosmological-screening chain that rested on it.
A new, sharper obstruction is derived in §4: the `x/(1+x)` interpolation tail leaves a
**constant anomalous acceleration ≈ a₀** in the solar system.
**Last updated:** 2026-09-12
**Author:** R.W. Yett / Sovereign Architecture Group
**Tags:** `[P]` proved · `[D]` derived here · `[C]` cited · `[O]` open · `[X]` killed

---

## 0. What changed and why

`TARGET_D3` §7.1 established that D7 §2 (as written through 2026-09-12) and `TARGET_D9` §1
stated **two different theories** sharing a section number:

| | old D7 §2 | D9 §1 (= AeST) |
|---|---|---|
| free function of | `K = c₁(∇_μA_ν)(∇^μA^ν)+c₂(∇·A)²+c₃(∇_μA_ν)(∇^νA^μ)` — the **vector** | `Y` — a **scalar** gradient |
| matter coupling | disformal `g̃ = e^{2φ}g + σ²A_μA_ν` | minimal, to `g_μν` |
| class | generalized Einstein-aether (Zlosnik–Ferreira–Starkman, astro-ph/0607411) | AeST / RelMOND (Skordis–Złośnik, PRL 127 161302) |

D9 is load-bearing — `μ(x)=x/(1+x)` and `c_T=c` are both derived there — so **D9's action is
ground truth and this document is corrected to it**, per the repo's settled-decisions rule.
Everything in the old §3–§6 that was computed from `K` on an FLRW background is void, because
in AeST `Y ≡ 0` on FLRW identically. Those retractions are recorded in place, not deleted.

---

## 1. The AeST action (verbatim from the source) [C]

Skordis & Złośnik, *New Relativistic Theory for Modified Newtonian Dynamics*,
PRL **127**, 161302 (2021), arXiv:2007.00082, eq. (5):

$$S=\int d^4x\,\frac{\sqrt{-g}}{16\pi\tilde G}\Big[R-\tfrac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
+2(2-K_B)\,J^{\mu}\nabla_{\mu}\phi-(2-K_B)\,\mathcal{Y}-\mathcal{F}(\mathcal{Y},\mathcal{Q})
-\lambda\big(A^{\mu}A_{\mu}+1\big)\Big]+S_m[g]$$

with

- $F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]}$, $J_{\mu}=A^{\alpha}\nabla_{\alpha}A_{\mu}$;
- $q_{\mu\nu}=g_{\mu\nu}+A_{\mu}A_{\nu}$ (three-metric orthogonal to $A^\mu$);
- $\mathcal{Y}=q^{\mu\nu}\nabla_{\mu}\phi\nabla_{\nu}\phi$, $\mathcal{Q}=A^{\mu}\nabla_{\mu}\phi$;
- $\lambda$ enforcing $A^{\mu}A_{\mu}=-1$;
- **matter minimally coupled to $g_{\mu\nu}$ — no disformal metric anywhere in the theory.**

Retrieved 2026-09-12 from `https://ar5iv.labs.arxiv.org/html/2007.00082`; the aether kinetic
term enters **only** through $F_{\mu\nu}F^{\mu\nu}$, which is the structural reason for §6.

**Three retractions follow immediately [X]:**

1. The old §2 action (free function of $\mathcal{K}$, disformal $\tilde g$) is not this theory.
2. The couplings $c_1,c_2,c_3$ do not exist in AeST. The vector sector carries the single
   parameter $K_B$. Every statement in this corpus of the form "depends on $c_1,c_2,c_3$"
   (old §6.2, old §7 condition 3, `TARGET_D3` §7.7 as phrased) must be re-indexed onto
   $(K_B,\mathcal{K}_2,\mathcal{Q}_0,\lambda_s)$.
3. $\sigma=a_0/c^2$ was never an expansion parameter of either theory (see `TARGET_D3` §7.1).

### 1.1 Sector split

- **Cosmology** is governed by $\mathcal{Q}$, not $\mathcal{Y}$: on FLRW, $A_\mu=(-N,0,0,0)$
  and $\phi=\bar\phi(t)$, so $\mathcal{Y}=0$ **identically** and
  $\mathcal{K}(\bar{\mathcal{Q}})\equiv-\tfrac12\mathcal{F}(0,\bar{\mathcal{Q}})$ is a
  shift-symmetric $k$-essence ("gravitational Higgs phase") with a minimum at
  $\mathcal{Q}_0\neq0$, giving dust + Λ. [C]
- **Galaxies/solar system** are governed by $\mathcal{Y}$ through
  $\mathcal{J}(\mathcal{Y})\equiv\mathcal{F}(\mathcal{Y},\mathcal{Q}_0)/(2-K_B)$. [C]

The two free functions are slices of one $\mathcal{F}(\mathcal{Y},\mathcal{Q})$ but are
**observationally independent**: $\mathcal{J}$ does nothing on the FLRW background, and
$\mathcal{K}$ does nothing in the quasistatic limit beyond the mass term $\mu^2\Phi^2$.

---

## 2. Quasistatic reduction and the corrected normalisation [D]

SZ's eq. (6): with $g_{00}=-1-2\Psi$, $g_{ij}=(1-2\Phi)\gamma_{ij}$, $A^0=1-\Psi$, $A^i=0$,
$\phi=\bar\phi+\varphi$, $\mathcal{Q}=(1-\Psi)\mathcal{Q}_0$, the action reduces to eq. (2)
after $\Phi=\hat\Phi+\varphi$ and $\tilde G=(1-\tfrac{K_B}{2})\hat G$:

$$S=\int d^4x\left\{\frac{1}{8\pi\hat G}\Big[|\vec\nabla\hat\Phi|^2+\mathcal{J}(\mathcal{Y})\Big]+\Phi\rho\right\},
\qquad \mathcal{Y}=|\vec\nabla\varphi|^2$$

Varying:

$$\nabla^2\hat\Phi=4\pi\hat G\rho,\qquad
\vec\nabla\!\cdot\!\big[\mathcal{J}'(\mathcal{Y})\,\vec\nabla\varphi\big]=4\pi\hat G\rho$$

**Matter feels $\Phi=\hat\Phi+\varphi$ — the dual channel is literal**: a Newtonian channel
$\hat\Phi$ and a MOND channel $\varphi$, added at the level of the potential.

### 2.1 The factor of 2 in D9 §2 is a convention, and it is not free [D]

With the prefactor $1/(8\pi\hat G)$ above, the AQUAL function is
$$\mu_\varphi=\mathcal{J}'(\mathcal{Y})\quad\text{— not }2\mathcal{J}'.$$
`TARGET_D9` §2 writes the variation with $2\mathcal{J}'$ while §1 writes the prefactor
$a_0^2/8\pi G$; those two are inconsistent by a factor 2. The *shape* $x/(1+x)$ is unaffected;
what the factor fixes is the **tracking slope** $\lambda_s$ and hence $G_N/\hat G$. Adopt:

$$\boxed{\;\mathcal{J}(\mathcal{Y})=2\lambda_s\,\tilde a_0^{\,2}\,\mathcal{F}_{\rm dual}\!\big(\sqrt{\mathcal{Y}}/\tilde a_0\big),
\qquad \mathcal{F}_{\rm dual}(u)=\tfrac12u^2-u+\ln(1+u)\;}$$

$$\Rightarrow\quad \mathcal{J}'(\mathcal{Y})=\lambda_s\,\frac{\tilde x}{1+\tilde x},
\qquad \tilde x\equiv\frac{|\vec\nabla\varphi|}{\tilde a_0}$$

Reproduce:
```
python3 - <<'EOF'
import sympy as sp
Y,a,l,u=sp.symbols('Y at lam u',positive=True)
F=u**2/2-u+sp.log(1+u)
print(sp.simplify(sp.diff(F,u)))                                   # u^2/(1+u)
J=2*l*a**2*F.subs(u,sp.sqrt(Y)/a)
print(sp.simplify(sp.diff(J,Y)))                                   # lam*sqrt(Y)/(sqrt(Y)+at)
EOF
```

**So $\mathcal{F}_{\rm dual}$ survives the rewrite intact, as a function of the scalar
$\mathcal{Y}$ rather than the vector $\mathcal{K}$.** No reinterpretation of its functional
form is required — $\mathcal{F}_{\rm dual}(\sqrt{\mathcal{Y}}/\tilde a_0)$ *is* D9's
$\mathcal{J}$ up to the two normalisation constants $(\lambda_s,\tilde a_0)$. **[D]**

### 2.2 Both normalisations are fixed, and they are not independent [D]

SZ require $\mathcal{J}\to\frac{2\lambda_s}{3(1+\lambda_s)a_0}\mathcal{Y}^{3/2}$ as
$\vec\nabla\varphi\to0$ (this is where $a_0$ enters), and $\mathcal{J}\to\lambda_s\mathcal{Y}$
at large $\mathcal{Y}$ (tracking), with $G_N=(1+1/\lambda_s)\hat G$.

Matching the small- and large-$\tilde x$ limits of $\mathcal{J}'=\lambda_s\tilde x/(1+\tilde x)$
against those two requirements forces

$$\tilde a_0=(1+\lambda_s)\,a_0 .$$

**The scale appearing inside the free function is not the phenomenological $a_0$** — it is
larger by the tracking factor. A one-parameter family $\lambda_s\in(0,\infty)$ of AeST
theories carries $\mathcal{F}_{\rm dual}$; $\lambda_s$ is *not* fixed by the MOND limit. **[O]**

---

## 3. Cosmology: the old §3 is void [X]

**Retracted 2026-09-12.** The previous §3 set
$\mathcal{K}_0=3H^2(c_1+3c_2+c_3)\equiv\alpha H^2$ and $x_0=\sqrt{\alpha}\,H_0c/a_0\approx5.67$.
In AeST, $\mathcal{Y}=0$ on FLRW **identically** (§1.1), so there is no background value of the
free function's argument at all, and $x_0\approx5.67$ does not exist. $\alpha$ was built from
couplings the theory does not contain.

What replaces it [C]: the background is $\mathcal{K}(\mathcal{Q})=-\tfrac12\mathcal{F}(0,\mathcal{Q})$
with $\mathcal{K}=-2\Lambda+\mathcal{K}_2(\mathcal{Q}-\mathcal{Q}_0)^2+\dots$, giving
$\bar\rho=\bar\rho_0/a^3+\dots$ (dust) plus a free CC — degenerate with ΛCDM at background
level, as the old §3.1 said, but **for a different reason**: shift-symmetric $k$-essence in the
Higgs phase, not "the free function evaluated on the Newtonian branch".

$\mathcal{F}_{\rm dual}$ **says nothing about cosmology.** It is the $\mathcal{Y}$-slice.
Choosing $\mathcal{K}(\mathcal{Q})$ is a separate, still-unmade modelling decision. **[O]**

### 3.1 Two AeST cosmology constraints this corpus had never carried [C]

From SZ's own text:
1. $\mu^{-1}=\Big[\sqrt{\tfrac{2\mathcal{K}_2}{2-K_B}}\,\mathcal{Q}_0\Big]^{-1}\gtrsim1\,$Mpc,
   or the quasistatic solution turns oscillatory inside galaxies.
2. That bound implies $w_0\gtrsim10^{-8}$, against $w\lesssim0.02$ at $a\sim10^{-4}$ from
   Kopp et al. / Ilić et al. SZ state the Higgs phase therefore "cannot be extended too long
   in the past" and higher terms in $\mathcal{K}$ are needed (their Cosh / Exp examples).

---

## 4. The solar system: a constant anomalous acceleration $\approx a_0$ **[D]** **[X]** for the interpolation

This replaces the old §4 ("screening") and old §6 ("$Q_2$ resolved by a 250× suppression").
**Both are retracted.** The old suppression factors $\mathcal{F}''/\mathcal{F}'\approx0.00233$,
$429\times$ and $250\times$ were all evaluated at $x_0\approx5.67$, which §3 has just deleted.

### 4.1 $\mathcal{F}_{\rm dual}$ puts AeST on the *tracking* branch, not the screening branch [D]

$\mathcal{J}'\to\lambda_s$ as $\mathcal{Y}\to\infty$, i.e. $\mathcal{J}\to\lambda_s\mathcal{Y}$.
In SZ's classification that is **tracking** ($\varphi\to\hat\Phi/\lambda_s$,
$G_N=(1+1/\lambda_s)\hat G$), not screening. Screening would require $\mathcal{J}$ to be built
only from powers $\mathcal{Y}^{p}$, $p\ge3/2$, with no linear piece — and SZ note that even
$p\to\infty$ "may be in conflict with Mercury's orbit". **The scalar fifth force does not
switch off in the solar system; it renormalises $G$ and leaves a residual.** Compute the residual.

### 4.2 The residual is a constant, and it is $\tilde a_0$ [D]

Spherical symmetry, $\hat g\equiv\hat GM/r^2$, $g_\varphi\equiv|\vec\nabla\varphi|$. The scalar
equation integrates exactly:

$$\lambda_s\frac{g_\varphi}{\tilde a_0+g_\varphi}\;g_\varphi=\hat g
\quad\Longrightarrow\quad
g_\varphi=\frac{\hat g+\sqrt{\hat g^{\,2}+4\lambda_s\hat g\,\tilde a_0}}{2\lambda_s}
=\frac{\hat g}{\lambda_s}+\tilde a_0-\frac{\lambda_s\tilde a_0^{2}}{\hat g}+\mathcal{O}(\hat g^{-2})$$

Total acceleration felt by matter, $g=\hat g+g_\varphi$:

$$\boxed{\;g(r)=\frac{G_NM}{r^2}+\tilde a_0+\mathcal{O}\!\big(a_0^2/g\big),\qquad
G_N=(1+1/\lambda_s)\hat G,\quad \tilde a_0=(1+\lambda_s)a_0\;}$$

Deep-MOND check ($\hat g\ll\tilde a_0$): $g_\varphi\to\sqrt{\hat g\tilde a_0/\lambda_s}
=\sqrt{G_NMa_0}/r$ ✓. The interpolation is correct; the problem is the **high-$x$ tail**.

**The anomaly is $r$-independent and $\ge a_0$.** It is not a post-Newtonian correction that
decays, and it is not removable by choosing $\lambda_s$: $\tilde a_0=(1+\lambda_s)a_0>a_0$ for
every $\lambda_s>0$. Its origin is elementary: $1-\mu(x)=1/(1+x)$ falls off as $1/x$, so the
*force* deficit $a_0\,x\cdot[1-\mu]\to a_0$ tends to a constant. Any $\mu$ with a $1/x$ tail
does this. This is a statement about $\mu(x)=x/(1+x)$ alone — **it is independent of AeST vs
GEA vs any other completion.**

### 4.3 Numbers [D]

| test | predicted | bound | verdict |
|---|:-:|:-:|:-:|
| Mercury anomalous perihelion precession, $\Delta\varpi=2\pi\tilde a_0r^2/(GM)$ per orbit | **1.5 arcsec/century** (at $\lambda_s\to0$; larger otherwise) | $\sim10^{-3}$ arcsec/cy | **violated by $\sim10^{3}$** |
| Cassini-type quadrupole scale $\tilde a_0/r$ at Mercury | $1.9\times10^{-21}$ s⁻² | $Q_2<3.4\times10^{-27}$ s⁻² | **violated by $5.7\times10^{5}$** |

```
python3 - <<'EOF'
a0=1.116e-10; GM=1.32712e20; r=5.7909e10           # SPARC a0, GM_sun, Mercury a
d=2*3.141592653589793*a0*r*r/GM                     # rad per orbit
print(d, d*415*206264.8, "arcsec/century")          # 1.77e-8, 1.52
print(a0/r, (a0/r)/3.4e-27)                         # 1.93e-21 s^-2, 5.7e5
EOF
```

The two rows are **the same physics measured twice** (one constant residual force, expressed as
a precession and as a quadrupole scale), not independent tests. Note also that Cassini is not
silenced by $\Psi=\Phi$: light deflection responds to $\Phi+\Psi=2\Phi$, and the $\tilde a_0r$
piece of $\Phi$ is in there. What §7 retires is the *$\gamma\ne1$ slip* signal, not Cassini.

**Corroboration in the literature [C].** This is a known class of failure, not an in-house
novelty — which upgrades it rather than weakening it:
- Milgrom, arXiv:1205.1317 — "a correction to the dynamics of isolated mass systems even when
  they are deep in the Newtonian regime… decreases only as a power of $R/R_M$", in exactly the
  modified-Poisson (AQUAL) formulation used here.
- Desmond, arXiv:2401.04796 — the solar-system quadrupole vs the Radial Acceleration Relation
  in AQUAL/QUMOND: the interpolating functions that fit the RAR are the ones the quadrupole
  excludes. That is this tension, stated as a general theorem about the $\mu$ family.
- Milgrom, arXiv:0906.4817; Hees et al. 2016 — inner-solar-system MOND/EFE anomalies.

Note the second row reproduces, to within rounding, the **$Q_2\sim10^{-21}$ s⁻² that the old
§6.2 attributed to the external field effect.** It is the same number; the old document then
divided it by 250 using a screening factor that §3–§4 have now deleted. Without that factor
the tension is the full $5.7\times10^5$. **The $Q_2$ tension is not resolved. [X] for "resolved".**

### 4.4 What would have to change — two branches [D]/[O]

**Branch A: change the tail.** A $\mu$ whose approach to 1 is $\mathcal{O}(1/x^2)$ kills the
residual: for $\mu_{\rm std}=x/\sqrt{1+x^2}$, $1-\mu\simeq1/(2x^2)$ and the residual force is
$\simeq a_0^2/(2g)=1.6\times10^{-19}$ m s⁻² at Mercury — 9 orders below the bound.

This is a live internal conflict, not a symbol collision: $\mu_{\rm std}=x/\sqrt{1+x^2}$ is used
as *the MOND interpolation function* throughout this corpus —
`TARGET_D1` §"standard square-root interpolation", `TARGET_D2` (where $F_{\rm std}$ is shown to
satisfy all five constraints too), `FIRST_PRINCIPLES_PHYSICS_MONOGRAPH.md` §64,
`FIG_TREE_MONOGRAPH.md`, `MuProjection.lean` — while `CLM-01` and `CLM-02` of the claim ledger
carry $x/(1+x)$ and $x/\sqrt{1+x^2}$ as *separate* claims, the second already `[O]`. Most
starkly, `05_lean_formalization/AXIOMS_V2.lean:64` axiomatises the disjunction outright:
```
weak_field_balance : ∀ (x : ℝ), x > 0 → μ x = x / (1 + x) ∨ μ x = x / Real.sqrt (1 + x^2)
```
**§4.2 breaks that disjunction: the left branch is excluded by the solar system and the right
is not.** Which one the dual-channel construction actually *derives*, and whether the
rotation-curve/RAR fits survive the swap (Desmond arXiv:2401.04796 argues the trade is tight in
both directions), is the open item this rewrite hands forward. **[O]**

**Branch B: keep $\mu=x/(1+x)$ and screen with higher derivatives.** SZ explicitly leave this
door open — screening may occur "via higher-derivative terms absent from (2)", i.e. structure in
$\mathcal{F}(\mathcal{Y},\mathcal{Q})$ or beyond it that suppresses $\varphi$ at large gradients
without altering the $\mathcal{J}'$ tail. Nothing in §4.2 excludes this branch; §4.2 excludes
the *two-derivative AQUAL sector alone*. Constructing such a term and showing it leaves the
galactic regime untouched is unattempted here. **[O]**

The kill in §4.3 is therefore a kill of **$\mu=x/(1+x)$ within two-derivative AQUAL/AeST**, not
of the dual-channel idea. Stating it wider than that would overclaim.

---

## 5. Ghost freedom [D] + [C]

**Old §7's conditions 1 and 3 are re-indexed.** There are no $c_1,c_2,c_3$, so
"$c_1+c_2+c_3>0$, $c_1+c_3>0$" is void **[X]**.

What survives, in the quasistatic scalar sector: positivity of the kinetic matrix for
perturbations of $\varphi$ requires $\mathcal{J}'>0$ (transverse) and
$\mathcal{J}'+2\mathcal{Y}\mathcal{J}''>0$ (longitudinal). For $\mathcal{F}_{\rm dual}$:

$$\mathcal{J}'=\lambda_s\frac{\tilde x}{1+\tilde x}>0,\qquad
\mathcal{J}''=\frac{\lambda_s}{2\tilde a_0^{2}}\cdot\frac{1}{\tilde x(1+\tilde x)^{2}}>0
\quad\forall\,\tilde x>0 \;\;\Rightarrow\;\; \mathcal{J}'+2\mathcal{Y}\mathcal{J}''>0 \;\checkmark$$

so the $\mathcal{J}$-sector is ghost-free for all $\mathcal{Y}>0$. **[D]** (Same algebra as the
2026-09-08 correction; the argument is now $\mathcal{Y}$, and the constant $\lambda_s/2\tilde a_0^2$
is new. The 2026-09-08 finding that the pre-correction $\mathcal{F}''$ expression was a
$d/du$ derivative missing chain-rule factors stands and is preserved here.)

**This is necessary, not sufficient. [O]** SZ's ghost-freedom result is for the *full* second-order
action and additionally constrains $K_B$ (the $F^2$ vector sector) and $\mathcal{K}_2$ (the
$\mathcal{Q}$ sector). Those are conditions on functions $\mathcal{F}_{\rm dual}$ does not
specify. The old §7's claim that "$\mathcal{F}''>0$ ⇒ the SZ ghost-free condition holds"
overstated the coverage.

---

## 6. Gravitational-wave speed: now structural, and derivable [D]

The old §8 asserted $c_T=c$ "because the free function only affects the vector sector" — which
was both unargued and, on the old disformal action, **false**: a disformal matter coupling
$\tilde g=e^{2\phi}g+\sigma^2A_\mu A_\nu$ makes photons and gravitons propagate on different
cones, which is exactly how TeVeS dies against GW170817 (Boran et al. 2018; Skordis & Złośnik
2019). The rewrite removes that term, and the result becomes derivable:

1. Matter and photons couple minimally to $g_{\mu\nu}$ ⇒ photons follow $g$-null cones. [C, §1]
2. TT sector: perturb $g_{ij}=a^2(\delta_{ij}+h^{TT}_{ij})$. $\phi$ is a scalar and $A_\mu$ a
   vector; neither carries a transverse-traceless spin-2 piece, so $\mathcal{Y}$, $\mathcal{Q}$
   and $\lambda(A^2+1)$ contribute **no** $\dot h^{TT}$ or $(\partial h^{TT})^2$ terms.
3. The only aether kinetic structure is $F_{\mu\nu}F^{\mu\nu}$. On the background $A_i=0$, this
   is quadratic in $\delta A$ and contributes to $h^{TT}$ only at $\mathcal{O}(\delta A^2h)$ —
   no contribution to the TT quadratic action. The general aether terms
   $c_1(\nabla_\mu A_\nu)^2+c_3(\nabla_\mu A_\nu)(\nabla^\nu A^\mu)$ that *would* shift $c_T$
   appear only in the combination $c_1=-c_3=K_B/2$, i.e. exactly $F^2$.
4. Hence the TT quadratic action is $\propto\int\sqrt{-g}\,\big[\dot h_{ij}^2-(\partial_kh_{ij})^2\big]$
   from $R$ alone: $c_T=c$ **exactly**, for every $\mathcal{F}$, hence for $\mathcal{F}_{\rm dual}$.

$|c_T/c-1|=0\le10^{-15}$. **[D]** (structural sketch; the full second-order expansion is
Skordis & Złośnik arXiv:1905.09465 **[C]**). This is the one claim the rewrite makes *stronger*:
it moves from asserted to structural, and it is the reason D9 had to be ground truth.

---

## 7. PPN: $\gamma=1$ is now cleaner, $\beta$ is open, and the binding constraint moved [D]/[O]

- **$\gamma=1$.** SZ derive $\Psi=\Phi$ directly from eq. (5) in the quasistatic weak field
  (their text between eqs. 5 and 6), for any $\mathcal{F}$. Light deflection responds to
  $\Phi+\Psi=2\Phi$ with the same $\Phi$ matter feels, so lensing matches the dynamical mass
  with no slip: $\gamma_{\rm PPN}=1$ **[C]**, now with a source rather than D9 §0.4's assertion.
- **`TARGET_D3` §7.3–§7.5 answer the wrong question.** Foster & Jacobson's $\gamma=\beta=1$ is a
  theorem about *Einstein-aether*, which has no scalar fifth force. AeST does. With $\Psi=\Phi$
  exact there is no metric slip to bound, so the Cassini $1.1\times10^8$ / MESSENGER
  $1.6\times10^5$ margins are margins on a null observable. **The binding solar-system
  observable is §4.2's constant $\tilde a_0$, and it fails.** `TARGET_D3` §7.7's nomination of
  $\alpha_1^{\rm PPN},\alpha_2^{\rm PPN}$ as "the tightest obstruction" is superseded **[X]**;
  they are still uncomputed **[O]**, but they are no longer the first thing that breaks.
- **$\beta$** requires second order in AeST and is not given by SZ. **[O]** Published quasistatic
  spherical AeST solutions: Verwayen, Skordis, Złośnik et al., arXiv:2304.05134. **[C]**
- `TARGET_D3` §7.2's expansion parameter $\mathcal{K}\mathcal{F}''/\mathcal{F}'=1/(2(1+\sqrt{\mathcal{K}}))$
  is unaffected by the rewrite — the algebra is identical with $\mathcal{Y}$ for $\mathcal{K}$ —
  but it is the size of the *relative* correction to tracking, and §4.2 shows that correction is
  a constant *force* $\tilde a_0$, which does not decay with $r$. Bounding $|\gamma-1|$ by it was
  the error.

---

## 8. Lean follow-up (flagged, not edited)

| file | issue | action |
|---|---|---|
| `SkordisZlosnikEmbedding.lean` | `sz_aqual_reduction` proves $2\mathcal{J}'(u^2)=u/(1+u)$; §2.1 shows the factor 2 is prefactor-dependent and fixes $\lambda_s$. The *theorem* is fine as algebra; its physical reading is convention-bound. | add the normalisation hypothesis explicitly; state $\lambda_s,\tilde a_0$ |
| `SkordisZlosnikEmbedding.lean` | `sz_weak_field_lensing` ($\Phi=\Psi$) and `sz_tensor_speed_luminal` ($c_T=c_\gamma=1$) — now *better* supported (§6, §7), but check substitutability: do they close if the aether term is changed to a non-$F^2$ combination? If yes they are vacuous. | substitutability test |
| `CovariantCompletion.lean` | `F_dual_ghost_free`, `F_dual_second_deriv_antitone` are real-analysis facts about $\mathcal{F}_{\rm dual}$ and survive verbatim. Any comment/def naming the argument $\mathcal{K}$ or referencing $c_1,c_2,c_3$ is now wrong. | rename argument to $\mathcal{Y}$; delete $c_i$ references |
| `TensorSpeed.lean` | `PPN_VACUITY_AUDIT_2026-09-08.md` §5 flags that it hard-codes the Maxwell case $c_1=K/2,\;c_3=-K/2,\;c_4=0$ as an assumption. **Under AeST that is no longer an assumption — it is the theory** (§6 step 3). The audit finding is repaired by the rewrite. | re-scope the audit note; state $K_B$ |
| *(new)* | Nothing formalises §4.2. A Lean statement that $\mu(x)=x/(1+x)$ implies $g-G_NM/r^2\to\tilde a_0$ (and that $\mu=x/\sqrt{1+x^2}$ implies $\to0$) would make the negative result machine-checked and non-vacuous by construction. | propose |

---

## 9. Summary ledger

| claim | tag | basis |
|---|:-:|---|
| AeST action = SZ eq. (5); matter minimal, aether only via $F^2$ | [C] | arXiv:2007.00082 |
| Old D7 §2 (vector $\mathcal{K}$ + disformal $\tilde g$) is not AeST; retracted | [X] | §0, `TARGET_D3` §7.1 |
| $c_1,c_2,c_3$ do not exist in AeST; $\alpha=3(c_1+3c_2+c_3)$ void | [X] | §1 |
| $\mathcal{F}_{\rm dual}$ transfers to $\mathcal{J}(\mathcal{Y})$ with no change of form | [D] | §2.1, sympy |
| $\mu_\varphi=\mathcal{J}'$, not $2\mathcal{J}'$, at prefactor $1/8\pi\hat G$; D9 §1/§2 inconsistent by 2 | [D] | §2.1 |
| $\tilde a_0=(1+\lambda_s)a_0$; $\lambda_s$ unfixed by MOND limit | [D]/[O] | §2.2 |
| $\mathcal{Y}\equiv0$ on FLRW ⇒ $x_0\approx5.67$, $\mathcal{F}''/\mathcal{F}'=0.00233$, $429\times$, $250\times$ all void | [X] | §3, §4 |
| $\mathcal{F}_{\rm dual}$ is tracking, not screening | [D] | §4.1 |
| Constant residual $g-G_NM/r^2\to\tilde a_0\ge a_0$ | **[D]**+**[C]** | §4.2; Milgrom arXiv:1205.1317 |
| Mercury precession 1.5″/cy vs $10^{-3}$″/cy; $Q_2$ off by $5.7\times10^5$ (one effect, two expressions) | **[X]** for $\mu=x/(1+x)$ **within two-derivative AQUAL/AeST** | §4.3; Desmond arXiv:2401.04796 |
| `AXIOMS_V2.lean:64` axiomatises $\mu=x/(1+x)\;\vee\;\mu=x/\sqrt{1+x^2}$; §4.2 breaks the disjunction | [D] | §4.4 branch A |
| ~~Higher-derivative screening could rescue $\mu=x/(1+x)$~~ — **run down in §11, closed** | **[X]** | §11.5 |
| BDEF prove $f'>0,\,2sf''+f'>0\Rightarrow\varphi''(r)<0$ ⇒ constant $\approx a_0$ residual is forced by ghost-freedom itself, for *any* $\mathcal{J}$ | [C] | §11.1; arXiv:1106.2538 |
| No AeST paper builds SZ's screening hatch (this search, 2026-09-12) | [C] | §11.1 |
| Screening $\mathcal{F}_{\rm dual}$'s residual requires Vainshtein exponent $p\ge2.34$ (2.71 / 3.00 for dwarfs) | [D] | §11.3 |
| $c_T=c$-safe Horndeski ($G_2,G_3\Box\phi,G_4$ const) gives $\sup p=2^-$ ⇒ window empty | [D] | §11.3 |
| Cubic Galileon at max allowed $r_V$: $g_\varphi=2.7\times10^{-11}$ m s⁻², only $4\times$ better than $\tilde a_0$, still $1.4\times10^5$ over bound | [D] | §11.3 |
| BDEF's working $p=3$ term is Riemann-coupled ($G_4(X)/G_5$) ⇒ excluded by GW170817 | [D]+[C] | §11.2; arXiv:1710.05877/05901/06394 |
| §6's $c_T=c$ argument does **not** cover second-derivative operators ($\nabla\nabla\phi$ carries $\partial h^{TT}$) | [D] | §11.2 |
| Non-Horndeski ($q^{\mu\nu}\nabla_\mu\nabla_\nu\phi$, $A^\mu$) evasion at $p\ge2.34$ — the one surviving crack | [O] | §11.4 |
| Conformal (chameleon/symmetron) screening survives GW170817 but breaks shift symmetry + MOND lensing | [O]/[C] | §11.4 |
| Branch A ($\mu=x/\sqrt{1+x^2}$) is the live route; it renormalises $G$, it does **not** screen | [D] | §11.5 |
| $\mathcal{J}$-sector ghost-free ($\mathcal{J}'>0$, $\mathcal{J}''>0$) | [D] | §5 |
| Full AeST ghost-freedom ($K_B$, $\mathcal{K}_2$ conditions) | [O] | §5 |
| $c_T=c$ exactly, all $\mathcal{F}$ | [D]+[C] | §6; arXiv:1905.09465 |
| $\gamma_{\rm PPN}=1$ from $\Psi=\Phi$ | [C] | §7; SZ eq. (5)→(6) |
| $\beta$, $\alpha_1^{\rm PPN}$, $\alpha_2^{\rm PPN}$ for AeST | [O] | §7 |
| $\mu^{-1}\gtrsim$ Mpc and $w_0\gtrsim10^{-8}$ vs $w\lesssim0.02$ | [C]/[O] | §3.1 |
| $\mathcal{K}(\mathcal{Q})$ unspecified by this corpus | [O] | §3 |

---

## 10. Verdict

Rewriting D7 onto AeST costs the cosmological-screening story entirely and buys a genuinely
stronger $c_T=c$ (structural, not asserted) and a cleaner $\gamma=1$ (from $\Psi=\Phi$, not from
a vacuous theorem). $\mathcal{F}_{\rm dual}$ itself survives the transplant unchanged in form,
as $\mathcal{J}(\mathcal{Y})=2\lambda_s\tilde a_0^2\mathcal{F}_{\rm dual}(\sqrt{\mathcal{Y}}/\tilde a_0)$.
**The single tightest obstruction is no longer relativistic at all**: because $1-\mu=1/(1+x)$
decays like $1/x$, the dual-channel law leaves an $r$-independent anomalous acceleration
$\tilde a_0\ge a_0$ everywhere in the solar system — 1.5 arcsec/century at Mercury against a
$10^{-3}$ bound, corroborated as a general AQUAL phenomenon by Milgrom (arXiv:1205.1317) and
Desmond (arXiv:2401.04796). That kills $\mu(x)=x/(1+x)$ as a solar-system interpolation within
two-derivative AQUAL/AeST, regardless of the covariant completion, and it points at the
$\mu(x)=x/\sqrt{1+x^2}$ already used across this corpus — and axiomatised beside it as an
unresolved disjunction in `AXIOMS_V2.lean:64` — whose $1/x^2$ tail passes by nine orders of
magnitude. One escape remained open: SZ's higher-derivative screening (§4.4 branch B).
**§11 closes that escape:** the only published construction that achieves the required
suppression (Babichev–Deffayet–Esposito-Farèse, arXiv:1106.2538) needs a Vainshtein exponent
$p=3$, which requires an explicit Riemann–$(\nabla\varphi)^2\nabla\nabla\varphi$ coupling —
exactly the Horndeski $G_4(X)/G_5$ sector excluded by GW170817. The $c_T=c$-safe sector
$G_2+G_3\Box\varphi$ caps at $p<2$, against a requirement of $p\ge2.34$. Branch B costs
$c_T=c$; Branch A is the surviving route.

---

## 11. Branch B run down: higher-derivative screening vs. $c_T=c$ **[D]**+**[C]**+**[X]**

Added 2026-09-12. §4.4 left branch B ("keep $\mu=x/(1+x)$, screen with higher derivatives")
unattempted. It has now been attempted. **It fails, and it fails for a structural reason that
is sharper than a numerical near-miss.**

### 11.1 The literature already contains the construction — and the matching no-go [C]

Searched arXiv (`abs:"Aether-Scalar-Tensor"`, `all:"relativistic MOND" AND all:"solar system"`,
`au:Skordis_C AND abs:screening`), 2026-09-12. Findings:

- **No AeST paper builds SZ's escape hatch.** The AeST quasistatic literature
  (Verwayen–Skordis–Złośnik arXiv:2304.05134; Mistele arXiv:2305.07742; Kuzmichev et al.
  arXiv:2312.00889) studies the *two-derivative* sector — Newtonian / MOND / ghost-condensate
  oscillatory regimes — and nowhere adds a screening operator. The hatch is still only a remark
  in the PRL. **[C]** (absence here is a statement about this search, not about the literature.)
- **The construction exists, in pre-AeST form:** Babichev, Deffayet & Esposito-Farèse,
  *Improving relativistic MOND with Galileon k-mouflage*, arXiv:1106.2538 (PRD 84, 061502).
  This is precisely branch B built out, ten years earlier, on TeVeS instead of AeST. **[C]**
- **BDEF independently prove §4.2's kill, in stronger form.** Verbatim (their §I): the RAQUAL
  consistency conditions $f'(s)>0$ and $2sf''(s)+f'(s)>0$ — *the same two conditions this
  document derives in §5 as $\mathcal{J}'>0$, $\mathcal{J}'+2\mathcal{Y}\mathcal{J}''>0$ —*
  "suffice to prove that $\varphi''(r)<0$, i.e. that $\varphi'(r)$ is a decreasing function of
  $r$, and the best we can obtain is thus an almost constant force $\varphi'(r)c^2\approx a_0$
  within the solar system… But solar-system tests are precise enough to rule out a constant
  anomalous acceleration even numerically as tiny as [$a_0$]."

  So §4.2 is not an in-house novelty and not an AeST artefact: **ghost-freedom itself forces the
  constant residual in any single-scalar two-derivative sector.** This upgrades §4.3 from
  "$\mu=x/(1+x)$ fails" to "*no* $\mathcal{J}$ escapes by shape alone, given §5". **[C]**

### 11.2 What BDEF's screening term actually is, and why it cannot be transplanted [D]

BDEF add (their eq. 5)
$$\mathcal{L}_{\rm Galileon}=-\tfrac{k}{3}\,\varepsilon^{\alpha\beta\gamma\delta}\varepsilon^{\mu\nu\rho\sigma}\,\varphi_{,\alpha}\varphi_{,\mu}\varphi_{;\beta\nu}R_{\gamma\delta\rho\sigma},\qquad k\approx(100\,{\rm kpc})^4$$
whose spherical first integral (their eq. 8, on a Schwarzschild background) is
$$4k\frac{r_s}{r^2}\varphi'^2+\frac{r^2c^2}{a_0}\varphi'^2+\epsilon r^2\varphi'\approx\frac{r_s}{2}$$
giving $\varphi'\propto1/r^2$ (Brans–Dicke), $\propto1/r$ (MOND), $\propto r$ (screened) in the
three regimes. The screened branch is *absolute*: the anomalous force $\to0$, not merely its
ratio to Newtonian.

**The obstruction.** That term carries an explicit Riemann tensor contracted with
$(\nabla\varphi)^2\nabla\nabla\varphi$ — the double-dual-Riemann structure, i.e. the Horndeski
$G_4(X)$/$G_5$ sector. GW170817 + GRB170817A force $|c_T/c-1|\lesssim10^{-15}$, which in
Horndeski requires $G_{4X}=0$ and $G_5=\text{const}$ (Creminelli–Vernizzi arXiv:1710.05877;
Ezquiaga–Zumalacárregui arXiv:1710.05901; Baker et al. arXiv:1710.06394; Sakstein–Jain
arXiv:1710.05893). **[C]** On the AeST background $\nabla_\mu\phi$ is non-vanishing and
time-dependent ($\mathcal{Q}=A^\mu\nabla_\mu\phi=\mathcal{Q}_0\neq0$, §1.1), so the shift is
generic, not evaded by $\dot\varphi\to0$.

This is precisely the claim §6 makes strongest. **D7 §6's $c_T=c$ argument does not survive the
addition of BDEF's term** — §6 step 2 ("$\phi$ is a scalar, carries no TT piece") is valid for
*first* derivatives only; $\nabla_\mu\nabla_\nu\phi$ carries Christoffels containing
$\partial h^{TT}$, and $R_{\gamma\delta\rho\sigma}$ carries $h^{TT}$ outright. **[D]**

(BDEF is doubly dead post-2017 anyway: its physical metric, eq. 7,
$\tilde g_{\mu\nu}=e^{-2\varphi}g_{\mu\nu}-2\sinh(2\varphi)U_\mu U_\nu$, is the TeVeS disformal
coupling — the standard $c_T\neq c_\gamma$ kill. AeST does not need that piece, so only the
Galileon term was ever a candidate for transplant. The Galileon term is the one that fails.)

### 11.3 The GW-safe sector is quantitatively insufficient: a Vainshtein-exponent no-go [D]

Define the screening exponent $p$ by $g_\varphi/\hat g\simeq(r/r_V)^{p}$ inside the Vainshtein
radius, with $r_V\propto M^{1/3}$ for cubic-Galileon-type operators.

**Requirement (a): galaxies must stay unscreened.** $r_V(M_{\rm gal})<r_{\rm MOND}(M_{\rm gal})=\sqrt{\hat GM/a_0}$.
For a $10^{11}M_\odot$ spiral, $r_{\rm MOND}=11.2$ kpc, hence $r_V(M_\odot)<2.41$ pc.

**Requirement (b): the solar system must be quiet.** §4.3's bound on a constant anomalous
acceleration is $a_0/5.7\times10^5=2.0\times10^{-16}\,$m s$^{-2}$; at Mercury
$\hat g=3.96\times10^{-2}$ m s$^{-2}$.

$$\Rightarrow\quad p\;\ge\;\frac{\ln(2.0\times10^{-16}/3.96\times10^{-2})}{\ln(r_\mercury/r_V(M_\odot))}=\boxed{2.34}$$

and $p\ge2.71$ if $10^6M_\odot$ dwarfs must MOND, $p\ge3.00$ for BDEF's own conservative
$10^3M_\odot$ choice.

**Caveat on the parametrisation.** $p_{\rm req}=2.34$ assumes $r_V\propto M^{1/3}$, the cubic
($n=1$) scaling; BDEF's own term has $r_V\propto M^{1/4}$. The general $G_3=X^n\Box\phi$ scaling
is $r_V\propto M^{(2n-1)/(4n-1)}$, which *rises* to $M^{1/2}$ as $n\to\infty$, i.e. $r_V(M_\odot)$
falls (at $n\to\infty$, $r_V(M_\odot)\le r_{\rm MOND}(M_\odot)=733$ AU vs $4.97\times10^5$ AU at
$n=1$), which *raises* $p_{\rm req}$ to $4.37$. **$p_{\rm req}=2.34$ is therefore the most
permissive case in the family**, and every steeper mass-scaling only widens the gap. **[D]**

**What the $c_T=c$-safe sector can deliver.** After GW170817 the surviving Horndeski functions
are $G_2(\phi,X)$, $G_3(\phi,X)\Box\phi$, $G_4=$ const. Spherical first integrals **[D]**:

| operator | first integral | screened branch | $p$ |
|---|---|---|:-:|
| $G_2$ alone, $\mathcal{J}'\sim\mathcal{Y}^{m/2}$ (pure k-mouflage) | $g^{m+1}\propto\hat g$ | $g\propto\hat g^{1/(m+1)}$ | $\dfrac{2m}{m+1}\to2^{-}$ |
| $G_3=X\Box\phi$ (cubic Galileon) | $\lambda_sg+\frac{2\alpha}{\Lambda^3}\frac{g^2}{r}=\hat g$ | $g\propto(r\hat g)^{1/2}$ | $3/2$ |
| $G_3=X^n\Box\phi$ | $g^{2n}/r\propto\hat g$ | $g\propto(\hat g r)^{1/2n}$ | $2-\dfrac{1}{2n}\to2^{-}$ |
| BDEF Riemann$\times\!X\nabla\nabla\phi$ ($G_4(X)/G_5$) | $kr_sg^2/r^2\propto\hat g$ | $g\propto r$ | $3$ |

$$\boxed{\;\sup_{c_T=c\ \rm sector}p=2\;<\;2.34\le p_{\rm req}\;}$$

**Derivation of the $G_3$ row (this is the load-bearing line, so it is derived, not asserted).**
Quasistatic flat space, $\mathcal{L}_3=G_3(s)\nabla^2\varphi$ with $s=\varphi'^2$. Writing the
radial action $S=\int dr\,[\,r^2G_3\varphi''+2rG_3\varphi'\,]$ and using shift symmetry, the
first integral is
$$\mathcal{I}= -\frac{\partial\mathcal{L}}{\partial\varphi'}+\frac{d}{dr}\frac{\partial\mathcal{L}}{\partial\varphi''}
=-\big(2r^2G_3'\varphi'\varphi''+2rG_3+4rG_3's\big)+\big(2rG_3+2r^2G_3'\varphi'\varphi''\big)
=-4r\,s\,G_3'(s)$$
— the $\varphi''$ terms cancel identically (that is the Galileon property), leaving **exactly one
power of $r$, for every $G_3$**. Adding the $\mathcal{J}$ flux $r^2\mathcal{J}'(s)\varphi'$ and
the source:
$$\mathcal{J}'(g^2)\,g\;+\;\frac{4G_3'(g^2)g^2}{r}\;=\;\hat g,\qquad g\equiv|\varphi'| .$$
For $G_3\propto s^{n}$ this is $\propto g^{2n}/r$, so the screened branch is
$g\propto(\hat Gm/r)^{1/2n}$ and $g/\hat g\propto r^{\,2-1/(2n)}$. The $1/r$ is fixed by the
*derivative count* of the operator, not by $n$ — which is exactly BDEF's remark that the $1/r^2$
in their eq. (8) comes from "the large number of field derivatives" in their eq. (5). Two
derivatives ⇒ one power of $r$ ⇒ $p<2$; reaching $p=3$ needs the extra $r$-power that only the
background-Riemann contraction supplies. **[D]**

**The supremum is not attained and it is below the requirement.** This reproduces, and makes
quantitative, SZ's own aside that even $p\to\infty$ powers "may be in conflict with Mercury's
orbit". **[D]**

Explicit cubic-Galileon number: saturating (a) with $r_V(M_\odot)=2.41$ pc gives suppression
$(r_\mercury/r_V)^{3/2}=6.9\times10^{-10}$, i.e. $g_\varphi=2.7\times10^{-11}$ m s$^{-2}$ —
a factor **4** below the unscreened $\tilde a_0$, still $1.4\times10^5$ over the bound. The
constant $\tilde a_0$ *is* removed (it degrades to $\delta g\simeq g\lambda_s\tilde a_0/2\hat g
\sim10^{-9}g$), but what replaces it, an $r^{-1/2}$ force, is no smaller. **[D]**

Reproduce:
```
python3 - <<'PYEOF'
import math
a0=1.116e-10;G=6.674e-11;Ms=1.989e30;GMs=1.32712e20;rM=5.7909e10;pc=3.0857e16
gN=GMs/rM**2; ab=a0/5.7e5                       # 3.957e-2 ; 1.958e-16
for M,l in [(1e11*Ms,"1e11"),(1e6*Ms,"1e6"),(1e3*Ms,"1e3")]:
    rMo=math.sqrt(G*M/a0); rVs=rMo*(Ms/M)**(1/3.)
    print(l, rMo/pc, rVs/pc, math.log(ab/gN)/math.log(rM/rVs))   # p_req 2.342/2.712/2.996
sup=(rM/(2.408*pc))**1.5; print(sup, sup*gN, sup*gN/ab)          # 6.88e-10, 2.72e-11, 1.39e5
k=(100*1e3*pc)**4; print(9e16*rM/math.sqrt(8*k))                 # BDEF: 1.94e-16 = the bound
PYEOF
```
The last line is an independent check of the calibration: BDEF chose $k\approx(100\,$kpc$)^4$ to
sit exactly at the solar-system bound, and this document's bound reproduces their number to 1%.
Their $p=3$ clears $p_{\rm req}=3.00$ by nothing at all. **The window is not merely narrow in
$\Lambda$ — it is empty once $p\le2$.** **[D]**

### 11.4 Items not reached, and one priced alternative [O]

- **Nesting / external-field effect.** The Sun sits inside the Milky Way; a working screen must
  quiet the Sun without screening the galactic field at $R_\odot$. Not computed — §11.3 kills the
  candidate before nesting binds. **[O]**
- **Non-Horndeski evasion.** AeST carries a unit timelike $A_\mu$ and the projector $q^{\mu\nu}$.
  Operators built from $q^{\mu\nu}\nabla_\mu\nabla_\nu\phi$ and $A^\mu$ lie outside Horndeski, so
  the $G_{4X}=0$, $G_5=$const theorem does not formally apply and a degeneracy restoring $c_T=c$
  at $p\ge2.34$ is not excluded by anything derived here. This is the single surviving crack in
  §11.3, and it is narrow: the $p>2$ behaviour of BDEF comes *specifically* from the $1/r^2$
  generated by contracting with the background Riemann tensor, which is the structure GW170817
  constrains. Constructing an aether-projected analogue and computing its TT quadratic action is
  the only remaining branch-B derivation. **[O]**
- **Conformal (not disformal) screening — priced, not dismissed.** $\tilde g=e^{2\phi}g$
  preserves null cones, so chameleon/symmetron screening is *not* excluded by GW170817. Its price
  is a potential $V(\phi)$, which breaks the shift symmetry that AeST's $\mathcal{K}(\mathcal{Q})$
  ghost-condensate cosmology (§1.1, §3) is built on, and conformal coupling alone cannot produce
  MOND lensing (Bekenstein 1992 **[C]**, restated by BDEF around their eq. 7). A different
  theory, not a repair. **[O]**

### 11.5 Verdict on branch B **[X]**

Branch B is closed in the $c_T=c$ sector. Screening the $\mathcal{F}_{\rm dual}$ residual to
solar-system precision requires a Vainshtein exponent $p\ge2.34$; the post-GW170817 Horndeski
sector supplies at most $p\to2^-$; the only construction that reaches $p=3$
(arXiv:1106.2538) buys it with an explicit Riemann coupling that moves $c_T$ off $c$ — and
$c_T=c$ is the strongest result this document holds (§6). **The trade is $c_T=c$ against
$\mu=x/(1+x)$, and this corpus has already spent everything on $c_T=c$.**

Consequently §4.4's disjunction resolves: **branch A is the live route.**
`AXIOMS_V2.lean:64`'s $\mu=x/(1+x)\;\vee\;\mu=x/\sqrt{1+x^2}$ should collapse to the right
disjunct, and the open question becomes whether the dual-channel construction *derives*
$x/\sqrt{1+x^2}$ or merely tolerates it, and whether the RAR fit survives the swap
(Desmond arXiv:2401.04796). **[O]**

Note what §11.1 does *not* let us keep: BDEF's $\varphi''<0$ theorem says that under §5's
ghost conditions the scalar force in the solar system is bounded below by its MOND-scale value
$\sim a_0$ in *magnitude*. That is compatible with $\mu=x/\sqrt{1+x^2}$ only because there the
scalar force is the *tracking* force $g_\varphi\simeq\hat g\gg a_0$ and the *residual*
$g_\varphi-\hat g\simeq a_0^2/2\hat g$ is what is small. Branch A does not screen; it renormalises
$G$ and leaves a decaying remainder. Any future claim that branch A "screens" would be wrong. **[D]**

**Update 2026-09-12 — Branch A confirmed by exact solve.** `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md`
solves $\mu_{\rm std}(g_\varphi/a_0)g_\varphi=\hat g$ exactly (50-digit `mpmath` Newton, not an
asymptotic estimate) at Mercury: residual $=1.5735\ldots\times10^{-19}$ m/s², matching the
analytic $a_0^2/(2\hat g)$ prediction to 10 significant figures, clearing the Cassini-equivalent
bound by $\sim1300\times$. Ghost-free conditions ($\mathcal{J}'>0$, $\mathcal{J}'+2\mathcal{Y}
\mathcal{J}''>0$) hold identically to §5's. **What does not transfer:** D2's Padé[1/1]
uniqueness proof does not apply to $\mu_{\rm std}$ (not a rational function), and the
Fisher-identity/Hamilgrangian-split machinery (CLM-12/13/14) has no analogue found. D2's
uniqueness gap for $\mu_{\rm std}$ is now the program's central open problem.
