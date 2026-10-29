"""Unit and integration test suite for Sovereign MOND Orbit RL Environment."""

import os
import pytest
import numpy as np
from mond_orbit_env import MondOrbitEnv, qumond_acceleration, qumond_v_circ
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env


def test_qumond_asymptotics():
    # In natural units, at r=1, nu(1) = 0.5 + sqrt(1.25) ~ 1.618
    g_1 = qumond_acceleration(1.0)
    assert 1.60 < g_1 < 1.65

    # Deep MOND regime: r >> 1 (e.g. r=100)
    # g(r) should approach 1/r, so r * g(r) approaches 1.0 (flat rotation curve)
    g_100 = qumond_acceleration(100.0)
    assert abs(100.0 * g_100 - 1.0) < 0.01

    # Asymptotic circular velocity should approach 1.0
    v_circ_100 = qumond_v_circ(100.0)
    assert abs(v_circ_100 - 1.0) < 0.005


def test_gymnasium_conformance():
    env = MondOrbitEnv()
    check_env(env, warn=True)


def test_orbit_reset_bounds():
    env = MondOrbitEnv(target_radius=2.0)
    obs, info = env.reset(seed=42)
    assert obs.shape == (4,)
    assert obs.dtype == np.float32
    # Radius should be close to 2.0
    assert 1.5 < obs[0] < 2.5
    assert info["step"] == 0
    assert "v_circ" in info


def test_orbit_step_dynamics():
    env = MondOrbitEnv(target_radius=2.0, max_steps=10)
    obs, _ = env.reset(seed=101)
    # Zero thrust
    action = np.array([0.0], dtype=np.float32)
    next_obs, reward, term, trunc, info = env.step(action)
    assert next_obs.shape == (4,)
    assert isinstance(reward, float)
    assert not term
    assert not trunc
    assert "r" in info and "g_grav" in info


def test_trained_model_loading_and_inference():
    model_path = os.path.join(os.path.dirname(__file__), "mond_orbit_ppo.zip")
    assert os.path.exists(model_path), f"Checkpoint missing at {model_path}"
    model = PPO.load(model_path, device="cpu")

    env = MondOrbitEnv()
    obs, _ = env.reset(seed=202)
    action, _ = model.predict(obs, deterministic=True)
    assert action.shape == (1,)
    assert -1.0 <= action[0] <= 1.0
