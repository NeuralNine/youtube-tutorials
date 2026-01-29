from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from scratch_project.tools.custom_tool import get_stock_data


@CrewBase
class ScratchProject():
    """ScratchProject crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def collector(self) -> Agent:
        return Agent(config=self.agents_config['collector'], tools=[get_stock_data], verbose=True)

    @agent
    def summarizer(self) -> Agent:
        return Agent(config=self.agents_config['summarizer'], verbose=True)

    @agent
    def risk_checker(self) -> Agent:
        return Agent(config=self.agents_config['risk_checker'], verbose=True)

    @agent
    def brief_writer(self) -> Agent:
        return Agent(config=self.agents_config['brief_writer'], verbose=True)

    @task
    def collect_task(self) -> Task:
        return Task(config = self.tasks_config['collect_task'])

    @task
    def summarize_task(self) -> Task:
        return Task(config = self.tasks_config['summarize_task'])

    @task
    def risk_task(self) -> Task:
        return Task(config = self.tasks_config['risk_task'])

    @task
    def brief_task(self) -> Task:
        return Task(config = self.tasks_config['brief_task'])

    @crew
    def crew(self) -> Crew:
        """Creates the ScratchProject crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
