"""Sovereign MOND / QUMOND Orbital Dynamics Gymnasium Environment (MondOrbitEnv-v0).

Simulates continuous-control test-particle orbital mechanics under Milgrom / QUMOND
relativistic gravity, verifying flat rotation curves and asymptotic Tully-Fisher bounds.
"""

from __future__ import annotations

import gymnasium as gym
from gymnasium import spaces
import numpy as np


def qumond_acceleration(r: float) -> float:
    """Calculate radial gravitational acceleration under standard QUMOND interpolation.

    In natural dimensionless units where r_M = sqrt(G M / a_0) = 1:
      g_N(r) = 1 / r^2
      y = g_N / a_0 = 1 / r^2
      nu(y) = 1/2 + sqrt(1/4 + 1/y) = 1/2 + sqrt(1/4 + r^2)
      g(r) = g_N * nu(y) = (1 / r^2) * [1/2 + sqrt(1/4 + r^2)]
    """
    r_safe = max(1e-4, float(r))
    y_inv = r_safe * r_safe  # 1/y = r^2
    nu = 0.5 + np.sqrt(0.25 + y_inv)
    return float((1.0 / (r_safe * r_safe)) * nu)


def qumond_v_circ(r: float) -> float:
    """Calculate circular velocity v_circ = sqrt(r * g(r)).

    For r >> 1 (deep MOND), g(r) -> 1/r, so v_circ -> 1.0 (flat rotation curve).
    """
    g = qumond_acceleration(r)
    return float(np.sqrt(max(0.0, r * g)))


class MondOrbitEnv(gym.Env):
    """Gymnasium continuous control environment for orbital stabilization in MOND potentials.

    Observation Space (Box(4), float32):
      0: r            - Radial distance [0.2 to 8.0]
      1: r_dot        - Radial velocity [-3.0 to 3.0]
      2: v_theta      - Tangential orbital velocity [0.0 to 3.0]
      3: delta_v      - Velocity deviation from circular MOND equilibrium (v_theta - v_circ)

    Action Space (Box(1), float32 in [-1.0, 1.0]):
      Radial thrust injection a_control to counter eccentric drift.
    """

    metadata = {"render_modes": ["ansi"]}

    def __init__(self, target_radius: float = 2.0, max_steps: int = 100, dt: float = 0.05) -> None:
        super().__init__()
        self.target_radius = float(target_radius)
        self.max_steps = max_steps
        self.dt = float(dt)
        self.current_step = 0

        # Observation: [r, r_dot, v_theta, delta_v]
        self.observation_space = spaces.Box(
            low=np.array([0.0, -5.0, 0.0, -5.0], dtype=np.float32),
            high=np.array([10.0, 5.0, 5.0, 5.0], dtype=np.float32),
            dtype=np.float32,
        )

        # Action: Continuous radial thrust in [-1.0, 1.0]
        self.action_space = spaces.Box(
            low=np.array([-1.0], dtype=np.float32),
            high=np.array([1.0], dtype=np.float32),
            dtype=np.float32,
        )

        self._state = np.zeros(4, dtype=np.float32)

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict | None = None,
    ) -> tuple[np.ndarray, dict]:
        super().reset(seed=seed)
        self.current_step = 0

        # Initialize test particle near target radius with slight perturbation
        r0 = float(self.np_random.uniform(self.target_radius - 0.4, self.target_radius + 0.4))
        r_dot0 = float(self.np_random.uniform(-0.1, 0.1))
        v_circ0 = qumond_v_circ(r0)
        v_theta0 = float(v_circ0 + self.np_random.uniform(-0.15, 0.15))
        delta_v0 = v_theta0 - v_circ0

        self._state = np.array([r0, r_dot0, v_theta0, delta_v0], dtype=np.float32)
        return self._state.copy(), {"step": self.current_step, "v_circ": v_circ0}

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool, dict]:
        self.current_step += 1
        r, r_dot, v_theta, _ = self._state
        a_ctrl = float(np.clip(action[0], -1.0, 1.0))

        # Equations of motion in central MOND potential
        g_grav = qumond_acceleration(r)
        centrifugal = (v_theta * v_theta) / max(1e-4, r)
        r_ddot = centrifugal - g_grav + a_ctrl

        # Angular momentum conservation: d/dt(r * v_theta) = 0 => dot(v_theta) = - (r_dot * v_theta) / r
        v_theta_dot = - (r_dot * v_theta) / max(1e-4, r)

        # Symplectic Euler integration step
        r_dot_new = r_dot + r_ddot * self.dt
        r_new = r + r_dot_new * self.dt
        v_theta_new = max(0.0, v_theta + v_theta_dot * self.dt)

        v_circ_new = qumond_v_circ(r_new)
        delta_v_new = v_theta_new - v_circ_new

        # Reward: maintain circular orbit at target radius with minimal control effort
        r_error = abs(r_new - self.target_radius)
        reward = (
            1.5                         # Survival bonus
            - 2.0 * (r_error ** 2)      # Radial distance penalty
            - 1.5 * (r_dot_new ** 2)    # Radial velocity penalty (circularity)
            - 0.5 * (delta_v_new ** 2)  # Velocity match penalty
            - 0.05 * (a_ctrl ** 2)      # Control effort regularization
        )

        self._state = np.array(
            [r_new, r_dot_new, v_theta_new, delta_v_new], dtype=np.float32
        )

        # Termination: escape or collapse into core
        terminated = bool(r_new < 0.3 or r_new > 6.0)
        truncated = bool(self.current_step >= self.max_steps)

        info = {
            "step": self.current_step,
            "r": float(r_new),
            "v_circ": float(v_circ_new),
            "g_grav": float(g_grav),
        }
        return self._state.copy(), float(reward), terminated, truncated, info

    def render(self) -> str:
        r, r_dot, v_t, dv = self._state
        return (
            f"[Step {self.current_step}] Radius: {r:.3f} | r_dot: {r_dot:.3f} | "
            f"v_theta: {v_t:.3f} (delta_v: {dv:+.3f})"
        )
