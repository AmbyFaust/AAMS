from project.modeling.ObjectModels.Launcher_and_missile import LaunchSystem, Missile


launch_system = LaunchSystem(0, 0, 0)
missile = launch_system.launch_missile()
missile.plot_trajectory()


