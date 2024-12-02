import kagglehub

def get_data_paths():
    path = kagglehub.dataset_download("rishitmurarka/gym-exercises-dataset")

    gym_data_path = f"{path}/gym_exercise_dataset.csv"
    stretch_data_path = f"{path}/stretch_exercise_dataset.csv"

    return [gym_data_path, stretch_data_path]