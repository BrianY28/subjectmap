---
order: 10
when: 1822-1845
people:
  - Claude-Louis Navier
  - Augustin-Louis Cauchy
  - "Siméon Denis Poisson"
  - George Gabriel Stokes
status: established
sources:
  - "Navier, C.-L. (1827). Mémoire sur les lois du mouvement des fluides [Memoir on the laws of fluid motion; read 1822]. Mémoires de l'Académie Royale des Sciences de l'Institut de France, 6, 389-440."
  - "Stokes, G. G. (1845). On the theories of the internal friction of fluids in motion, and of the equilibrium and motion of elastic solids. Transactions of the Cambridge Philosophical Society, 8, 287-305."
  - "Landau, L. D., & Lifshitz, E. M. (1987). Fluid Mechanics (2nd ed., Course of Theoretical Physics, Vol. 6). Pergamon Press."
drafted_by: DeepSeek V4.1 Flash
reviewed_by:
  - Claude (AI)
---

# Navier-Stokes equations

These equations express momentum balance for a viscous Newtonian fluid, combining inertia with pressure and viscous stress: ρ(∂u/∂t + u·∇u) = −∇p + μ∇²u + f, with ∇·u = 0 for incompressible flow. Navier (1822) and Stokes (1845) introduced the viscous term through Cauchy's stress tensor.

## Concepts

- **Cauchy stress tensor**: Cauchy's 1822 stress principle represents surface traction as a tensor, which yields the viscous term μ∇²u in the momentum equation.
- **Stokes flow and drag**: When inertia is negligible the equations linearize, giving Stokes flow and the drag law F = 6πμRv for a sphere (1851).
- **No-slip boundary condition**: Matching fluid velocity to solid walls closes the boundary-value problem, though slip appears in rarefied, microfluidic and superhydrophobic regimes.
- **Existence and smoothness (open)**: Whether smooth three-dimensional solutions exist for all time and all smooth data is an unsolved Clay Millennium Prize problem (2000).
