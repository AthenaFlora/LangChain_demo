from models.md_template import MdTemplate
from application.selector.education_selector import EducationSelector
from application.selector.experience_selector import ExperienceSelector
from application.selector.project_selector import ProjectSelector
from application.selector.skill_selector import SkillSelector
from application.selector.summary_selector import SummaryCreator


class CVTemplate(MdTemplate):
    def __init__(self, template_md_path:str) -> None:
        super().__init__(template_md_path)
    
    def overwrite_template(self, contents: dict):
        to_replace = self.template
        to_replace = self._overwrite_summary( to_replace = to_replace, contents = contents)
        to_replace = self._overwrite_skills( to_replace = to_replace, contents = contents)
        to_replace = self._overwrite_experiences( to_replace = to_replace, contents = contents)
        to_replace = self._overwrite_projects( to_replace = to_replace, contents = contents)
        to_replace = self._overwrite_education( to_replace = to_replace, contents = contents)
        self.replaced = to_replace

    def get_replaced_text(self) -> str | None:
        return self.replaced
    
    def _overwrite_education(self, to_replace:str, contents:dict) -> str:
        if contents.__contains__(EducationSelector.__name__):
            start="## Education\n"
            end="\n## Languages"
            return self.replace_part(start=start, end= end, to_replace=to_replace, replace=contents[EducationSelector.__name__])
        return to_replace
    
    def _overwrite_projects(self, to_replace:str, contents:dict) -> str:
        projects = self._create_projects_content(contents=contents)
        if projects is not None:
            start="## Key Projects\n"
            end="## Education\n"
            return self.replace_part(start=start, end= end, to_replace=to_replace, replace=projects)
        return to_replace
    
    def _create_projects_content(self, contents) -> str | None:
        projects = ""
        if contents.__contains__(ProjectSelector.__name__):
            for project in contents[ProjectSelector.__name__]["projects"]:
                projects += f"- {project}\n"
            return projects
    
    def _overwrite_summary(self, to_replace:str, contents:dict) -> str:
        summary = self._create_summary_content(contents=contents)
        if summary is not None:
            start="## Summary"
            end="## Key Skills"
            return self.replace_part(start=start, end= end, to_replace=to_replace, replace=summary)
        return to_replace

    def _create_summary_content(self, contents) -> str | None:
        if contents.__contains__(SummaryCreator.__name__):
            return contents[SummaryCreator.__name__]
            
    def _overwrite_skills(self, to_replace:str, contents:dict) -> str:
        skills = self._create_skills_content(contents=contents)
        if skills is not None:
            start="## Key Skills\n"
            end="\n## Professional Experience"
            return self.replace_part(start=start, end= end, to_replace=to_replace, replace=skills)
        return to_replace

    def _create_skills_content(self, contents) -> str | None:
        if contents.__contains__(SkillSelector.__name__):
            if contents[SkillSelector.__name__]["skills"]:
                skills= str(contents[SkillSelector.__name__]["skills"]).replace("[","").replace("]","")
                return skills

    def _overwrite_experiences(self, to_replace:str, contents:dict) -> str:
        experiences = self._create_experiences_content(contents=contents)
        if experiences is not None:
            start = self.get_next_line(known_line="## Professional Experience", content=to_replace)
            end = "## Key Projects"
            if start is not None:
                return self.replace_part(start, end, to_replace, experiences)
        return to_replace

    def _create_experiences_content(self, contents) -> str | None:
        all_experiences = "\n"
        if contents.__contains__(ExperienceSelector.__name__):
            if contents[ExperienceSelector.__name__]["experiences"]:
                for category, experiences in contents[ExperienceSelector.__name__]["experiences"].items():
                    all_experiences += f"- **{category}**\n"
                    for exp in experiences:
                        all_experiences += f"   - {exp}\n"
                return all_experiences
            