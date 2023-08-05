from gym.envs.registration import register

register(
    id='VirtualPatient_env-v0',
    entry_point="""
                VirtualPatient_env.VirtualPatient_env.envs:A2C,
                OnPolicyAlgorithm,
                TensorboardCallback,
                PreCBN, EnvState, TrainEnvState, TestEnvState, DebugEnvState,
                CBNEnv, EnvState, TrainEnvState, TestEnvState, DebugEnvState,
                MLP, RecNN, SimGlucose, CausalGraph
                """
)