from crewai_tools import CSVSearchTool
from gym_trainer.crewai.utils import get_llm_config
from gym_trainer.utils import get_data_paths

gym_data_path, stretch_data_path = get_data_paths()
print(gym_data_path, stretch_data_path)

gym_rag_tool = CSVSearchTool(
    csv=gym_data_path,
    config = get_llm_config()
)

stretch_rag_tool = CSVSearchTool(
    csv=stretch_data_path,
    config = get_llm_config()
)