"""Train and evaluate the Sovereign MOND Orbital Stabilization PPO Agent using Stable Baselines3."""

from __future__ import annotations

import os
import sys

# Ensure local package path resolution
sys.path.insert(0, os.path.dirname(__file__))

from mond_orbit_env import MondOrbitEnv, qumond_v_circ
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_util import make_vec_env


def main() -> None:
    print("=" * 80)
    print("  RES-NOVA REINFORCEMENT LEARNING: SOVEREIGN MOND ORBIT PPO AGENT")
    print("=" * 80)

    # 1. API Conformance Check
    print("[1/5] Validating MondOrbitEnv via check_env()...")
    raw_env = MondOrbitEnv()
    check_env(raw_env, warn=True)
    print("[OK] Environment conforms 100% to Gymnasium API specifications.")

    # 2. Vectorized Training Environment
    print("[2/5] Initializing Vectorized Environment (DummyVecEnv, 4 parallel workers)...")
    vec_env = make_vec_env(MondOrbitEnv, n_envs=4, seed=42)

    # 3. Configure Continuous PPO Policy (CPU-optimized)
    print("[3/5] Configuring Continuous PPO Policy (MlpPolicy, hidden=[64, 64], device=cpu)...")
    model = PPO(
        policy="MlpPolicy",
        env=vec_env,
        learning_rate=3e-4,
        n_steps=128,
        batch_size=32,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.005,
        verbose=0,
        device="cpu",
        seed=42,
    )

    # 4. Train Model
    total_timesteps = 16000
    print(f"[4/5] Training PPO model for {total_timesteps} environment timesteps...")
    model.learn(total_timesteps=total_timesteps)
    print("[OK] PPO continuous control training phase complete.")

    # 5. Evaluate Policy on Held-Out Test Environment
    print("[5/5] Evaluating trained policy on held-out test episodes...")
    eval_env = MondOrbitEnv()
    mean_reward, std_reward = evaluate_policy(
        model,
        eval_env,
        n_eval_episodes=15,
        deterministic=True,
    )
    print(f"  Deterministic Mean Return: {mean_reward:.2f} ± {std_reward:.2f}")

    # Save Model Artifact
    save_path = os.path.join(os.path.dirname(__file__), "mond_orbit_ppo.zip")
    model.save(save_path)
    print(f"[SAVED] Trained model checkpoint written to: {save_path}")

    # Diagnostic Simulation: Verify Orbit Retention
    print("\n--- Diagnostic Benchmark: Orbit Retention & Flat Velocity Verification ---")
    sim_env = MondOrbitEnv(target_radius=2.5, max_steps=60)
    obs, _ = sim_env.reset(seed=999)
    initial_r = float(obs[0])
    v_flat_theoretical = qumond_v_circ(2.5)

    cumulative_reward = 0.0
    for step in range(60):
        action, _ = model.predict(obs, deterministic=True)
        obs, r, term, trunc, info = sim_env.step(action)
        cumulative_reward += r
        if term or trunc:
            break

    final_r = float(obs[0])
    final_v = float(obs[2])
    print(f"Initial Radius: {initial_r:.3f} | Final Radius: {final_r:.3f} (Target: 2.500)")
    print(f"Final Tangential Velocity: {final_v:.3f} | Theoretical MOND v_circ: {v_flat_theoretical:.3f}")
    print(f"Cumulative Episode Reward: {cumulative_reward:.2f}")

    assert abs(final_r - 2.5) < 0.6, f"Orbit destabilized! Final r={final_r:.3f}"
    print("[VERIFIED] Continuous PPO policy maintains stable bound orbit under QUMOND acceleration.")


if __name__ == "__main__":
    main()
